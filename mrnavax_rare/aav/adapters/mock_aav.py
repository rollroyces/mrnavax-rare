"""Stdlib-only mock AAV vector designer (v0.10 default).

This adapter composes a structural :class:`AAVSpec` for a
``(target_gene, variant)`` pair without invoking any external viral vector
design tool. The output is fully deterministic and follows the same
honest-controls contract as the rest of ``mrnavax-rare`` — every payload
field is structural (no AUPRC / F1 / efficacy predictions), and every
uncertainty is surfaced in :attr:`AAVSpec.notes`.

Design choices
--------------

- **Capsid** — ``"auto"`` resolves to ``capsid_for_tissue(tissue)`` or
  ``AAV9`` as the safest default. Unknown capsid tokens raise
  ``ValueError``.
- **Promoter** — ``"auto"`` picks ``"CAG"`` for non-CNS, ``"hSyn"`` for
  CNS / SCN1A (Dravet). Unknown promoter tokens raise ``ValueError``.
- **Variant application** — when ``hgvs_c`` is non-empty,
  :func:`mrnavax_rare.design.variant_injector.apply_hgvs_c` is called.
  Unparseable HGVS-C strings propagate as :class:`ValueError` from the
  injector — callers should treat that as a structural defect, not a
  transient failure.
- **ITRs / WPRE / bGH_polyA** — represented as length-labelled stubs
  (``"[AAV2 5'ITR | 145 bp]"``, etc.). The mock does NOT embed full AAV2
  ITR DNA (145 bp × 2 = 290 bp of repetitive GC-rich sequence).
- **Payload assembly** — ``5'ITR + promoter_label + CDS + WPRE_label +
  bGH_polyA_label + 3'ITR`` is concatenated as a string for downstream
  inspection. Length is computed from the canonical lengths recorded in
  ``_COMPONENT_LENGTHS_BP`` (not the string concatenation length, which
  is shorter because of labels).

Public surface::

    from mrnavax_rare.aav.adapters.mock_aav import MockAAVVectorDesigner
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG...",
        hgvs_c="c.1624G>T",
        tissue="lung",
    )
"""

from __future__ import annotations

from ..data_types import (
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
    capsid_for_tissue,
)
from ..protocol import AAVVectorDesigner

#: Canonical per-component lengths (in bp). These are conservative
#: structural defaults; real payloads should be computed from actual
#: sequences. The ITRs are 145 bp each (AAV2 canonical); WPRE is 599 bp;
#: bGH_polyA is 227 bp; promoter is recorded as a label (0 bp in the
#: structural length sum) — the actual promoter sequence is spliced in by
#: downstream callers.
_COMPONENT_LENGTHS_BP: dict[str, int] = {
    "5ITR": 145,
    "promoter": 0,
    "CDS": 0,  # filled at runtime
    "WPRE": 599,
    "bGH_polyA": 227,
    "3ITR": 145,
}

#: Label strings used in the assembled :attr:`AAVSpec.payload` field. These
#: are NOT sequences — they mark positions and lengths so the assembled
#: payload is human-readable.
_5ITR_LABEL = "[AAV2 5'ITR | 145 bp]"
_3ITR_LABEL = "[AAV2 3'ITR | 145 bp]"
_WPRE_LABEL = "[WPRE | 599 bp]"
_BGH_POLYA_LABEL = "[bGH_polyA | 227 bp]"

#: Capsid tokens accepted as ``capsid="auto"`` resolutions.
_CNS_TISSUE_TOKENS: tuple[str, ...] = ("cns", "brain", "neuron", "nav", "scn1a", "glia")


def _resolve_capsid(capsid: str, tissue: str) -> str:
    """Resolve ``capsid`` token to one of :data:`AAV_CAPSIDS`."""
    if capsid == "auto":
        resolved = capsid_for_tissue(tissue)
        if resolved is None:
            return AAV9
        return resolved
    if capsid in AAV_CAPSIDS:
        return capsid
    raise ValueError(
        f"Unknown capsid: {capsid!r}; expected one of {AAV_CAPSIDS} or 'auto'."
    )


