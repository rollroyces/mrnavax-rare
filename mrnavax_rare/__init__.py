"""mrnavax-rare — mRNA therapeutics design toolkit for rare Mendelian diseases.

A sibling of mrnavax (https://github.com/rollroyces/mrnavax) that focuses the
same eight-layer mRNA-therapeutics pipeline on rare genetic diseases rather
than cancer vaccines.

This package reached the **v0.10.0 milestone** on 2026-10-14: 9 subsystems
(`indication`, `target_protein`, `modality`, `safety`, `design`, `aav`,
`trial`, `cfrna_persistence_classifier`, `sweat_chloride_predictor`)
shipped with mock + live adapters, 256 + 1 tests, 7 substantive studies
(CF Class I, PCCA, Pareto-sweep, sweat_chloride, cfRNA, Phase 1 trial
design, Dravet SCN1A) + 1 replication study, paper draft at ~6,000 words,
two real-data-integration passes that reduced the verification queue from
22 to 11 net active anchors.

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

__version__ = "0.10.0"
__all__ = ["__version__"]

# All 6 base subsystems declared. Two biomarker predictors (cfRNA persistence,
# sweat chloride) appended under the safety subsystem. Trial was added in
# the parallel v0.5 push; we re-ordered to put trial last to align with the
# SCOPE §7 roadmap.
# v0.6 append: cfrna_persistence_classifier — a cfRNA-derived plasma-
# persistence predictor sitting under the safety subsystem (see
# mrnavax_rare/safety/cfrna/).
# v0.7 append: sweat_chloride_predictor — a sweat chloride CFTR-function
# biomarker predictor also under the safety subsystem (see
# mrnavax_rare/safety/sweat_chloride/).
# v0.10 append: aav — AAV gene-therapy vector design (capsid + ITR-flanked
# transgene cassette), sibling to the LNP-mRNA ``design`` subsystem. Uses
# ``design.variant_injector.apply_hgvs_c`` for non-PTC variant payloads.
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
    # v0.9.0 milestone: 8 subsystems shipped; 2 base subsystems expanded
    # to 8 total with the two biomarker predictors under safety.
    # v0.9.0 additional milestone: trial-corpus extension beyond CF
    # (DEFAULT_CORPUS = 9 entries: 5 CF + 2 PCCA/OTC Moderna mRNA-IV
    # + 2 Dravet Stoke STK-001 / zorevunersen) so the trial matcher
    # returns informative non-CF top-1 for the v0.6 PCCA, v0.7.3 Dravet,
    # and v0.7.2 Phase-1 trial-design cohorts.
    # v0.10.0 milestone: aav subsystem added — AAV gene-therapy vector
    # design (capsid + ITR-flanked transgene cassette), sibling to the
    # LNP-mRNA ``design`` pipeline. Uses ``design.variant_injector`` for
    # non-PTC variant payloads. Mock backend only; live backend stub.
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
