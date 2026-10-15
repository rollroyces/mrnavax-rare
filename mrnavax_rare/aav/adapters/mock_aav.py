"""Stdlib-only mock AAV vector designer (v0.10.1 default).

This adapter composes a structural :class:`AAVSpec` for a
``(target_gene, variant)`` pair without invoking any external viral vector
design tool. The output is fully deterministic and follows the same
honest-controls contract as the rest of ``mrnavax-rare`` — every payload
field is structural (no AUPRC / F1 / efficacy predictions), and every
uncertainty is surfaced in :attr:`AAVSpec.notes`.

v0.10.1 changes
---------------

- **Minigene** — when ``minigene`` is non-empty, the CDS length is
  taken from :data:`AAV_MINIGENE_CDS_LENGTH_BP` instead of the input
  wildtype CDS. This is the canonical 4D-710 / SP-101 truncation
  strategy: CFTR with the R-domain (residues 708–835) deleted brings
  the cassette from over-ceiling to ``ok``.
- **Codon optimization** — when ``codon_optimized=True``, the CDS is
  passed through ``mrnavax.codon_lineardesign.optimize_lineardesign``
  if the backend is available. If the backend is not importable, the
  flag stays ``True`` and a note is added to the spec (the mock does
  not silently fall back to a non-codon-optimized CDS).
- **Split-intein** — when ``split_intein=("N", "C")`` is set, the
  cassette is emitted as a 2-tuple (N-half, C-half) of payloads, with
  the packaging status computed per-half. This is the Mich 2025
  SCN1A delivery strategy.
- **Cell-type enhancer** — ``cell_type_enhancer`` records a
  GABAergic / excitatory / pan-neuronal tag. A safety note is added
  when a pan-neuronal enhancer is paired with a gene in
  :data:`AAV_CELL_TYPE_CRITICAL_GENES` (e.g. SCN1A + hSyn1).
- **Proprietary-capsid caveat** — when the resolved capsid is NOT in
  the public :data:`AAV_CAPSIDS` (because the caller passed a
  proprietary token like ``"4D-A101"`` or ``"AAV2.5T"``), a caveat
  note is added to the spec.
"""

from __future__ import annotations

from ..data_types import (
    AAV5,
    AAV8,
    AAV9,
    AAVRH10,
    AAV_CAPSID_TROPISM,
    AAV_CAPSIDS,
    AAV_CELL_TYPE_CRITICAL_GENES,
    AAV_CELL_TYPE_ENHANCERS,
    AAV_MINIGENE_CDS_LENGTH_BP,
    AAV_PACKAGING_BORDERLINE_MARGIN_BP,
    AAV_PACKAGING_CEILING_BP,
    AAV_PROMOTERS,
    AAVSpec,
    capsid_for_tissue,
    resolve_minigene_cds_length,
)
from ..protocol import AAVVectorDesigner

#: Canonical per-component lengths (in bp). These are conservative
#: structural defaults; real payloads should be computed from actual
#: sequences.
_COMPONENT_LENGTHS_BP: dict[str, int] = {
    "5ITR": 145,
    "promoter": 0,
    "CDS": 0,
    "WPRE": 599,
    "bGH_polyA": 227,
    "3ITR": 145,
}

#: Split-intein per-half overhead (Mich 2025). Each half gets a small
#: intein tag (~50 aa ≈ 150 nt) plus a short linker.
_SPLIT_INTEIN_TAG_BP: int = 200

#: Label strings used in the assembled :attr:`AAVSpec.payload` field.
_5ITR_LABEL = "[AAV2 5'ITR | 145 bp]"
_3ITR_LABEL = "[AAV2 3'ITR | 145 bp]"
_WPRE_LABEL = "[WPRE | 599 bp]"
_BGH_POLYA_LABEL = "[bGH_polyA | 227 bp]"

#: Capsid tokens accepted as ``capsid="auto"`` resolutions.
_CNS_TISSUE_TOKENS: tuple[str, ...] = ("cns", "brain", "neuron", "nav", "scn1a", "glia")

#: v0.10.1 — pan-neuronal enhancers that trigger a safety note when
#: paired with a cell-type-critical gene.
_PAN_NEURONAL_ENHANCERS: frozenset[str] = frozenset({"hSyn1", "hSyn"})

#: v0.10.1 — proprietary capsid tokens (NOT in AAV_CAPSIDS) that the
#: mock recognizes to surface a caveat note.
_PROPRIETARY_CAPSID_TOKENS: frozenset[str] = frozenset({
    "4D-A101",  # 4DMT CF / ophthalmology
    "AAV2.5T",  # Spirovant CF
    "AAV2.5T-SP183",  # Spirovant SP-101 specific
})


