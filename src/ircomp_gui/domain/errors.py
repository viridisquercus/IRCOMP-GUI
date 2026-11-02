"""Transport-independent failures. Project owner: Lukáš Dubšík; review pending."""

from __future__ import annotations

from ircomp_gui.domain.models import Diagnostic


class DomainError(Exception):
    """Reject an operation with stable code and sanitized field diagnostics."""

    def __init__(
        self,
        code: str,
        message: str,
        location: str | None = None,
        *,
        diagnostics: list[Diagnostic] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.diagnostics = (
            diagnostics
            if diagnostics is not None
            else [Diagnostic(code=code, message=message, location=location)]
        )
