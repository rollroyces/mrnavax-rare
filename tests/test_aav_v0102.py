"""Tests for the v0.10.2 ``mrnavax_rare.aav`` extensions."""

from __future__ import annotations

import pytest

from mrnavax_rare.aav import design_aav
from mrnavax_rare.aav.adapters.mock_aav import (
    MockAAVVectorDesigner,
    _pick_split_vector_junction,
    _tissue_codon_weights,
)


DMD_LIKE_CDS = "ATG" * 2000  # 6,000 nt


def test_split_vector_emits_two_payloads():
    spec = MockAAVVectorDesigner().design(
        target_gene="DMD",
        cds_wildtype=DMD_LIKE_CDS,
        tissue="muscle",
        split_vector=("5p", "3p"),
    )
    assert spec.split_vector == ("5p", "3p")
    assert isinstance(spec.payload, tuple)
    assert len(spec.payload) == 2
    assert spec.junction_split_position is not None
    assert spec.junction_split_position % 3 == 0
    assert 2_500 <= spec.junction_split_position <= 3_500


def test_split_vector_per_half_length_under_ceiling():
    spec = MockAAVVectorDesigner().design(
        target_gene="DMD",
        cds_wildtype=DMD_LIKE_CDS,
        tissue="muscle",
        split_vector=("5p", "3p"),
    )
    assert spec.payload_length_bp < 4_700
    assert spec.packaging_status in ("ok", "borderline")


def test_split_vector_mutual_exclusion_with_split_intein():
    with pytest.raises(ValueError, match="mutually exclusive"):
        MockAAVVectorDesigner().design(
            target_gene="DMD",
            cds_wildtype=DMD_LIKE_CDS,
            split_intein=("N", "C"),
            split_vector=("5p", "3p"),
        )


def test_split_vector_invalid_tuple_raises():
    with pytest.raises(ValueError, match="split_vector must be a 2-tuple"):
        MockAAVVectorDesigner().design(
            target_gene="DMD",
            cds_wildtype=DMD_LIKE_CDS,
            split_vector=("5p",),
        )


def test_split_vector_note_emitted():
    spec = MockAAVVectorDesigner().design(
        target_gene="DMD",
        cds_wildtype=DMD_LIKE_CDS,
        tissue="muscle",
        split_vector=("5p", "3p"),
    )
    assert any("split-vector delivery" in n for n in spec.notes)
    assert any(f"CDS position {spec.junction_split_position}" in n for n in spec.notes)
    assert any("overlap 500 bp" in n for n in spec.notes)


def test_junction_picker_returns_codon_boundary():
    cds = "A" * 6_000
    for _ in range(10):
        pos = _pick_split_vector_junction(cds, overlap_bp=500)
        assert pos % 3 == 0
        assert 0 < pos < len(cds)


def test_junction_picker_avoids_canonical_splice_motifs():
    cds = "A" * 3_000 + "GT" + "A" * 3_000
    pos = _pick_split_vector_junction(cds, overlap_bp=500)
    assert not (2_990 <= pos <= 3_010)


def test_junction_picker_handles_short_cds():
    cds = "ATGAAATAA"
    pos = _pick_split_vector_junction(cds, overlap_bp=500)
    assert pos >= 0


def test_tissue_codon_weights_liver_balanced():
    w = _tissue_codon_weights("liver")
    assert w["translation"] == 1.0
    assert w["structure"] == 1.0


def test_tissue_codon_weights_cns_biases_structure():
    w = _tissue_codon_weights("cns")
    assert w["translation"] < 1.0
    assert w["structure"] > 1.0


def test_tissue_codon_weights_lung_extends_gc_window():
    w_liver = _tissue_codon_weights("liver")
    w_lung = _tissue_codon_weights("lung")
    assert w_lung["gc_window"] > w_liver["gc_window"]


def test_tissue_codon_weights_unknown_falls_back_to_default():
    w = _tissue_codon_weights("unknown_tissue_xyz")
    assert w["translation"] == 1.0
    assert w["structure"] == 1.0


def test_codon_optimized_records_tissue_weights_in_spec():
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="cns",
        codon_optimized=True,
    )
    assert spec.codon_translation_weight is not None
    assert spec.codon_structure_weight is not None
    assert spec.codon_translation_weight < 1.0
    assert spec.codon_structure_weight > 1.0


def test_codon_optimized_false_records_no_weights():
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="liver",
    )
    assert spec.codon_translation_weight is None
    assert spec.codon_structure_weight is None


def test_design_aav_passes_split_vector_kwarg():
    spec = design_aav(
        target_gene="DMD",
        cds_wildtype=DMD_LIKE_CDS,
        tissue="muscle",
        split_vector=("5p", "3p"),
    )
    assert spec.split_vector == ("5p", "3p")
    assert spec.junction_split_position is not None


def test_design_aav_passes_codon_optimized_with_tissue():
    spec = design_aav(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="cns",
        codon_optimized=True,
    )
    assert spec.codon_optimized is True
    assert spec.codon_translation_weight < 1.0
    assert spec.codon_structure_weight > 1.0
