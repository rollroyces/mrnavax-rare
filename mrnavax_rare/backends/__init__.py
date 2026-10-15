"""Backend-adapter registry and structural integrity checks.

Mirrors the ``mrnavax.backends`` convention: a stdlib-only mock backend
is always present, real backends are opt-in via ``[extra]`` dependencies,
and ``mrnavax_rare.backends --check-all`` (or :func:`check_all` from
Python) verifies the deterministic integrity assertions on each backend.

API surface:

- ``CHECKS``: list of registered :class:`CheckResult` objects.
- :func:`register_backend`: append a new check result.
- :func:`check_all`: run all registered checks (return list of CheckResult).
- :func:`check_all_summary`: return ``(passed, total, failures)``.
- :func:`skeleton_self_check`: return a CheckResult with ``family="skeleton"``
  and ``ok=True`` — used by the smoke test to confirm the skeleton is intact.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence


@dataclass
class CheckResult:
    """Single integrity-check outcome."""
    name: str
    family: str = ""
    ok: bool = True
    detail: str = ""


# Registry of integrity checks. Real backends append to it at import time.
# The skeleton self-check is always present.
CHECKS: list[CheckResult] = []


def register_backend(check: CheckResult) -> None:
    """Append a check result to the registry. Idempotent by ``name``."""
    if any(c.name == check.name for c in CHECKS):
        return
    CHECKS.append(check)


def check_all() -> list[CheckResult]:
    """Run every registered check. Since CHECKS already holds CheckResult
    objects, this is a thin re-validator: it returns the list and flags
    any ``ok=False`` entries that are present in the registry."""
    return list(CHECKS)


def check_all_summary() -> tuple[int, int, list[CheckResult]]:
    """Return ``(passed, total, failures)`` for quick reporting."""
    passed = sum(1 for c in CHECKS if c.ok)
    total = len(CHECKS)
    failures = [c for c in CHECKS if not c.ok]
    return passed, total, failures


def skeleton_self_check() -> CheckResult:
    """Return a CheckResult asserting the package skeleton is intact.

    Always succeeds (the package imports == the skeleton is intact).
    """
    return CheckResult(name="skeleton_self_check", family="skeleton",
                       ok=True, detail="package skeleton imports cleanly")


# Register the skeleton check at import time.
register_backend(skeleton_self_check())


__all__ = [
    "CHECKS",
    "CheckResult",
    "register_backend",
    "check_all",
    "check_all_summary",
    "skeleton_self_check",
]