def _resolve_capsid(capsid: str, tissue: str) -> str:
    """Resolve ``capsid`` token to one of :data:`AAV_CAPSIDS` (or proprietary)."""
    if capsid == "auto":
        resolved = capsid_for_tissue(tissue)
        if resolved is None:
            return AAV9
        return resolved
    if capsid in AAV_CAPSIDS:
        return capsid
    if capsid in _PROPRIETARY_CAPSID_TOKENS:
        return capsid
    raise ValueError(
        f"Unknown capsid: {capsid!r}; expected one of {AAV_CAPSIDS} or "
        f"a recognised proprietary token ({sorted(_PROPRIETARY_CAPSID_TOKENS)})."
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
                f"{AAV_PACKAGING_CEILING_BP} bp — consider published minigene "
                f"truncation (e.g. CFTRΔR(708–835)) or split-intein delivery "
                f"(e.g. DLX2.0-SCN1A per Mich 2025).",
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


def _try_codon_optimize(cds: str) -> tuple[str, bool]:
    """Pass the CDS through ``mrnavax.codon_lineardesign.optimize_lineardesign``."""
    try:
        from mrnavax.codon_lineardesign import optimize_lineardesign
    except ImportError:
        return cds, False
    try:
        result = optimize_lineardesign(cds)
        if isinstance(result, str):
            return result, True
        if isinstance(result, (list, tuple)) and result:
            return str(result[0]), True
        return cds, True
    except Exception:  # pragma: no cover — defensive
        return cds, False


class MockAAVVectorDesigner(AAVVectorDesigner):
    """Stdlib-only mock AAV vector designer (v0.10.1 default)."""

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
        cell_type_enhancer: str = "",
    ) -> AAVSpec:
        from ...design.variant_injector import apply_hgvs_c

        if not target_gene or not target_gene.strip():
            raise ValueError("target_gene must be a non-empty gene symbol.")
        if not cds_wildtype or not cds_wildtype.strip():
            raise ValueError("cds_wildtype must be a non-empty DNA string.")

        target_gene_clean = target_gene.strip().upper()
        resolved_capsid = _resolve_capsid(capsid, tissue)
        resolved_promoter = _resolve_promoter(promoter, tissue, target_gene)
        is_proprietary_capsid = resolved_capsid in _PROPRIETARY_CAPSID_TOKENS

        minigene_clean = (minigene or "").strip()
        minigene_cds_length = resolve_minigene_cds_length(target_gene_clean, minigene_clean)
        if minigene_clean and minigene_cds_length is None:
            raise ValueError(
                f"Unknown minigene: {minigene_clean!r}; v0.10.1 only supports "
                f"{sorted(AAV_MINIGENE_CDS_LENGTH_BP)}."
            )

        hgvs_c_clean = (hgvs_c or "").strip()
        if hgvs_c_clean:
            cds_payload = apply_hgvs_c(cds_wildtype, hgvs_c_clean)
        else:
            cds_payload = cds_wildtype

        codon_note = ""
        if codon_optimized:
            cds_payload, used_live = _try_codon_optimize(cds_payload)
            if not used_live:
                codon_note = (
                    "codon_optimized=True requested but mrnavax.codon_lineardesign "
                    "backend not importable; CDS passed through unchanged."
                )

        components: dict[str, str] = {
            "5ITR": _5ITR_LABEL,
            "promoter": f"[promoter={resolved_promoter} | 0 bp]",
            "CDS": cds_payload,
            "WPRE": _WPRE_LABEL,
            "bGH_polyA": _BGH_POLYA_LABEL,
            "3ITR": _3ITR_LABEL,
        }

        if minigene_cds_length is not None:
            cds_for_length = minigene_cds_length
        else:
            cds_for_length = len(cds_payload)

        lengths: dict[str, int] = dict(_COMPONENT_LENGTHS_BP)
        lengths["CDS"] = cds_for_length
        payload_length = sum(lengths.values())

        if split_intein is not None:
            if len(split_intein) != 2:
                raise ValueError(
                    f"split_intein must be a 2-tuple (e.g. ('N', 'C')); got {split_intein!r}"
                )
            half_label_N, half_label_C = split_intein
            half_cds_length = cds_for_length // 2 + _SPLIT_INTEIN_TAG_BP
            half_length = (
                _COMPONENT_LENGTHS_BP["5ITR"]
                + _COMPONENT_LENGTHS_BP["promoter"]
                + half_cds_length
                + _COMPONENT_LENGTHS_BP["WPRE"]
                + _COMPONENT_LENGTHS_BP["bGH_polyA"]
                + _COMPONENT_LENGTHS_BP["3ITR"]
            )
            half_status_N, half_notes_N = _packaging_status(half_length)
            payload = (
                _5ITR_LABEL
                + components["promoter"]
                + f"[{half_label_N}-half CDS | {half_cds_length} bp]"
                + f"[intein-{half_label_N} | {_SPLIT_INTEIN_TAG_BP} bp]"
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL,
                _5ITR_LABEL
                + components["promoter"]
                + f"[intein-{half_label_C} | {_SPLIT_INTEIN_TAG_BP} bp]"
                + f"[{half_label_C}-half CDS | {half_cds_length} bp]"
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL,
            )
            payload_length_bp = half_length
            packaging_status = half_status_N
            payload_packaging_notes = half_notes_N
        else:
            payload = (
                _5ITR_LABEL
                + components["promoter"]
                + cds_payload
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL
            )
            payload_length_bp = payload_length
            packaging_status, payload_packaging_notes = _packaging_status(payload_length)

        tropism_tags = AAV_CAPSID_TROPISM.get(resolved_capsid, ())

        notes: list[str] = list(payload_packaging_notes)
        if hgvs_c_clean:
            notes.append(
                f"applied HGVS-C variant {hgvs_c_clean!r} to wildtype CDS "
                f"({len(cds_wildtype)} bp -> {len(cds_payload)} bp)."
            )
        if minigene_cds_length is not None:
            notes.append(
                f"minigene {minigene_clean!r} used: CDS length for payload "
                f"calculation is {minigene_cds_length} bp (per 4D-710 / SP-101)."
            )
        if codon_note:
            notes.append(codon_note)
        if split_intein is not None:
            notes.append(
                f"split-intein delivery: two-cassette payload (N-half + C-half), "
                f"each ~{payload_length_bp} bp, assembled via protein trans-splicing "
                f"per Mich 2025 *Sci Transl Med* 17:eadn5603."
            )
        if is_proprietary_capsid:
            notes.append(
                f"proprietary capsid {resolved_capsid!r} used; not in public "
                f"AAV_CAPSIDS — requires direct license from the developer."
            )

        enhancer_clean = (cell_type_enhancer or "").strip()
        enhancer_note = ""
        if enhancer_clean and enhancer_clean not in AAV_CELL_TYPE_ENHANCERS:
            enhancer_note = (
                f"unrecognised cell_type_enhancer {enhancer_clean!r}; not in "
                f"the canonical AAV_CELL_TYPE_ENHANCERS list — verify safety."
            )
        elif (
            enhancer_clean in _PAN_NEURONAL_ENHANCERS
            and target_gene_clean in AAV_CELL_TYPE_CRITICAL_GENES
        ):
            enhancer_note = (
                f"SAFETY: pan-neuronal enhancer {enhancer_clean!r} paired with "
                f"cell-type-critical gene {target_gene_clean!r} — Mich et al. 2025 "
                f"*Sci Transl Med* 17:eadn5603 reported dose-dependent preweaning "
                f"mortality with hSyn1-SCN1A in DS mice. Consider hDLXI5/6i "
                f"GABAergic-interneuron enhancer instead."
            )

        if enhancer_note:
            notes.append(enhancer_note)

        caveat = None
        if is_proprietary_capsid:
            caveat = (
                f"Capsid {resolved_capsid!r} is proprietary and not in the public "
                f"mrnavax-rare AAV_CAPSIDS registry. The mock emits a structural "
                f"design but does NOT validate the capsid's tropism, packaging, or "
                f"safety against the developer's published data."
            )

        return AAVSpec(
            target_gene=target_gene_clean,
            capsid=resolved_capsid,
            promoter=resolved_promoter,
            cds_wildtype=cds_wildtype,
            cds_payload=cds_payload,
            hgvs_c_applied=hgvs_c_clean,
            payload=payload,
            payload_components=components,
            payload_length_bp=payload_length_bp,
            packaging_status=packaging_status,
            tropism_tags=tropism_tags,
            notes=tuple(notes),
            minigene=minigene_clean or None,
            codon_optimized=codon_optimized,
            split_intein=split_intein,
            cell_type_enhancer=enhancer_clean or None,
            proprietary_capsid_caveat=caveat,
        )


__all__ = ["MockAAVVectorDesigner"]