def _resolve_promoter(promoter: str, tissue: str, target_gene: str) -> str:
    """Resolve ``promoter`` token to one of :data:`AAV_PROMOTERS`."""
    if promoter == "auto":
        tissue_lc = (tissue or "").strip().lower()
        gene_upper = (target_gene or "").strip().upper()
        if any(token in tissue_lc for token in _CNS_TISSUE_TOKENS) or gene_upper == "SCN1A":
            return "hSyn"
        return "CAG"
    if promoter in AAV_PROMOTERS:
        return promoter
    raise ValueError(
        f"Unknown promoter: {promoter!r}; expected one of {AAV_PROMOTERS} or 'auto'."
    )


def _packaging_status(length_bp: int) -> tuple[str, tuple[str, ...]]:
    """Return ``(status, notes)`` for a payload length."""
    if length_bp > AAV_PACKAGING_CEILING_BP:
        return (
            "over_limit",
            (
                f"payload length {length_bp} bp exceeds AAV packaging ceiling "
                f"{AAV_PACKAGING_CEILING_BP} bp — consider split-vector or "
                f"trans-splicing strategy.",
            ),
        )
    if length_bp > AAV_PACKAGING_CEILING_BP - AAV_PACKAGING_BORDERLINE_MARGIN_BP:
        return (
            "borderline",
            (
                f"payload length {length_bp} bp approaches AAV packaging "
                f"ceiling {AAV_PACKAGING_CEILING_BP} bp (within "
                f"{AAV_PACKAGING_BORDERLINE_MARGIN_BP} bp margin) — verify "
                f"full sequence lengths before manufacture.",
            ),
        )
    return ("ok", ())


class MockAAVVectorDesigner(AAVVectorDesigner):
    """Stdlib-only mock AAV vector designer (v0.10 default).

    See the module docstring for design choices. Always available; never
    raises ``ImportError``.
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
        # Lazy import — keeps the mock adapter importable without forcing
        # the variant_injector module to load.
        from ...design.variant_injector import apply_hgvs_c

        if not target_gene or not target_gene.strip():
            raise ValueError("target_gene must be a non-empty gene symbol.")
        if not cds_wildtype or not cds_wildtype.strip():
            raise ValueError("cds_wildtype must be a non-empty DNA string.")

        resolved_capsid = _resolve_capsid(capsid, tissue)
        resolved_promoter = _resolve_promoter(promoter, tissue, target_gene)

        # Variant application (HGVS-C). Empty hgvs_c means wildtype payload.
        hgvs_c_clean = (hgvs_c or "").strip()
        if hgvs_c_clean:
            cds_payload = apply_hgvs_c(cds_wildtype, hgvs_c_clean)
        else:
            cds_payload = cds_wildtype

        # Build the cassette components.
        components: dict[str, str] = {
            "5ITR": _5ITR_LABEL,
            "promoter": f"[promoter={resolved_promoter} | 0 bp]",
            "CDS": cds_payload,
            "WPRE": _WPRE_LABEL,
            "bGH_polyA": _BGH_POLYA_LABEL,
            "3ITR": _3ITR_LABEL,
        }

        # Compute payload length from the canonical per-component lengths.
        lengths: dict[str, int] = dict(_COMPONENT_LENGTHS_BP)
        lengths["CDS"] = len(cds_payload)
        payload_length = sum(lengths.values())

        packaging_status, packaging_notes = _packaging_status(payload_length)

        # Assemble the payload as a human-readable string.
        payload = (
            _5ITR_LABEL
            + components["promoter"]
            + cds_payload
            + _WPRE_LABEL
            + _BGH_POLYA_LABEL
            + _3ITR_LABEL
        )

        tropism_tags = AAV_CAPSID_TROPISM.get(resolved_capsid, ())

        notes: list[str] = list(packaging_notes)
        if hgvs_c_clean:
            notes.append(
                f"applied HGVS-C variant {hgvs_c_clean!r} to wildtype CDS "
                f"({len(cds_wildtype)} bp -> {len(cds_payload)} bp)."
            )

        return AAVSpec(
            target_gene=target_gene.strip().upper(),
            capsid=resolved_capsid,
            promoter=resolved_promoter,
            cds_wildtype=cds_wildtype,
            cds_payload=cds_payload,
            hgvs_c_applied=hgvs_c_clean,
            payload=payload,
            payload_components=components,
            payload_length_bp=payload_length,
            packaging_status=packaging_status,
            tropism_tags=tropism_tags,
            notes=tuple(notes),
        )


__all__ = ["MockAAVVectorDesigner"]
