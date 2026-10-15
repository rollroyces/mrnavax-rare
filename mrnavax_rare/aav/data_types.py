"""Frozen dataclasses for the ``aav`` subsystem (v0.10.1).

The ``aav`` subsystem composes an AAV gene-therapy vector design — capsid +
ITR-flanked transgene cassette — for a target gene + variant. It is the
v0.10 deliverable and is the sibling subsystem to ``mrnavax_rare.design``
(which handles LNP-mRNA constructs). Public output is an :class:`AAVSpec`.

Scope (v0.10.1, validated against wet-lab programs in
``paper/AAV_WET_LAB_VALIDATION.md``)
--------------------------------------

- **Capsid** — :data:`AAV_CAPSIDS` enumerates the five v0.10.1 capsids
  (AAV5 / AAV8 / AAV9 / AAVrh10 / AAV-PHP.eB) with their canonical
  tissue tropism. AAV-PHP.eB is the first **non-wildtype** capsid in
  the registry — it is the publicly-available engineered variant
  developed by the Gradinaru lab (Chan et al. 2017 *Nat Neurosci*,
  20:1172–1179) and used in the Allen Institute Dravet SCN1A program
  (Mich et al. 2025 *Sci Transl Med* 17:eadn5603).
- **Transgene cassette** — ``5'ITR + promoter + variant-injected CDS +
  WPRE + bGH_polyA + 3'ITR``. The variant-injected CDS uses
  :func:`mrnavax_rare.design.variant_injector.apply_hgvs_c`.
- **Tropism dispatch** — :func:`capsid_for_tissue` picks a capsid from a
  free-text tissue / cell-type token (e.g. ``"lung"``, ``"liver"``,
  ``"cns"``).
- **Packaging check** — :attr:`AAVSpec.packaging_status` flags the
  cassette length against the canonical ~4.7 kb AAV packaging ceiling.
- **Minigene** (v0.10.1) — :attr:`AAVSpec.minigene` selects a published
  truncation strategy when the wildtype CDS exceeds the ceiling. The
  canonical v0.10.1 minigene is ``"CFTRΔR(708–835)"`` (4D-710 / SP-101).
- **Codon optimization** (v0.10.1) — :attr:`AAVSpec.codon_optimized` is a
  bool flag indicating whether the CDS was passed through a codon
  optimizer (mirrors the LNP-mRNA ``design`` subsystem's
  ``mrnavax.codon_lineardesign.optimize_lineardesign`` backend).
- **Split-intein** (v0.10.1) — :attr:`AAVSpec.split_intein` is a
  2-tuple ``("N", "C")`` indicating the cassette has been split into
  two halves with intein tags for protein trans-splicing (Mich 2025).
  When set, :attr:`AAVSpec.payload` becomes a 2-tuple of cassettes and
  :attr:`AAVSpec.packaging_status` is computed per-half.
- **Cell-type enhancer** (v0.10.1) — :attr:`AAVSpec.cell_type_enhancer`
  records a cell-type-specific enhancer tag (e.g. ``"hDLXI5/6i"`` for
  GABAergic interneurons). A safety note is added when a pan-neuronal
  enhancer is paired with a known cell-type-specific gene (SCN1A).
- **Proprietary capsid gap** (v0.10.1 honest disclosure) — 4DMT's
  4D-A101 and Spirovant's AAV2.5T are NOT in :data:`AAV_CAPSIDS`
  because they are proprietary and not publicly available. The
  ``paper/AAV_WET_LAB_VALIDATION.md`` paper documents this gap.

What is NOT in v0.10.1
----------------------

- No real viral vector design tool integration (the ``Live`` adapter
  is still a :class:`NotImplementedError` stub).
- No split-vector / dual-AAV payload generation — the split-intein
  two-cassette emission is supported, but the per-half payload
  contents are the same structural shape as a single cassette.
- No manufacturing / CMC output — no titre, no purity, no GMP scale.
- No in-vivo potency / efficacy predictions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


#: Canonical AAV capsid identifiers.
AAV9 = "AAV9"
AAV8 = "AAV8"
AAV5 = "AAV5"
AAVRH10 = "AAVrh10"
AAV_PHP_EB = "AAV-PHP.eB"  # v0.10.1 — Gradinaru-lab engineered capsid

#: Canonical set of v0.10.1 capsid IDs.
AAV_CAPSIDS: tuple[str, ...] = (AAV5, AAV8, AAV9, AAVRH10, AAV_PHP_EB)

#: Per-capsid tissue tropism tags.
AAV_CAPSID_TROPISM: dict[str, tuple[str, ...]] = {
    AAV5: ("lung_epithelium", "retinal_pigment_epithelium", "hepatocytes_low"),
    AAV8: ("hepatocytes_high", "skeletal_muscle", "cardiac_myocytes"),
    AAV9: ("cardiac_myocytes", "skeletal_muscle", "cns_neurons", "glia"),
    AAVRH10: ("cns_neurons", "glia", "hepatocytes_low"),
    # v0.10.1: PHP.eB is a CNS-tropic engineered variant of AAV9.
    AAV_PHP_EB: (
        "cns_neurons",
        "glia",
        "broad_cns_tropism",
        "research_use_only_luaad_seronegative_required",
    ),
}

#: Canonical ~4.7 kb AAV packaging ceiling.
AAV_PACKAGING_CEILING_BP: int = 4700

#: Borderline margin — cassettes within this many bases of the ceiling are
#: flagged ``"borderline"`` rather than ``"ok"``.
AAV_PACKAGING_BORDERLINE_MARGIN_BP: int = 200

#: Tissue → capsid dispatch table (v0.10.1).
_TISSUE_TO_CAPSID: tuple[tuple[str, str], ...] = (
    ("lung", AAV5),
    ("airway", AAV5),
    ("cf", AAV5),
    ("liver", AAV8),
    ("hepatocyte", AAV8),
    ("hepatic", AAV8),
    ("cns", AAV9),
    ("brain", AAV9),
    ("neuron", AAV9),
    ("nav", AAV9),
    ("scn1a", AAV9),
    ("muscle", AAV9),
    ("cardiac", AAV9),
    ("heart", AAV9),
    ("rh10", AAVRH10),
    ("glia", AAVRH10),
    # v0.10.1: PHP.eB for explicit CNS / AAV-PHP.eB tissue tokens.
    ("php.eb", AAV_PHP_EB),
    ("aav-php.eb", AAV_PHP_EB),
)

#: Canonical promoter choices (v0.10.1).
AAV_PROMOTERS: tuple[str, ...] = ("CAG", "EF1a", "hSyn", "TBG", "mPGK")

#: v0.10.1 — cell-type specific enhancers. The canonical v0.10.1 example
#: is ``hDLXI5/6i`` (GABAergic interneuron enhancer; Mich 2021 *Cell Rep*;
#: used by Mich 2025 in the Dravet SCN1A DLX2.0 construct).
AAV_CELL_TYPE_ENHANCERS: tuple[str, ...] = (
    "hDLXI5/6i",  # GABAergic telencephalic interneurons (Dravet)
    "mDLX5/6i",  # mouse version
    "hSyn1",  # pan-neuronal (CAUTION: Mich 2025 mortality signal for SCN1A)
    "CaMKIIa",  # excitatory neurons
)

#: v0.10.1 — published minigene truncation strategies. The keys are the
#: minigene identifiers (used in :attr:`AAVSpec.minigene`); the values
#: are the **CDS length in nucleotides** after truncation. These are
#: v0.10.1 structural defaults — see
#: ``paper/AAV_WET_LAB_VALIDATION.md`` §3.1 for the citation chain.
AAV_MINIGENE_CDS_LENGTH_BP: dict[str, int] = {
    # CFTR R-domain deletion (residues 708-835) — 4D-710 / SP-101.
    # Full-length CFTR = 4,443 nt; 128 aa × 3 nt/aa = 384 nt removed.
    "CFTRΔR(708–835)": 4443 - 384,  # = 4,059 nt
}

#: v0.10.1 — genes with known cell-type-specific safety requirements.
#: Pairing these with a pan-neuronal enhancer triggers a safety note.
#: The list is intentionally short — only genes with published cell-
#: type-specific safety signals are listed.
AAV_CELL_TYPE_CRITICAL_GENES: frozenset[str] = frozenset({
    "SCN1A",  # Mich 2025 — hSyn1 caused preweaning mortality
})


def capsid_for_tissue(tissue: str) -> str | None:
    """Return the v0.10.1 capsid for a free-text tissue token, or ``None``."""
    if not tissue:
        return None
    key = tissue.strip().lower()
    for needle, capsid in _TISSUE_TO_CAPSID:
        if needle in key:
            return capsid
    return None


def resolve_minigene_cds_length(target_gene: str, minigene: str | None) -> int | None:
    """Return the published minigene CDS length in nt, or ``None``."""
    if not minigene:
        return None
    return AAV_MINIGENE_CDS_LENGTH_BP.get(minigene)


#: Canonical payload status literal.
PackagingStatus = str  # "ok" | "borderline" | "over_limit"


@dataclass(frozen=True)
class AAVSpec:
    """Full AAV vector design spec for one ``(target_gene, variant)`` pair.

    v0.10.1 adds five fields relative to v0.10:
    :attr:`minigene`, :attr:`codon_optimized`, :attr:`split_intein`,
    :attr:`cell_type_enhancer`, and :attr:`proprietary_capsid_caveat`.
    All five are optional and default to ``None`` / ``False`` so the
    v0.10 API surface is preserved.
    """

    target_gene: str
    capsid: str
    promoter: str
    cds_wildtype: str
    cds_payload: str
    hgvs_c_applied: str
    payload: str | tuple[str, str]  # v0.10.1: tuple when split_intein is set
    payload_components: Mapping[str, str]
    payload_length_bp: int  # v0.10.1: per-half length when split_intein
    packaging_status: PackagingStatus  # v0.10.1: per-half when split_intein
    tropism_tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)
    # v0.10.1 — new fields:
    minigene: str | None = None
    codon_optimized: bool = False
    split_intein: tuple[str, str] | None = None
    cell_type_enhancer: str | None = None
    proprietary_capsid_caveat: str | None = None


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
    "PackagingStatus",
    "capsid_for_tissue",
    "resolve_minigene_cds_length",
]
