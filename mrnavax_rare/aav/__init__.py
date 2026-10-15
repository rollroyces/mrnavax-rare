"""``mrnavax_rare.aav`` — AAV vector design subsystem (v0.10.1).

This subsystem composes an AAV gene-therapy vector design — capsid + ITR-
flanked transgene cassette — for a target gene + optional HGVS-C variant.
It is the v0.10 deliverable and is the sibling subsystem to
``mrnavax_rare.design`` (which handles LNP-mRNA constructs).

v0.10.1 changes (validated against published wet-lab programs; see
``paper/AAV_WET_LAB_VALIDATION.md``):

- **Minigene support** — :attr:`AAVSpec.minigene` selects a published
  truncation strategy (e.g. ``"CFTRΔR(708–835)"`` for the 4D-710 /
  SP-101 CF program).
- **Codon optimization** — :attr:`AAVSpec.codon_optimized` (bool) wires
  the cassette through ``mrnavax.codon_lineardesign.optimize_lineardesign``.
- **Split-intein delivery** — :attr:`AAVSpec.split_intein` (2-tuple)
  emits a two-cassette payload (N-half + C-half) for very large genes
  like SCN1A (Mich 2025 *Sci Transl Med* 17:eadn5603).
- **Cell-type enhancer** — :attr:`AAVSpec.cell_type_enhancer` records
  a GABAergic / excitatory / pan-neuronal tag; a safety note is added
  when a pan-neuronal enhancer is paired with a known cell-type-
  critical gene (e.g. SCN1A).
- **AAV-PHP.eB** — added to :data:`AAV_CAPSIDS` as the first
  non-wildtype capsid.
- **Proprietary capsid support** — ``MockAAVVectorDesigner`` recognizes
  ``"4D-A101"`` and ``"AAV2.5T"`` and emits a caveat note.

Public surface::

    from mrnavax_rare.aav import (
        design_aav,
        AAVSpec,
        AAVVectorDesigner,
        AAV_CAPSIDS,
        AAV_CELL_TYPE_ENHANCERS,
        AAV_MINIGENE_CDS_LENGTH_BP,
        AAV_PHP_EB,
        AAV_PROMOTERS,
        AAV_PACKAGING_CEILING_BP,
        capsid_for_tissue,
    )
"""

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
    cell_type_enhancer: str = "",
    backend: str = "auto",
) -> AAVSpec:
    """Design an AAV vector for ``target_gene`` on the chosen capsid.

    v0.10.1 adds four optional parameters:

    - ``minigene`` — select a published minigene truncation
      (e.g. ``"CFTRΔR(708–835)"``).
    - ``codon_optimized`` — wire the CDS through
      ``mrnavax.codon_lineardesign.optimize_lineardesign`` if the
      backend is available.
    - ``split_intein`` — emit a two-cassette payload for very large
      genes (Mich 2025 strategy).
    - ``cell_type_enhancer`` — record a cell-type specific enhancer
      (e.g. ``"hDLXI5/6i"`` for GABAergic interneurons); pan-neuronal
      enhancers paired with cell-type-critical genes trigger a
      safety note.
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
