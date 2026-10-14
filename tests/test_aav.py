"""Tests for the v0.10 ``mrnavax_rare.aav`` subsystem.

Coverage
--------

- Public surface (imports, public types, public functions).
- ``capsid_for_tissue`` dispatch (lung / liver / cns / unknown / None).
- ``MockAAVVectorDesigner`` happy path (default auto-resolution, explicit
  capsid, explicit promoter, HGVS-C variant application, payload length
  accounting, packaging status dispatch).
- ``design_aav`` entry point (mock / live / auto).
- Negative paths (unknown capsid, unknown promoter, empty target_gene,
  empty cds_wildtype, unparseable HGVS-C).
- The ``AAVVectorDesigner`` protocol is ``runtime_checkable``.
"""

from __future__ import annotations

import pytest

from mrnavax_rare.aav import (
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
    AAVVectorDesigner,
    PackagingStatus,
    capsid_for_tissue,
    design_aav,
)
from mrnavax_rare.aav.adapters.live_aav import LiveAAVVectorDesigner
from mrnavax_rare.aav.adapters.mock_aav import MockAAVVectorDesigner


#: Short CFTR NBD1 fragment (real DNA not required — the mock adapter is
#: structural; payload length comes from len() of the input CDS).
SHORT_CDS = "ATGCAGCTGTTGCAAGCAGCATCAGCAAGCTGCTGAAGCAGCTGCAAGCAGCAG" * 4  # 216 bp


# -----------------------------------------------------------------------------
# Public surface
# -----------------------------------------------------------------------------


def test_public_imports_resolve():
    """All public symbols importable from the package root."""
    assert design_aav is not None
    assert isinstance(AAV_CAPSIDS, tuple)
    assert len(AAV_CAPSIDS) == 4
    assert isinstance(AAV_PROMOTERS, tuple)
    assert AAV_PACKAGING_CEILING_BP == 4700
    assert AAV_PACKAGING_BORDERLINE_MARGIN_BP == 200


def test_aavspec_is_frozen_dataclass():
    """AAVSpec is a frozen dataclass — mutating raises."""
    spec = design_aav(
        target_gene="CFTR",
        cds_wildtype=SHORT_CDS,
        tissue="lung",
    )
    with pytest.raises(Exception):
        spec.target_gene = "OTC"  # type: ignore[misc]


def test_aavectordesigner_is_runtime_checkable():
    """AAVVectorDesigner protocol is runtime_checkable (duck typing)."""
    assert isinstance(MockAAVVectorDesigner(), AAVVectorDesigner)
    assert isinstance(LiveAAVVectorDesigner(), AAVVectorDesigner)


# -----------------------------------------------------------------------------
# capsid_for_tissue dispatch
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "tissue,expected",
    [
        ("lung", AAV5),
        ("Lung", AAV5),  # case-insensitive
        ("airway epithelium", AAV5),
        ("CFTR airway", AAV5),
        ("liver", AAV8),
        ("hepatocytes", AAV8),
        ("cns", AAV9),
        ("brain", AAV9),
        ("scn1a", AAV9),
        ("muscle", AAV9),
        ("cardiac", AAV9),
        ("rh10", AAVRH10),
    ],
)
def test_capsid_for_tissue_dispatch(tissue, expected):
    assert capsid_for_tissue(tissue) == expected


def test_capsid_for_tissue_unknown_returns_none():
    assert capsid_for_tissue("unknown_tissue_xyz") is None
    assert capsid_for_tissue("") is None


# -----------------------------------------------------------------------------
# MockAAVVectorDesigner happy paths
# -----------------------------------------------------------------------------


