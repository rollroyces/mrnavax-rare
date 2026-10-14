"""Frozen dataclasses for the ``aav`` subsystem (v0.10).

The ``aav`` subsystem composes an AAV gene-therapy vector design — capsid +
ITR-flanked transgene cassette — for a target gene + variant. It is the
v0.10 deliverable and is the sibling subsystem to ``mrnavax_rare.design``
(which handles LNP-mRNA constructs). Public output is an :class:`AAVSpec`.

Scope (v0.10)
-------------

- **Capsid** — :data:`AAV_CAPSIDS` enumerates the four v0.10 capsids
  (AAV5 / AAV8 / AAV9 / AAVrh10) with their canonical tissue tropism.
- **Transgene cassette** — ``5'ITR + promoter + variant-injected CDS + WPRE +
  bGH_polyA + 3'ITR``. The variant-injected CDS uses
  :func:`mrnavax_rare.design.variant_injector.apply_hgvs_c`.
- **Tropism dispatch** — :func:`capsid_for_tissue` picks a capsid from a
  free-text tissue / cell-type token (e.g. ``"lung"``, ``"liver"``,
  ``"cns"``).
- **Packaging check** — :attr:`AAVSpec.packaging_status` flags the cassette
  length against the canonical ~4.7 kb AAV packaging ceiling.

What is NOT in v0.10
--------------------

- No codon optimization — the CDS is passed through unchanged after
  variant injection (codon optimization for AAV is mechanistically
  meaningful but out of scope for the v0.10 scaffold).
- No capsid engineering — wildtype capsids only.
- No split-vector / dual-AAV packaging strategies — single AAV cassette
  only, with a ``"over_limit"`` status when the CDS is too long.
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

#: Canonical set of v0.10 capsid IDs.
AAV_CAPSIDS: tuple[str, ...] = (AAV5, AAV8, AAV9, AAVRH10)

#: Per-capsid tissue tropism tags.
AAV_CAPSID_TROPISM: dict[str, tuple[str, ...]] = {
    AAV5: ("lung_epithelium", "retinal_pigment_epithelium", "hepatocytes_low"),
    AAV8: ("hepatocytes_high", "skeletal_muscle", "cardiac_myocytes"),
    AAV9: ("cardiac_myocytes", "skeletal_muscle", "cns_neurons", "glia"),
    AAVRH10: ("cns_neurons", "glia", "hepatocytes_low"),
}

#: Canonical ~4.7 kb AAV packaging ceiling.
AAV_PACKAGING_CEILING_BP: int = 4700

#: Borderline margin — cassettes within this many bases of the ceiling are
#: flagged ``"borderline"`` rather than ``"ok"``.
AAV_PACKAGING_BORDERLINE_MARGIN_BP: int = 200

#: Tissue → capsid dispatch table (v0.10).
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
)

#: Canonical promoter choices (v0.10).
AAV_PROMOTERS: tuple[str, ...] = ("CAG", "EF1a", "hSyn", "TBG", "mPGK")


def capsid_for_tissue(tissue: str) -> str | None:
    """Return the v0.10 capsid for a free-text tissue token, or ``None``."""
    if not tissue:
        return None
    key = tissue.strip().lower()
    for needle, capsid in _TISSUE_TO_CAPSID:
        if needle in key:
            return capsid
    return None


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
    payload: str
    payload_components: Mapping[str, str]
    payload_length_bp: int
    packaging_status: PackagingStatus
    tropism_tags: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)


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
    "PackagingStatus",
    "capsid_for_tissue",
]
