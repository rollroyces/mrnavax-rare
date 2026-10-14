"""Live AAV vector designer stub (v0.10).

This is a :class:`NotImplementedError` stub. Reserved for a future
integration with an external viral vector design tool (e.g. an in-house
capsid engineering pipeline, ``aavlearn``, or similar). The mock adapter
is the v0.10 default; ``"auto"`` falls back to mock when no live backend
is available.
"""

from __future__ import annotations

from ..data_types import AAVSpec
from ..protocol import AAVVectorDesigner


class LiveAAVVectorDesigner(AAVVectorDesigner):
    """Stub for a future live AAV vector designer (v0.10).

    Raises :class:`NotImplementedError` on every :meth:`design` call.
    """

    def design(
        self,
        target_gene: str,
        cds_wildtype: str,
        hgvs_c: str = "",
        capsid: str = "auto",
        promoter: str = "auto",
        tissue: str = "",
    ) -> AAVSpec:
        raise NotImplementedError(
            "LiveAAVVectorDesigner is a v0.10 stub — no live AAV vector design "
            "backend is wired in this release. Use backend='mock' or "
            "backend='auto' to fall back to MockAAVVectorDesigner."
        )


__all__ = ["LiveAAVVectorDesigner"]