def test_mock_default_auto_lung_cftr():
    """CFTR + lung auto-resolves to AAV5 + CAG."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype=SHORT_CDS,
        tissue="lung",
    )
    assert isinstance(spec, AAVSpec)
    assert spec.target_gene == "CFTR"
    assert spec.capsid == AAV5
    assert spec.promoter == "CAG"
    assert spec.hgvs_c_applied == ""
    assert spec.cds_payload == spec.cds_wildtype
    assert "lung_epithelium" in spec.tropism_tags


def test_mock_default_auto_liver_otc():
    """OTC + liver auto-resolves to AAV8 + CAG."""
    spec = MockAAVVectorDesigner().design(
        target_gene="OTC",
        cds_wildtype=SHORT_CDS,
        tissue="liver",
    )
    assert spec.capsid == AAV8
    assert spec.promoter == "CAG"
    assert "hepatocytes_high" in spec.tropism_tags


def test_mock_default_auto_cns_scn1a_uses_hsyn():
    """SCN1A + CNS auto-resolves to AAV9 + hSyn (Dravet path)."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=SHORT_CDS,
        tissue="cns",
    )
    assert spec.capsid == AAV9
    assert spec.promoter == "hSyn"
    assert "cns_neurons" in spec.tropism_tags


def test_mock_explicit_capsid_and_promoter():
    """Explicit capsid / promoter overrides auto-resolution."""
    spec = MockAAVVectorDesigner().design(
        target_gene="OTC",
        cds_wildtype=SHORT_CDS,
        capsid="AAV9",
        promoter="TBG",
        tissue="liver",  # would normally pick AAV8
    )
    assert spec.capsid == AAV9
    assert spec.promoter == "TBG"


def test_mock_unknown_tissue_falls_back_to_aav9():
    """Unknown tissue falls back to AAV9 (safest default)."""
    spec = MockAAVVectorDesigner().design(
        target_gene="XYZ",
        cds_wildtype=SHORT_CDS,
        tissue="tissue_unknown_xyz",
    )
    assert spec.capsid == AAV9


def test_mock_applies_hgvs_c_variant():
    """HGVS-C variant is applied to the wildtype CDS via variant_injector."""
    # Build a CDS where position 1 is G — easy to assert.
    cds = "G" + "ATGCAGCTGTGCAAACAGTGCAAACAGTGCAAACAGTGCAAACAGTGCAAACAGTGC" * 2
    assert cds[0] == "G"  # position 1 (1-based) is G
    # c.1G>T — substitute the 1st base (G) with T.
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype=cds,
        hgvs_c="c.1G>T",
        tissue="lung",
    )
    assert spec.hgvs_c_applied == "c.1G>T"
    assert spec.cds_payload != spec.cds_wildtype
    assert spec.cds_payload[0] == "T"
    assert spec.cds_wildtype[0] == "G"
    assert any("applied HGVS-C variant" in n for n in spec.notes)


def test_mock_payload_components_include_all_canonical_keys():
    """payload_components includes 5ITR / promoter / CDS / WPRE / bGH_polyA / 3ITR."""
    spec = design_aav(target_gene="CFTR", cds_wildtype=SHORT_CDS, tissue="lung")
    keys = set(spec.payload_components.keys())
    assert keys == {"5ITR", "promoter", "CDS", "WPRE", "bGH_polyA", "3ITR"}
    assert spec.payload_components["CDS"] == SHORT_CDS


def test_mock_payload_length_accounting():
    """payload_length_bp = 145 + 0 + CDS + 599 + 227 + 145 = CDS + 1116."""
    spec = design_aav(target_gene="CFTR", cds_wildtype=SHORT_CDS, tissue="lung")
    expected_length = len(SHORT_CDS) + 145 + 599 + 227 + 145
    assert spec.payload_length_bp == expected_length


def test_mock_packaging_status_ok_for_short_cds():
    """Short CDS yields 'ok' status with no notes."""
    spec = design_aav(target_gene="CFTR", cds_wildtype=SHORT_CDS, tissue="lung")
    assert spec.packaging_status == "ok"
    assert spec.notes == ()


def test_mock_packaging_status_borderline():
    """CDS that brings payload within 200 bp of 4700 ceiling → 'borderline'."""
    # Need payload > 4500 bp (4700 - 200) → CDS > 4500 - 1116 = 3384 bp
    borderline_cds = "A" * 3500
    spec = design_aav(target_gene="CFTR", cds_wildtype=borderline_cds, tissue="lung")
    assert spec.packaging_status == "borderline"
    assert any("approaches AAV packaging ceiling" in n for n in spec.notes)


