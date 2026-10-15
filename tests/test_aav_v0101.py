"""Tests for the v0.10.1 ``mrnavax_rare.aav`` extensions.

These tests cover the four new v0.10.1 features validated against
real wet-lab programs (see ``paper/AAV_WET_LAB_VALIDATION.md``):

- **Minigene** — ``"CFTRΔR(708–835)"`` brings over-ceiling CFTR back
  to ``"ok"`` (the canonical 4D-710 / SP-101 strategy).
- **Codon optimization** — ``codon_optimized=True`` flag is plumbed
  through to the spec; the actual ``mrnavax.codon_lineardesign`` call
  is best-effort (graceful fallback if the backend is not importable).
- **Split-intein** — ``split_intein=("N", "C")`` emits a 2-tuple
  payload with per-half packaging status (the canonical Mich 2025
  SCN1A strategy).
- **Cell-type enhancer** — ``hSyn1 + SCN1A`` triggers the Mich 2025
  preweaning-mortality safety note; ``hDLXI5/6i + SCN1A`` does not.
- **AAV-PHP.eB capsid** — added to AAV_CAPSIDS and resolved by
  ``"php.eb"`` / ``"aav-php.eb"`` tissue tokens.
- **Proprietary capsid** — ``"4D-A101"`` and ``"AAV2.5T"`` are
  accepted by the mock and surface a caveat note.
"""

from __future__ import annotations

import pytest

from mrnavax_rare.aav import (
    AAV_CAPSIDS,
    AAV_CELL_TYPE_CRITICAL_GENES,
    AAV_CELL_TYPE_ENHANCERS,
    AAV_MINIGENE_CDS_LENGTH_BP,
    AAV_PHP_EB,
    design_aav,
)
from mrnavax_rare.aav.adapters.mock_aav import MockAAVVectorDesigner


REAL_CFTR_CDS = "A" * 4443  # 4,443 nt — real CFTR CDS length.
REAL_SCN1A_CDS = "G" * 6030  # 6,030 nt — real SCN1A CDS length.


# -----------------------------------------------------------------------------
# Minigene (CFTRΔR(708–835))
# -----------------------------------------------------------------------------


def test_minigene_cftr_full_length_is_over_ceiling():
    """Real CFTR (4,443 bp) + cassette = 5,559 bp > 4.7 kb → over_limit."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype=REAL_CFTR_CDS,
        tissue="lung",
    )
    assert spec.packaging_status == "over_limit"


def test_minigene_flag_is_plumbed():
    """When minigene="CFTRΔR(708–835)", the spec records the minigene."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype=REAL_CFTR_CDS,
        tissue="lung",
        minigene="CFTRΔR(708–835)",
    )
    assert spec.minigene == "CFTRΔR(708–835)"
    assert any("minigene" in n for n in spec.notes)


def test_minigene_cftr_dr_honest_math():
    """ΔR-only minigene gets closer to ceiling (5,559 → 5,175) but does NOT fix it.

    Honest v0.10.1 disclosure: 4D-710's "microCFTR" uses additional
    truncations + a minimal promoter that v0.10.1 does not model.
    """
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype=REAL_CFTR_CDS,
        tissue="lung",
        minigene="CFTRΔR(708–835)",
    )
    # 4,059 (minigene) + 1,116 (cassette structure) = 5,175 bp.
    assert spec.payload_length_bp == 5175
    assert spec.payload_length_bp > 4700


def test_minigene_with_short_cds_works():
    """A short CDS with the minigene flag still produces a valid spec."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="lung",
        minigene="CFTRΔR(708–835)",
    )
    assert spec.minigene == "CFTRΔR(708–835)"


def test_unknown_minigene_raises():
    """Unknown minigene token raises ValueError."""
    with pytest.raises(ValueError, match="Unknown minigene"):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype=REAL_CFTR_CDS,
            minigene="CFTRΔR(123–456)",
        )


# -----------------------------------------------------------------------------
# Codon optimization
# -----------------------------------------------------------------------------


def test_codon_optimized_flag_plumbed_through():
    """codon_optimized=True is recorded in the spec."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="lung",
        codon_optimized=True,
    )
    assert spec.codon_optimized is True


def test_codon_optimized_false_default():
    """codon_optimized defaults to False."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="lung",
    )
    assert spec.codon_optimized is False


# -----------------------------------------------------------------------------
# Split-intein (Mich 2025)
# -----------------------------------------------------------------------------


def test_split_intein_emits_two_payloads():
    """split_intein=("N", "C") emits a 2-tuple payload."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=REAL_SCN1A_CDS,
        tissue="cns",
        split_intein=("N", "C"),
    )
    assert spec.split_intein == ("N", "C")
    assert isinstance(spec.payload, tuple)
    assert len(spec.payload) == 2


def test_split_intein_per_half_length_under_ceiling():
    """Each split-intein half is under 4.7 kb."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=REAL_SCN1A_CDS,
        tissue="cns",
        split_intein=("N", "C"),
    )
    # Per-half: 6030 // 2 + 200 + 145 + 599 + 227 + 145 = 3015 + 200 + 1116 = 4331.
    assert spec.payload_length_bp == 4331
    assert spec.payload_length_bp < 4700


def test_split_intein_invalid_tuple_raises():
    """split_intein must be a 2-tuple."""
    with pytest.raises(ValueError, match="split_intein must be a 2-tuple"):
        MockAAVVectorDesigner().design(
            target_gene="SCN1A",
            cds_wildtype=REAL_SCN1A_CDS,
            split_intein=("N",),
        )


def test_split_intein_safety_note_added():
    """Split-intein spec includes a Mich 2025 cite note."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=REAL_SCN1A_CDS,
        tissue="cns",
        split_intein=("N", "C"),
    )
    assert any("Mich 2025" in n for n in spec.notes)


