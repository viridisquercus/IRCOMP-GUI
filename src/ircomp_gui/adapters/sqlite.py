"""Atomic SQLite snapshots. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from pydantic import ValidationError

from ircomp_gui.adapters.exchange import MAX_DOCUMENT, Exchange, encode_json, parse_json
from ircomp_gui.application.ports import SavedStudy, StudySummary
from ircomp_gui.domain.catalogue import Catalogue
from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import Study
from ircomp_gui.domain.rules import validate_study


class SQLiteRepository:
    """One aggregate per row prevents partially saved evidence/review state."""

    def __init__(self, path: Path, catalogue: Catalogue, exchange: Exchange) -> None:
        self.path = path
        self.catalogue = catalogue
        self.exchange = exchange
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with self._connection() as connection:
                version = connection.execute("PRAGMA user_version").fetchone()[0]
                if version not in {0, 1}:
                    raise DomainError(
                        "SCHEMA_INVALID",
                        "Unsupported database layout; the file was not changed.",
                    )
                _ = connection.execute(
                    "CREATE TABLE IF NOT EXISTS studies (study_id TEXT PRIMARY "
                    "KEY, request_id TEXT NOT NULL UNIQUE, saved_version INTEGER "
                    "NOT NULL CHECK(saved_version > 0), title TEXT NOT NULL, "
                    "updated_at TEXT NOT NULL, document_json TEXT NOT NULL)"
                )
                _ = connection.execute("PRAGMA user_version = 1")
        except (sqlite3.Error, OSError) as error:
            raise DomainError(
                "PERSISTENCE_UNAVAILABLE", "Cannot open the local study database."
            ) from error

    @contextmanager
    def _connection(self) -> Generator[sqlite3.Connection, None, None]:
        connection = sqlite3.connect(self.path, isolation_level=None, timeout=5)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        finally:
            connection.close()

    def list(self) -> list[StudySummary]:
        """List saved metadata without loading large source records."""
        try:
            with self._connection() as connection:
                rows = connection.execute(
                    "SELECT study_id, title, saved_version, updated_at FROM "
                    "studies ORDER BY updated_at DESC, study_id"
                ).fetchall()
                return [StudySummary.model_validate(dict(row)) for row in rows]
        except sqlite3.Error as error:
            raise DomainError(
                "PERSISTENCE_UNAVAILABLE", "Cannot list saved studies."
            ) from error

    def identity_exists(self, study_id: str, request_id: str) -> str | None:
        """Check both identity namespaces before accepting an imported request."""
        try:
            with self._connection() as connection:
                row = connection.execute(
                    "SELECT study_id FROM studies WHERE study_id = ? OR request_id = ?",
                    (study_id, request_id),
                ).fetchone()
                return str(row["study_id"]) if row else None
        except sqlite3.Error as error:
            raise DomainError(
                "PERSISTENCE_UNAVAILABLE", "Cannot check saved request identity."
            ) from error

    def load(self, study_id: str) -> SavedStudy:
        """Fail on corrupt content, mismatched metadata or unsupported versions."""
        try:
            with self._connection() as connection:
                row = connection.execute(
                    "SELECT * FROM studies WHERE study_id = ?", (study_id,)
                ).fetchone()
            if row is None:
                raise DomainError("NOT_FOUND", "Saved study was not found.")
            document = parse_json(
                row["document_json"].encode("utf-8"), limit=MAX_DOCUMENT
            )
            if (
                set(document) != {"storage_version", "study"}
                or type(document["storage_version"]) is not int
                or document["storage_version"] != 1
            ):
                raise DomainError(
                    "SCHEMA_INVALID", "Unsupported stored document; it was not changed."
                )
            study = Study.model_validate(document["study"])
            if (
                study.study_id != row["study_id"]
                or study.request_id != row["request_id"]
                or study.title != row["title"]
            ):
                raise DomainError(
                    "SCHEMA_INVALID",
                    "Stored study metadata disagrees with its document.",
                )
            validate_study(study, self.catalogue)
            self.exchange.verify_sources(study)
            return SavedStudy(
                study=study,
                saved_version=row["saved_version"],
                updated_at=row["updated_at"],
            )
        except (ValidationError, ValueError, TypeError) as error:
            raise DomainError(
                "SCHEMA_INVALID", "Stored study is invalid; it was not changed."
            ) from error
        except sqlite3.Error as error:
            raise DomainError(
                "PERSISTENCE_UNAVAILABLE", "Cannot read the saved study."
            ) from error

    def save(self, study: Study, expected_saved_version: int) -> int:
        """Compare-and-save in an explicit transaction; rollback every failed write."""
        validate_study(study, self.catalogue)
        self.exchange.verify_sources(study)
        raw = encode_json(
            {"storage_version": 1, "study": study.model_dump(mode="json")}
        ).decode("utf-8")
        updated_at = datetime.now(UTC).isoformat()
        version = expected_saved_version + 1
        try:
            with self._connection() as connection:
                _ = connection.execute("BEGIN IMMEDIATE")
                try:
                    if expected_saved_version == 0:
                        _ = connection.execute(
                            "INSERT INTO studies VALUES (?, ?, ?, ?, ?, ?)",
                            (
                                study.study_id,
                                study.request_id,
                                version,
                                study.title,
                                updated_at,
                                raw,
                            ),
                        )
                    else:
                        cursor = connection.execute(
                            "UPDATE studies SET saved_version = ?, title = ?, "
                            "updated_at = ?, document_json = ? "
                            "WHERE study_id = ? AND request_id = ? "
                            "AND saved_version = ?",
                            (
                                version,
                                study.title,
                                updated_at,
                                raw,
                                study.study_id,
                                study.request_id,
                                expected_saved_version,
                            ),
                        )
                        if cursor.rowcount != 1:
                            raise DomainError(
                                "SAVE_CONFLICT",
                                "A newer saved study exists. Keep your work "
                                "and resolve the conflict explicitly.",
                            )
                    _ = connection.execute("COMMIT")
                except Exception:
                    _ = connection.execute("ROLLBACK")
                    raise
        except sqlite3.IntegrityError as error:
            raise DomainError(
                "SAVE_CONFLICT",
                (
                    "This study/request identity is already saved. Open it or "
                    "duplicate the request."
                ),
            ) from error
        except sqlite3.Error as error:
            raise DomainError(
                "PERSISTENCE_UNAVAILABLE",
                (
                    "Save failed. Your working changes are still available; retry"
                    " when storage is writable."
                ),
            ) from error
        return version
