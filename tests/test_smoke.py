"""Smoke test — confirm the skeleton imports + integrity checks pass.

CI runs this on Python 3.11–3.14 without any heavy dependencies.
"""

from __future__ import annotations

import mrnavax_rare
from mrnavax_rare.backends import (
    CHECKS,
    CheckResult,
    check_all,
    check_all_summary,
)
from mrnavax_rare import SUBSYSTEMS


def test_version_is_string():
    assert isinstance(mrnavax_rare.__version__, str)
    assert mrnavax_rare.__version__ == "0.10.0"


def test_get_version_matches_dunder():
    assert mrnavax_rare.get_version() == mrnavax_rare.__version__


def test_subsystems_declared():
    status = mrnavax_rare.skeleton_status()
    assert "indication" in status["subsystems_declared"]
    assert "target_protein" in status["subsystems_declared"]
    assert "modality" in status["subsystems_declared"]
    assert "safety" in status["subsystems_declared"]
    assert "design" in status["subsystems_declared"]
    assert "trial" in status["subsystems_declared"]
    # v0.6: cfRNA persistence classifier added as a 7th subsystem.
    assert "cfrna_persistence_classifier" in status["subsystems_declared"]
    assert status["is_skeleton"] is False  # v0.5 milestone shipped
    assert SUBSYSTEMS == (
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


def test_backends_registry_is_a_list():
    assert isinstance(CHECKS, list)
    assert len(CHECKS) >= 1  # the self-check is always registered


def test_check_all_runs():
    results = check_all()
    assert isinstance(results, list)
    assert all(isinstance(r, CheckResult) for r in results)


def test_check_all_summary_passes_at_least_one():
    passed, total, failures = check_all_summary()
    assert total >= 1
    assert passed >= 1
    assert failures == [] or all(r.detail for r in failures)


def test_skeleton_self_check_passes():
    from mrnavax_rare.backends import skeleton_self_check

    r = skeleton_self_check()
    assert isinstance(r, CheckResult)
    assert r.ok is True
    assert r.family == "skeleton"


def test_subsystem_list_is_consistent_v05():
    """All 6 (v0.5) + 1 (v0.6) subsystems declared and implemented.

    Locks in the v0.5 milestone (6 subsystems) and the v0.6 addition
    (``cfrna_persistence_classifier``). When this test fails, a
    subsystem was declared but not implemented (or vice versa).
    """
    from mrnavax_rare import SUBSYSTEMS, skeleton_status

    declared = set(SUBSYSTEMS)
    implemented = set(skeleton_status()["subsystems_implemented"])
    assert declared == implemented, (
        f"declared/declared mismatch: declared={declared}, implemented={implemented}"
    )
    # All six expected in v0.5, plus the v0.6 cfRNA classifier.
    expected_v05 = (
        "indication",
        "target_protein",
        "modality",
        "safety",
        "design",
        "trial",
    )
    for s in expected_v05:
        assert s in declared, f"{s} missing from SUBSYSTEMS"
    # v0.6 addition.
    assert "cfrna_persistence_classifier" in declared, (
        "v0.6: cfrna_persistence_classifier missing from SUBSYSTEMS"
    )
    assert "cfrna_persistence_classifier" in implemented, (
        "v0.6: cfrna_persistence_classifier missing from subsystems_implemented"
    )
    # v0.10 addition.
    assert "aav" in declared, (
        "v0.10: aav missing from SUBSYSTEMS"
    )
    assert "aav" in implemented, (
        "v0.10: aav missing from subsystems_implemented"
    )


def test_skeleton_status_flipped_to_false():
    """v0.5 milestone: is_skeleton flips to False when all 6 shipped.

    v0.7.4 update: the version assertion is updated to the current milestone
    state (8 subsystems, 2 biomarkers appended). The is_skeleton check still
    locks in the v0.5 milestone's structural flip.
    v0.10.0 update: 9 subsystems shipped (aav added).
    """
    s = mrnavax_rare.skeleton_status()
    assert s["is_skeleton"] is False, "skeleton_status should be False at v0.10.0"
    assert s["version"] == "0.10.0"
