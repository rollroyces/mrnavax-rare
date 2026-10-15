"""``mrnavax_rare.aav`` — AAV vector design subsystem (v0.10.2)."""

from __future__ import annotations

from .data_types import (
    AAV5,
    AAV8,
    AAV9,
    AAVRH10,
    AAV_CAPSIDS,
    AAV_CAPSID_TROPISM,
    AAV_CELL_TYPE_CRITICAL_GENES,
    AAV_CELL_TYPE_ENHANCERS,
    AAV_MINIGENE_CDS_LENGTH_BP,
    AAV_PACKAGING_BORDERLINE_MARGIN_BP,
    AAV_PACKAGING_CEILING_BP,
    AAV_PHP_EB,
    AAV_PROMOTERS,
    AAVSpec,
    PackagingStatus,
    capsid_for_tissue,
    resolve_minigene_cds_length,
)
from .protocol import AAVVectorDesigner

__all__ = [
    "AAV5",
    "AAV8",
    "AAV9",
    "AAVRH10",
    "AAV_CAPSIDS",
    "AAV_CAPSID_TROPISM",
    "AAV_CELL_TYPE_CRITICAL_GENES",
    "AAV_CELL_TYPE_ENHANCERS",
    "AAV_MINIGENE_CDS_LENGTH_BP",
    "AAV_PACKAGING_BORDERLINE_MARGIN_BP",
    "AAV_PACKAGING_CEILING_BP",
    "AAV_PHP_EB",
    "AAV_PROMOTERS",
    "AAVSpec",
    "AAVVectorDesigner",
    "PackagingStatus",
    "capsid_for_tissue",
    "design_aav",
    "resolve_minigene_cds_length",
]


def design_aav(
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
    backend: str = "auto",
) -> AAVSpec:
    """Design an AAV vector for ``target_gene`` on the chosen capsid.

    v0.10.1 parameters:
    - ``minigene``, ``codon_optimized``, ``split_intein`` (Mich 2025),
      ``cell_type_enhancer``

    v0.10.2 parameters:
    - ``split_vector`` (older dual-AAV trans-splicing approach, e.g.
      4DMT DMD). Mutually exclusive with ``split_intein``.
    """
    if backend == "auto":
        backend = "mock"
    if backend == "mock":
        from .adapters.mock_aav import MockAAVVectorDesigner

        return MockAAVVectorDesigner().design(
            target_gene=target_gene,
            cds_wildtype=cds_wildtype,
            hgvs_c=hgvs_c,
            capsid=capsid,
            promoter=promoter,
            tissue=tissue,
            minigene=minigene,
            codon_optimized=codon_optimized,
            split_intein=split_intein,
            split_vector=split_vector,
            cell_type_enhancer=cell_type_enhancer,
        )
    if backend == "live":
        from .adapters.live_aav import LiveAAVVectorDesigner

        return LiveAAVVectorDesigner().design(
            target_gene=target_gene,
            cds_wildtype=cds_wildtype,
            hgvs_c=hgvs_c,
            capsid=capsid,
            promoter=promoter,
            tissue=tissue,
        )
    raise ValueError(
        f"Unknown AAV backend: {backend!r}; expected one of 'auto', 'mock', 'live'."
    )
