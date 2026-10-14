"""mrnavax_rare.aav — AAV vector design subsystem (v0.10).

This subsystem composes an AAV gene-therapy vector design — capsid + ITR-
flanked transgene cassette — for a target gene + optional HGVS-C variant.
It is the v0.10 deliverable and is the sibling subsystem to
``mrnavax_rare.design`` (which handles LNP-mRNA constructs).

Public surface::

    from mrnavax_rare.aav import (
        design_aav,
        AAVSpec,
        AAVVectorDesigner,
        AAV_CAPSIDS,
        AAV_PROMOTERS,
        AAV_PACKAGING_CEILING_BP,
        capsid_for_tissue,
    )

Adapter selection mirrors the rest of ``mrnavax-rare``:

- ``"auto"`` (default) → ``"mock"`` (stdlib-only rule-based; v0.10 default).
- ``"mock"`` → :class:`~mrnavax_rare.aav.adapters.mock_aav.MockAAVVectorDesigner`
  (always available).
- ``"live"`` → :class:`~mrnavax_rare.aav.adapters.live_aav.LiveAAVVectorDesigner`
  (stub; raises :class:`NotImplementedError`).
"""

from __future__ import annotations

from .data_types import (
    AAV5,
    AAV8,
    AAV9,
    AAVRH10,
    AAV_CAPSIDS,
    AAV_CAPSID_TROPISM,
    AAV_PACKAGING_BORDERLINE_MARGIN_BP,
    AAV_PACKAGING_CEILING_BP,
    AAV_PROMOTERS,
    AAVSpec,
    PackagingStatus,
    capsid_for_tissue,
)
from .protocol import AAVVectorDesigner

__all__ = [
    "AAV5",
    "AAV8",
    "AAV9",
    "AAVRH10",
    "AAV_CAPSIDS",
    "AAV_CAPSID_TROPISM",
    "AAV_PACKAGING_BORDERLINE_MARGIN_BP",
    "AAV_PACKAGING_CEILING_BP",
    "AAV_PROMOTERS",
    "AAVSpec",
    "AAVVectorDesigner",
    "PackagingStatus",
    "capsid_for_tissue",
    "design_aav",
]


def design_aav(
    target_gene: str,
    cds_wildtype: str,
    hgvs_c: str = "",
    capsid: str = "auto",
    promoter: str = "auto",
    tissue: str = "",
    backend: str = "auto",
) -> AAVSpec:
    """Design an AAV vector for ``target_gene`` on the chosen capsid.

    Parameters
    ----------
    target_gene:
        Gene symbol (e.g. ``"CFTR"``, ``"OTC"``).
    cds_wildtype:
        Wildtype CDS DNA string (A/C/G/T).
    hgvs_c:
        Optional HGVS-C variant (e.g. ``"c.1624G>T"``). Empty string means
        "deliver wildtype CDS".
    capsid:
        One of :data:`AAV_CAPSIDS`, or ``"auto"`` (default) to pick from
        ``tissue`` via :func:`capsid_for_tissue`.
    promoter:
        One of :data:`AAV_PROMOTERS`, or ``"auto"`` (default) to pick
        ``"CAG"`` for non-CNS / non-SCN1A and ``"hSyn"`` for CNS / SCN1A.
    tissue:
        Free-text tissue token (e.g. ``"lung"``, ``"liver"``, ``"cns"``).
        Used only when ``capsid == "auto"`` (and informs promoter when
        ``promoter == "auto"``).
    backend:
        ``"auto"`` (default), ``"mock"``, or ``"live"``.

    Returns
    -------
    AAVSpec
        The composed AAV vector design spec.
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
