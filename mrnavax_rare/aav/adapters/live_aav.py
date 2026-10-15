"""Live AAV vector designer stub (v0.10.2).

This is a :class:`NotImplementedError` stub. The v0.10.2 honest
research finding (``paper/AAV_LIVE_BACKEND_RESEARCH.md``) is that
there is no public open viral-vector design tool that the
``LiveAAVVectorDesigner`` could integrate with — BindCraft (EPFL,
*Nature* 2025) is the closest open tool but it's a *protein binder*
designer, not a full capsid engineering platform. Boltz-2 (MIT,
*Nature* 2025) is a structure predictor, not a capsid designer. The
proprietary capsid gap (4D-A101, AAV2.5T) is real and not solvable
without direct license from 4D Molecular Therapeutics or Spirovant.
"""

from __future__ import annotations

from ..data_types import AAVSpec
from ..protocol import AAVVectorDesigner


class LiveAAVVectorDesigner(AAVVectorDesigner):
    """Stub for a future live AAV vector designer (v0.10.2)."""

    def design(
        self,
        target_gene: str,
        cds_wildtype: str,
        hgvs_c: str = "",
        capsid: str = "auto",
        promoter: str = "auto",
        tissue: str = "",
        minigene: str = "",
        codon_optimized: bool = False,
        split_intein: tuple[str, str] | None = None,
        split_vector: tuple[str, str] | None = None,
        cell_type_enhancer: str = "",
    ) -> AAVSpec:
        raise NotImplementedError(
            "LiveAAVVectorDesigner is a v0.10.2 stub — no public open "
            "viral-vector design tool exists (see paper/AAV_LIVE_BACKEND_RESEARCH.md). "
            "The closest open tool is BindCraft (EPFL, Nature 2025) for "
            "de novo protein binder design, but it's not a capsid "
            "engineer. Use backend='mock' or backend='auto' to fall back "
            "to MockAAVVectorDesigner."
        )


__all__ = ["LiveAAVVectorDesigner"]