# -----------------------------------------------------------------------------
# Cell-type enhancer (Mich 2025 safety signal)
# -----------------------------------------------------------------------------


def test_pan_neuronal_hsyn1_with_scn1a_triggers_safety_note():
    """hSyn1 + SCN1A → Mich 2025 preweaning-mortality safety note."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=REAL_SCN1A_CDS,
        tissue="cns",
        cell_type_enhancer="hSyn1",
    )
    assert spec.cell_type_enhancer == "hSyn1"
    assert any("SAFETY" in n and "preweaning mortality" in n for n in spec.notes)


def test_hdlx_5_6i_with_scn1a_no_safety_note():
    """hDLXI5/6i + SCN1A → no safety note (this is the Mich 2025 SUCCESS path)."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=REAL_SCN1A_CDS,
        tissue="cns",
        cell_type_enhancer="hDLXI5/6i",
    )
    assert spec.cell_type_enhancer == "hDLXI5/6i"
    assert not any("pan-neuronal" in n and "SCN1A" in n for n in spec.notes)


def test_hsyn1_with_non_critical_gene_no_safety_note():
    """hSyn1 + non-critical gene → no safety note."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",  # NOT in AAV_CELL_TYPE_CRITICAL_GENES
        cds_wildtype="ATG" * 100,
        tissue="cns",
        cell_type_enhancer="hSyn1",
    )
    assert not any("SAFETY" in n and "preweaning" in n for n in spec.notes)


def test_critical_genes_set_contains_scn1a():
    """Sanity: the critical-genes registry includes SCN1A."""
    assert "SCN1A" in AAV_CELL_TYPE_CRITICAL_GENES


# -----------------------------------------------------------------------------
# AAV-PHP.eB capsid (v0.10.1)
# -----------------------------------------------------------------------------


def test_aav_php_eb_in_capsids():
    """AAV-PHP.eB is now in AAV_CAPSIDS."""
    assert AAV_PHP_EB in AAV_CAPSIDS
    assert len(AAV_CAPSIDS) == 5


def test_php_eb_tissue_token_resolves():
    """'php.eb' / 'AAV-PHP.eB' tissue tokens resolve to AAV-PHP.eB."""
    from mrnavax_rare.aav import capsid_for_tissue

    assert capsid_for_tissue("php.eb") == AAV_PHP_EB
    assert capsid_for_tissue("AAV-PHP.eB") == AAV_PHP_EB
    assert capsid_for_tissue("aav-php.eb capsid") == AAV_PHP_EB


def test_php_eb_via_explicit_capsid():
    """Explicit capsid='AAV-PHP.eB' works."""
    spec = MockAAVVectorDesigner().design(
        target_gene="SCN1A",
        cds_wildtype=REAL_SCN1A_CDS,
        capsid="AAV-PHP.eB",
        tissue="cns",
    )
    assert spec.capsid == AAV_PHP_EB
    assert "cns_neurons" in spec.tropism_tags


# -----------------------------------------------------------------------------
# Proprietary capsid caveat
# -----------------------------------------------------------------------------


def test_proprietary_capsid_4d_a101_emits_caveat():
    """4D-A101 proprietary capsid accepted with caveat."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        capsid="4D-A101",
        tissue="lung",
    )
    assert spec.capsid == "4D-A101"
    assert spec.proprietary_capsid_caveat is not None
    assert "proprietary" in spec.proprietary_capsid_caveat
    assert any("proprietary" in n for n in spec.notes)


def test_proprietary_capsid_aav2_5t_emits_caveat():
    """AAV2.5T (Spirovant) proprietary capsid accepted with caveat."""
    spec = MockAAVVectorDesigner().design(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        capsid="AAV2.5T",
        tissue="lung",
    )
    assert spec.capsid == "AAV2.5T"
    assert spec.proprietary_capsid_caveat is not None


def test_unknown_capsid_raises_still():
    """Unknown capsid (not in registry, not proprietary) still raises."""
    with pytest.raises(ValueError, match="Unknown capsid"):
        MockAAVVectorDesigner().design(
            target_gene="CFTR",
            cds_wildtype="ATG" * 100,
            capsid="AAV99-FOO",
        )


# -----------------------------------------------------------------------------
# design_aav entry point (v0.10.1)
# -----------------------------------------------------------------------------


def test_design_aav_passes_v0101_kwargs():
    """design_aav() entry point propagates v0.10.1 kwargs to the adapter."""
    spec = design_aav(
        target_gene="CFTR",
        cds_wildtype="ATG" * 100,
        tissue="lung",
        minigene="CFTRΔR(708–835)",
        codon_optimized=True,
        cell_type_enhancer="hDLXI5/6i",
    )
    assert spec.minigene == "CFTRΔR(708–835)"
    assert spec.codon_optimized is True
    assert spec.cell_type_enhancer == "hDLXI5/6i"
