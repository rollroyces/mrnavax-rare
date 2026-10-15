"""mrnavax-rare — mRNA therapeutics design toolkit for rare Mendelian diseases.

A sibling of mrnavax (https://github.com/rollroyces/mrnavax) that focuses the
same eight-layer mRNA-therapeutics pipeline on rare genetic diseases rather
than cancer vaccines.

This package reached the **v0.10.1 milestone** on 2026-10-15: 9 subsystems
(`indication`, `target_protein`, `modality`, `safety`, `design`, `aav`,
`trial`, `cfrna_persistence_classifier`, `sweat_chloride_predictor`)
shipped with mock + live adapters, 279 + 1 tests, 7 substantive studies
(CF Class I, PCCA, Pareto-sweep, sweat_chloride, cfRNA, Phase 1 trial
design, Dravet SCN1A) + 1 replication study, paper draft at ~6,000 words,
two real-data-integration passes that reduced the verification queue from
22 to 11 net active anchors, and a wet-lab validation sweep against
4D-710 / SP-101 / DLX2.0-SCN1A / VX-522 published programs (see
`paper/AAV_WET_LAB_VALIDATION.md`).

Public surface:

    from mrnavax_rare import indication, target_protein, modality, safety, design, trial
    from mrnavax_rare.aav import design_aav
    from mrnavax_rare.safety import score as safety_score
    from mrnavax_rare.safety.cfrna import predict_cfrna_persistence
    from mrnavax_rare.safety.sweat_chloride import predict_sweat_chloride_response
    from mrnavax_rare.trial import match_trials
    from mrnavax_rare.design.variant_injector import apply_hgvs_c

Backend-adapter convention mirrors mrnavax:

    - stdlib-only mock backend always present
    - real backend opt-in via `[extra]` dependency
    - structural integrity check via deterministic assertions
    - `mrnavax_rare.backends --check-all` to verify
"""

from __future__ import annotations

__version__ = "0.10.1"
__all__ = ["__version__"]

SUBSYSTEMS = (
    "indication",
    "target_protein",
    "modality",
    "safety",
    "design",
    "aav",
    "trial",
    "cfrna_persistence_classifier",
    "sweat_chloride_predictor",
)


def get_version() -> str:
    """Return the package version string (helper for tooling)."""
    return __version__


def skeleton_status() -> dict:
    """Return the current skeleton status as a dict."""
    implemented = [
        "indication",
        "target_protein",
        "modality",
        "safety",
        "design",
        "aav",
        "trial",
        "cfrna_persistence_classifier",
        "sweat_chloride_predictor",
    ]
    return {
        "version": __version__,
        "subsystems_declared": list(SUBSYSTEMS),
        "subsystems_implemented": implemented,
        "is_skeleton": False,
    }
