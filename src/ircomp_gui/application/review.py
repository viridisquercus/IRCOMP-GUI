"""Review editing use cases. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

from collections.abc import Callable

from ircomp_gui.application.commands import (
    AddMember,
    CreateCollection,
    RemoveCollection,
    RemoveMember,
    RenameCollection,
    SetDecision,
)
from ircomp_gui.domain.errors import DomainError
from ircomp_gui.domain.models import Collection, Membership, Study
from ircomp_gui.domain.rules import resolve_candidate, revision_by_id


class ReviewService:
    """Change only the review layer, never imported source observations."""

    def __init__(self, new_id: Callable[[], str]) -> None:
        self.new_id = new_id

    def apply(
        self,
        study: Study,
        command: CreateCollection
        | RenameCollection
        | RemoveCollection
        | AddMember
        | RemoveMember
        | SetDecision,
    ) -> Study:
        """Apply one revision-scoped collection/membership operation atomically."""
        if isinstance(command, CreateCollection):
            _ = revision_by_id(study, command.revision_id)
            collection = Collection(
                collection_id=self.new_id(),
                revision_id=command.revision_id,
                name=command.name,
                memberships=[],
            )
            return study.model_copy(
                update={"collections": [*study.collections, collection]}
            )
        collection = next(
            (
                item
                for item in study.collections
                if item.collection_id == command.collection_id
            ),
            None,
        )
        if collection is None:
            raise DomainError("DANGLING_REFERENCE", "Review collection was not found.")
        buffers = study.draft_buffers
        if isinstance(command, RemoveCollection):
            if (
                buffers.decision
                and buffers.decision.collection_id == collection.collection_id
            ):
                buffers = buffers.model_copy(update={"decision": None})
            return study.model_copy(
                update={
                    "collections": [
                        item
                        for item in study.collections
                        if item.collection_id != collection.collection_id
                    ],
                    "draft_buffers": buffers,
                }
            )
        if isinstance(command, RenameCollection):
            changed = collection.model_copy(update={"name": command.name})
        else:
            resolve_candidate(study, command.candidate, collection.revision_id)
            member = next(
                (
                    item
                    for item in collection.memberships
                    if item.candidate == command.candidate
                ),
                None,
            )
            if isinstance(command, AddMember):
                if member:
                    return study
                changed = collection.model_copy(
                    update={
                        "memberships": [
                            *collection.memberships,
                            Membership(
                                candidate=command.candidate,
                                disposition="undecided",
                                rationale="",
                                evidence_refs=[],
                            ),
                        ]
                    }
                )
            elif isinstance(command, RemoveMember):
                changed = collection.model_copy(
                    update={
                        "memberships": [
                            item
                            for item in collection.memberships
                            if item.candidate != command.candidate
                        ]
                    }
                )
                if (
                    buffers.decision
                    and buffers.decision.collection_id == collection.collection_id
                    and buffers.decision.candidate == command.candidate
                ):
                    buffers = buffers.model_copy(update={"decision": None})
            else:
                if member is None:
                    raise DomainError(
                        "DANGLING_REFERENCE",
                        (
                            "Add the candidate to this collection before recording a "
                            "decision."
                        ),
                    )
                replacement = Membership(
                    candidate=command.candidate,
                    disposition=command.disposition,
                    rationale=command.rationale,
                    evidence_refs=command.evidence_refs,
                )
                changed = collection.model_copy(
                    update={
                        "memberships": [
                            replacement if item.candidate == command.candidate else item
                            for item in collection.memberships
                        ]
                    }
                )
                buffers = buffers.model_copy(update={"decision": None})
        return study.model_copy(
            update={
                "collections": [
                    changed if item.collection_id == changed.collection_id else item
                    for item in study.collections
                ],
                "draft_buffers": buffers,
            }
        )
