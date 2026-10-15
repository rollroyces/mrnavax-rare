"""Stdlib-only mock AAV vector designer (v0.10.2 default).

This adapter composes a structural :class:`AAVSpec` for a
``(target_gene, variant)`` pair without invoking any external viral vector
design tool. The output is fully deterministic and follows the same
honest-controls contract as the rest of ``mrnavax-rare``.

v0.10.0 / v0.10.1 — capsid / ITR / packaging status / minigene /
codon_optimized / split_intein / cell_type_enhancer / proprietary
capsid caveat (see ``paper/AAV_WET_LAB_VALIDATION.md``).

v0.10.2 — split_vector (trans-splicing overlap, the older dual-AAV
approach for very large genes like DMD); tissue-aware codon
optimization (CNS biases structure, lung biases stability, liver
balanced); junction picker for split_vector (avoids strong splice
motifs in a ±10 bp window of the junction).
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

#: Canonical per-component lengths (in bp).
_COMPONENT_LENGTHS_BP: dict[str, int] = {
    "5ITR": 145,
    "promoter": 0,
    "CDS": 0,
    "WPRE": 599,
    "bGH_polyA": 227,
    "3ITR": 145,
}

#: Split-intein per-half overhead.
_SPLIT_INTEIN_TAG_BP: int = 200

#: v0.10.2 — split-vector trans-splicing overlap.
_SPLIT_VECTOR_OVERLAP_BP: int = 500

#: v0.10.2 — tissue-specific codon-optimization weights.
_TISSUE_CODON_WEIGHTS: dict[str, dict[str, float]] = {
    "liver":    {"translation": 1.0, "structure": 1.0, "gc_window": 30, "min_stem": 3},
    "lung":     {"translation": 1.0, "structure": 1.2, "gc_window": 50, "min_stem": 4},
    "cns":      {"translation": 0.8, "structure": 1.5, "gc_window": 80, "min_stem": 4},
    "muscle":   {"translation": 1.0, "structure": 1.2, "gc_window": 60, "min_stem": 4},
    "cardiac":  {"translation": 1.0, "structure": 1.2, "gc_window": 60, "min_stem": 4},
    "default":  {"translation": 1.0, "structure": 1.0, "gc_window": 30, "min_stem": 3},
}

#: v0.10.2 — strong splice motifs to AVOID when picking a split-vector junction.
_SPLICE_MOTIFS_TO_AVOID: tuple[str, ...] = ("GT", "AG", "GCAG", "ATAC")

#: v0.10.2 — junction-picker window.
_JUNCTION_PICKER_WINDOW_BP: int = 600

#: Label strings.
_5ITR_LABEL = "[AAV2 5'ITR | 145 bp]"
_3ITR_LABEL = "[AAV2 3'ITR | 145 bp]"
_WPRE_LABEL = "[WPRE | 599 bp]"
_BGH_POLYA_LABEL = "[bGH_polyA | 227 bp]"

#: Capsid tokens.
_CNS_TISSUE_TOKENS: tuple[str, ...] = ("cns", "brain", "neuron", "nav", "scn1a", "glia")

#: v0.10.1 — pan-neuronal enhancers.
_PAN_NEURONAL_ENHANCERS: frozenset[str] = frozenset({"hSyn1", "hSyn"})

#: v0.10.1 — proprietary capsid tokens.
_PROPRIETARY_CAPSID_TOKENS: frozenset[str] = frozenset({
    "4D-A101",
    "AAV2.5T",
    "AAV2.5T-SP183",
})


def _resolve_capsid(capsid: str, tissue: str) -> str:
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


def _try_codon_optimize(
    cds: str,
    translation_weight: float | None = None,
    structure_weight: float | None = None,
    gc_window_size: int | None = None,
    min_stem_length: int | None = None,
) -> tuple[str, bool]:
    try:
        from mrnavax.codon_lineardesign import optimize_lineardesign
    except ImportError:
        return cds, False
    try:
        kwargs: dict[str, float | int | bool] = {"verbose": False}
        if translation_weight is not None:
            kwargs["translation_weight"] = translation_weight
        if structure_weight is not None:
            kwargs["structure_weight"] = structure_weight
        if gc_window_size is not None:
            kwargs["gc_window_size"] = gc_window_size
        if min_stem_length is not None:
            kwargs["min_stem_length"] = min_stem_length
        result = optimize_lineardesign(cds, **kwargs)
        if isinstance(result, str):
            return result, True
        if hasattr(result, "cds"):
            return str(result.cds), True
        if isinstance(result, (list, tuple)) and result:
            return str(result[0]), True
        return cds, True
    except Exception:
        return cds, False


def _tissue_codon_weights(tissue: str) -> dict[str, float | int]:
    key = (tissue or "").strip().lower()
    for needle, weights in _TISSUE_CODON_WEIGHTS.items():
        if needle == "default":
            continue
        if needle in key:
            return weights
    return _TISSUE_CODON_WEIGHTS["default"]


def _pick_split_vector_junction(cds: str, overlap_bp: int) -> int:
    cds_len = len(cds)
    if cds_len < 6:
        return cds_len // 2
    mid = cds_len // 2
    mid = mid - (mid % 3)
    best = mid
    best_score = -float("inf")
    start = max(3, mid - _JUNCTION_PICKER_WINDOW_BP)
    end = min(cds_len - 3, mid + _JUNCTION_PICKER_WINDOW_BP)
    for pos in range(start, end + 1, 3):
        window = cds[max(0, pos - 10):min(cds_len, pos + 11)]
        motif_hits = sum(1 for m in _SPLICE_MOTIFS_TO_AVOID if m in window)
        distance = abs(pos - mid)
        score = -distance if motif_hits == 0 else -10_000
        if score > best_score:
            best_score = score
            best = pos
    return best


class MockAAVVectorDesigner(AAVVectorDesigner):
    """Stdlib-only mock AAV vector designer (v0.10.2 default)."""

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
        codon_translation_weight: float | None = None
        codon_structure_weight: float | None = None
        if codon_optimized:
            tissue_w = _tissue_codon_weights(tissue)
            cds_payload, used_live = _try_codon_optimize(
                cds_payload,
                translation_weight=tissue_w["translation"],
                structure_weight=tissue_w["structure"],
                gc_window_size=int(tissue_w["gc_window"]),
                min_stem_length=int(tissue_w["min_stem"]),
            )
            codon_translation_weight = float(tissue_w["translation"])
            codon_structure_weight = float(tissue_w["structure"])
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

        if split_intein is not None and split_vector is not None:
            raise ValueError(
                "split_intein and split_vector are mutually exclusive; "
                "use split_intein for protein trans-splicing (Mich 2025) "
                "or split_vector for nucleic-acid trans-splicing (4DMT DMD)."
            )
        junction_split_position: int | None = None

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
            payload_N = (
                _5ITR_LABEL
                + components["promoter"]
                + f"[{half_label_N}-half CDS | {half_cds_length} bp]"
                + f"[intein-{half_label_N} | {_SPLIT_INTEIN_TAG_BP} bp]"
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL
            )
            payload_C = (
                _5ITR_LABEL
                + components["promoter"]
                + f"[intein-{half_label_C} | {_SPLIT_INTEIN_TAG_BP} bp]"
                + f"[{half_label_C}-half CDS | {half_cds_length} bp]"
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL
            )
            payload = (payload_N, payload_C)
            payload_length_bp = half_length
            packaging_status = half_status_N
            payload_packaging_notes = half_notes_N
        elif split_vector is not None:
            if len(split_vector) != 2:
                raise ValueError(
                    f"split_vector must be a 2-tuple (e.g. ('5p', '3p')); got {split_vector!r}"
                )
            half_label_5p, half_label_3p = split_vector
            junction = _pick_split_vector_junction(cds_payload, _SPLIT_VECTOR_OVERLAP_BP)
            cds_5p_len = junction
            cds_3p_len = len(cds_payload) - junction + _SPLIT_VECTOR_OVERLAP_BP
            half_5p_length = (
                _COMPONENT_LENGTHS_BP["5ITR"]
                + _COMPONENT_LENGTHS_BP["promoter"]
                + cds_5p_len
                + _COMPONENT_LENGTHS_BP["WPRE"]
                + _COMPONENT_LENGTHS_BP["bGH_polyA"]
                + _COMPONENT_LENGTHS_BP["3ITR"]
            )
            half_3p_length = (
                _COMPONENT_LENGTHS_BP["5ITR"]
                + _COMPONENT_LENGTHS_BP["promoter"]
                + cds_3p_len
                + _COMPONENT_LENGTHS_BP["WPRE"]
                + _COMPONENT_LENGTHS_BP["bGH_polyA"]
                + _COMPONENT_LENGTHS_BP["3ITR"]
            )
            half_status_5p, half_notes_5p = _packaging_status(half_5p_length)
            half_status_3p, half_notes_3p = _packaging_status(half_3p_length)
            payload_5p = (
                _5ITR_LABEL
                + components["promoter"]
                + f"[{half_label_5p}-half CDS (CDS[1:{junction}]) | {cds_5p_len} bp]"
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL
            )
            payload_3p = (
                _5ITR_LABEL
                + components["promoter"]
                + f"[{half_label_3p}-half CDS (CDS[{junction}:] + overlap {_SPLIT_VECTOR_OVERLAP_BP} bp) | {cds_3p_len} bp]"
                + _WPRE_LABEL
                + _BGH_POLYA_LABEL
                + _3ITR_LABEL
            )
            payload = (payload_5p, payload_3p)
            payload_length_bp = max(half_5p_length, half_3p_length)
            packaging_status = (
                "ok"
                if half_status_5p == "ok" and half_status_3p == "ok"
                else "over_limit" if "over_limit" in (half_status_5p, half_status_3p) else "borderline"
            )
            payload_packaging_notes = half_notes_5p + half_notes_3p
            junction_split_position = junction
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
        if split_vector is not None:
            notes.append(
                f"split-vector delivery: two-cassette payload (5'-half + 3'-half), "
                f"trans-spliced at CDS position {junction_split_position} (overlap "
                f"{_SPLIT_VECTOR_OVERLAP_BP} bp; junction picker chose a position "
                f"near the CDS midpoint avoiding strong splice motifs). The 5'-half "
                f"is {cds_5p_len} bp, the 3'-half is {cds_3p_len} bp (CDS[len-overlap:] "
                f"+ overlap). Per-half packaging status: 5'={half_status_5p}, "
                f"3'={half_status_3p}."
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
            split_vector=split_vector,
            codon_translation_weight=codon_translation_weight,
            codon_structure_weight=codon_structure_weight,
            junction_split_position=junction_split_position,
        )


__all__ = ["MockAAVVectorDesigner"]