def test_mock_packaging_status_over_limit():
    """CDS that brings payload over 4700 bp → 'over_limit'."""
    over_cds = "A" * 4500  # 4500 + 1116 = 5616 > 4700
    spec = design_aav(target_gene="CFTR", cds_wildtype=over_cds, tissue="lung")
    assert spec.packaging_status == "over_limit"
    assert any("exceeds AAV packaging ceiling" in n for n in spec.notes)


# -----------------------------------------------------------------------------
# design_aav entry point
# -----------------------------------------------------------------------------


def test_design_aav_auto_defaults_to_mock():
    """design_aav(backend='auto') returns the mock output."""
    spec = design_aav(target_gene="CFTR", cds_wildtype=SHORT_CDS, tissue="lung")
    assert isinstance(spec, AAVSpec)
    assert spec.capsid == AAV5


def test_design_aav_explicit_mock():
    """design_aav(backend='mock') returns the mock output."""
    spec = design_aav(
        target_gene="OTC",
        cds_wildtype=SHORT_CDS,
        tissue="liver",
        backend="mock",
    )
    assert spec.capsid == AAV8


def test_design_aav_live_raises_not_implemented():
    """design_aav(backend='live') raises NotImplementedError (v0.10 stub)."""
    with pytest.raises(NotImplementedError):
        design_aav(
            target_gene="CFTR",
            cds_wildtype=SHORT_CDS,
            backend="live",
        )


def test_design_aav_unknown_backend_raises():
    """Unknown backend token raises ValueError."""
    with pytest.raises(ValueError, match="Unknown AAV backend"):
        design_aav(
            target_gene="CFTR",
            cds_wildtype=SHORT_CDS,
            backend="does_not_exist",
        )


# -----------------------------------------------------------------------------
# Negative paths
# -----------------------------------------------------------------------------


def test_unknown_capsid_raises():
    """Unknown capsid token raises ValueError."""
    with pytest.raises(ValueError, match="Unknown capsid"):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype=SHORT_CDS,
            capsid="AAV99",
        )


def test_unknown_promoter_raises():
    """Unknown promoter token raises ValueError."""
    with pytest.raises(ValueError, match="Unknown promoter"):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype=SHORT_CDS,
            promoter="BAD_PROMOTER",
        )


def test_empty_target_gene_raises():
    """Empty target_gene raises ValueError."""
    with pytest.raises(ValueError, match="target_gene"):
        MockAAVVectorDesigner().design(
            target_gene="",
            cds_wildtype=SHORT_CDS,
        )


def test_empty_cds_raises():
    """Empty cds_wildtype raises ValueError."""
    with pytest.raises(ValueError, match="cds_wildtype"):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype="",
        )


def test_unparseable_hgvs_c_propagates_value_error():
    """Unparseable HGVS-C string raises ValueError from variant_injector."""
    with pytest.raises(ValueError):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype=SHORT_CDS,
            hgvs_c="c.not_a_valid_hgvs_string",
        )


def test_hgvs_c_ref_mismatch_propagates_value_error():
    """HGVS-C with wrong ref base raises ValueError from variant_injector."""
    # c.1A>T — SHORT_CDS[0] is 'A' (good); but use a CDS where position 1 is G.
    cds = "G" + "A" * 200  # position 1 is G, not A
    with pytest.raises(ValueError):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype=cds,
            hgvs_c="c.1A>T",
        )


# -----------------------------------------------------------------------------
# Sanity anchors
# -----------------------------------------------------------------------------


def test_all_four_capsids_have_tropism_tags():
    """Every capsid in AAV_CAPSIDS has at least one tropism tag."""
    for capsid in AAV_CAPSIDS:
        tags = AAV_CAPSID_TROPISM.get(capsid, ())
        assert len(tags) > 0, f"capsid {capsid} has no tropism tags"


def test_packaging_status_is_string_literal():
    """PackagingStatus is a plain string union (JSON-friendly)."""
    spec = design_aav(target_gene="CFTR", cds_wildtype=SHORT_CDS, tissue="lung")
    assert isinstance(spec.packaging_status, str)
    assert spec.packaging_status in ("ok", "borderline", "over_limit")
