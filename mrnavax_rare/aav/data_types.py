"""Frozen dataclasses for the ``aav`` subsystem (v0.10.2).

The ``aav`` subsystem composes an AAV gene-therapy vector design — capsid +
ITR-flanked transgene cassette — for a target gene + variant. It is the
v0.10 deliverable and is the sibling subsystem to ``mrnavax_rare.design``
(which handles LNP-mRNA constructs). Public output is an :class:`AAVSpec`.

Scope (v0.10.2, validated against wet-lab programs in
``paper/AAV_WET_LAB_VALIDATION.md``)
--------------------------------------

v0.10.0 — adds the 9th subsystem (AAV); capsid / ITR / packaging status.
v0.10.1 — minigene (CFTRΔR(708–835)), codon_optimized, split_intein
(Mich 2025 DLX2.0-SCN1A), cell_type_enhancer (hDLXI5/6i for
GABAergic interneurons), AAV-PHP.eB capsid, proprietary
capsid caveat.
v0.10.2 — split_vector (trans-splicing overlap, the older dual-AAV
approach for very large genes like DMD); tissue-aware codon
optimization (CNS biases structure, lung biases stability,
liver balanced); junction picker for split_vector.

What is NOT in v0.10.2
----------------------

- No real viral vector design tool integration (the ``Live`` adapter
  is still a :class:`NotImplementedError` stub; see
  ``paper/AAV_LIVE_BACKEND_RESEARCH.md`` for the v0.10.2 honest
  finding that there is no public open viral-vector-design tool).
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
AAV_PHP_EB = "AAV-PHP.eB"

#: Canonical set of v0.10.2 capsid IDs.
AAV_CAPSIDS: tuple[str, ...] = (AAV5, AAV8, AAV9, AAVRH10, AAV_PHP_EB)

#: Per-capsid tissue tropism tags.
AAV_CAPSID_TROPISM: dict[str, tuple[str, ...]] = {
    AAV5: ("lung_epithelium", "retinal_pigment_epithelium", "hepatocytes_low"),
    AAV8: ("hepatocytes_high", "skeletal_muscle", "cardiac_myocytes"),
    AAV9: ("cardiac_myocytes", "skeletal_muscle", "cns_neurons", "glia"),
    AAVRH10: ("cns_neurons", "glia", "hepatocytes_low"),
    AAV_PHP_EB: (
        "cns_neurons",
        "glia",
        "broad_cns_tropism",
        "research_use_only_luaad_seronegative_required",
    ),
}

#: Canonical ~4.7 kb AAV packaging ceiling.
AAV_PACKAGING_CEILING_BP: int = 4700

#: Borderline margin.
AAV_PACKAGING_BORDERLINE_MARGIN_BP: int = 200

#: Tissue → capsid dispatch table (v0.10.2).
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
    ("php.eb", AAV_PHP_EB),
    ("aav-php.eb", AAV_PHP_EB),
)

#: Canonical promoter choices.
AAV_PROMOTERS: tuple[str, ...] = ("CAG", "EF1a", "hSyn", "TBG", "mPGK")

#: v0.10.1 — cell-type specific enhancers.
AAV_CELL_TYPE_ENHANCERS: tuple[str, ...] = (
    "hDLXI5/6i", "mDLX5/6i", "hSyn1", "CaMKIIa",
)

#: v0.10.1 — published minigene truncation strategies.
AAV_MINIGENE_CDS_LENGTH_BP: dict[str, int] = {
    "CFTRΔR(708–835)": 4443 - 384,  # = 4,059 nt
}

#: v0.10.1 — genes with known cell-type-specific safety requirements.
AAV_CELL_TYPE_CRITICAL_GENES: frozenset[str] = frozenset({
    "SCN1A",
})


def capsid_for_tissue(tissue: str) -> str | None:
    """Return the v0.10.2 capsid for a free-text tissue token, or ``None``."""
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
    """Full AAV vector design spec for one ``(target_gene, variant)`` pair."""

    target_gene: str
    capsid: str
    promoter: str
    cds_wildtype: str
    cds_payload: str
    hgvs_c_applied: str
    payload: str | tuple[str, str]  # v0.10.1: tuple when split_intein is set
    payload_components: Mapping[str, str]
    payload_length_bp: int
    packaging_status: PackagingStatus
    tropism_tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)
    # v0.10.1 fields
    minigene: str | None = None
    codon_optimized: bool = False
    split_intein: tuple[str, str] | None = None
    cell_type_enhancer: str | None = None
    proprietary_capsid_caveat: str | None = None
    # v0.10.2 fields
    split_vector: tuple[str, str] | None = None
    codon_translation_weight: float | None = None
    codon_structure_weight: float | None = None
    junction_split_position: int | None = None


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
