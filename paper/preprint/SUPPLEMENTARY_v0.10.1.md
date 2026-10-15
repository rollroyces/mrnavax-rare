# Supplementary materials — `mrnavax-rare v0.10.1` preprint

## S1. Full per-section manuscript files

The manuscript body in `PREPRINT_v0.10.1.md` is a continuous-prose version. The per-section source files for v0.7.4 (which still anchor the v0.10.1 manuscript) are in the main `paper/` directory:

- `paper/ABSTRACT.md` — abstract (verbatim)
- `paper/INTRODUCTION.md` — introduction (verbatim)
- `paper/METHODS.md` — methods (verbatim)
- `paper/RESULTS.md` — v0.5–v0.9.0 results (verbatim; the v0.10 / v0.10.1 results are in the new manuscript)
- `paper/DISCUSSION.md` — discussion (verbatim)
- `paper/REFERENCES.md` — references (re-flowed to numbered list)
- `paper/TITLE.md` — title candidates (primary used in `PREPRINT_v0.10.1.md`)

## S2. v0.10.1 wet-lab validation synthesis

- `paper/AAV_WET_LAB_VALIDATION.md` (13.3 KB) — the cross-program synthesis that anchors the v0.10.1 §3.3 results. Covers 4D-710 (NCT05248230), SP-101 (Spirovant), DLX2.0-SCN1A (Mich 2025 *Sci Transl Med* 17:eadn5603), and VX-522 (NCT05668741, discontinued). Documents 4 structural gaps the v0.10 mock had and the v0.10.1 extensions that close them.

## S3. v0.9 design-space synthesis paper

- `paper/DESIGN_SPACE_TOPOLOGY.md` (227 lines) — the v0.9 forward-looking synthesis paper that motivated the v0.10 work.

## S4. Toolkit modules

- `mrnavax_rare/__init__.py` — package root; `SUBSYSTEMS = (indication, target_protein, modality, safety, design, aav, trial, cfrna_persistence_classifier, sweat_chloride_predictor)`. `__version__ = "0.10.1"`.
- `mrnavax_rare/aav/__init__.py` — `design_aav()` entry point.
- `mrnavax_rare/aav/data_types.py` — `AAVSpec` frozen dataclass + capsid / promoter / minigene / cell-type-enhancer constants.
- `mrnavax_rare/aav/protocol.py` — `AAVVectorDesigner` runtime-checkable protocol.
- `mrnavax_rare/aav/adapters/mock_aav.py` — `MockAAVVectorDesigner` (v0.10.1 default; stdlib-only; never raises ImportError).
- `mrnavax_rare/aav/adapters/live_aav.py` — `LiveAAVVectorDesigner` (`NotImplementedError` stub; reserved for a future integration with an open viral-vector design tool).
- `mrnavax_rare/design/variant_injector.py` — v0.8 HGVS-C variant injector (substitution, insertion, deletion, delins). Used by both `design` (LNP-mRNA) and `aav` (AAV).
- `mrnavax_rare/safety/cfrna/classifier.py` — v0.6 cfRNA persistence classifier; output is consumed by the sister toolkit `deepcatch-methylation` v0.10.0 (`deepcatch_methylation.cfrna_coupling.couple_cfrna_to_cdm`).

## S5. Studies and result CSVs

| Study | Anchor | CSV / artefact |
|---|---|---|
| CF Class I nonsense cohort | v0.5 | `studies/class_i_pcs/results.csv` (12 variants) |
| PCCA / PCCB propionic acidemia | v0.6 | `studies/pa_pcs/results.csv` (12 variants) |
| Pareto sweep (LinearDesign vs alternatives) | v0.7.1 | `studies/pareto_full_cftr/interpretation.md` |
| Sweat chloride response | v0.7.1 | `studies/sweat_chloride_response/results.csv` |
| cfRNA persistence | v0.7.4 | `studies/cfrna_persistence/results.csv` |
| Dravet SCN1A | v0.7.3 | `studies/dravet_scn1a/results.csv` |
| Phase 1 trial design | v0.7.2 | `studies/phase1_trial_design/PROTOCOL.md` + `cohort.csv` |
| Replication study | v0.7.4 | `studies/replication_study/results.csv` |
| v0.7.4 real-data integration | v0.7.4 | `studies/v0_7_4_realdata_integration/TODO.md` (audit of 22 → 11 anchors) |

The one-command pipeline reproduction is:

```bash
bash studies/phase1_trial_design/REPRODUCE.sh
```

## S6. Tests

`tests/test_aav.py` (39 tests, v0.10.0) + `tests/test_aav_v0101.py` (23 tests, v0.10.1) + the 11 per-subsystem test files. **279 + 1 skipped (TDC), 0 regressions** at v0.10.1.

## S7. Honest-disclosure inventory

Every v0.10.1 honest-disclosure item is preserved in the manuscript §4.5, `CHANGELOG.md` v0.10.1, and `paper/AAV_WET_LAB_VALIDATION.md` §6. Summary:

- No new wet-lab evidence produced by mrnavax-rare.
- The ΔR minigene alone doesn't fix CFTR over-ceiling (5,175 > 4,700 nt).
- The proprietary capsid gap is real (4D-A101, AAV2.5T not publicly available).
- VX-522's discontinuation is a caution, not a refutation.
- hSyn1-induced mortality in DS mice is a critical safety signal.
- The honest-controls gate is the toolkit's central methodological commitment.

## S8. Source-of-truth chain

```
paper/AAV_WET_LAB_VALIDATION.md   ← v0.10.1 cross-program synthesis
paper/DESIGN_SPACE_TOPOLOGY.md   ← v0.9 forward-looking synthesis
paper/PAPER.md                   ← v0.7.4 canonical concatenation
paper/ABSTRACT.md                ← abstract
paper/INTRODUCTION.md            ← introduction
paper/METHODS.md                 ← methods
paper/RESULTS.md                 ← v0.5–v0.9.0 results
paper/DISCUSSION.md              ← discussion
paper/REFERENCES.md              ← references
mrnavax_rare/                    ← package source
tests/                           ← test suite
studies/<variant>/results.csv    ← case-study data
studies/phase1_trial_design/     ← pipeline + reproduction

        ↓ (formatting pass + v0.10.1 synthesis)

paper/preprint/PREPRINT_v0.10.1.md        ← bioRxiv distributable (this preprint)
paper/preprint/COVER_LETTER_v0.10.1.md    ← editorial cover letter
paper/preprint/SUPPLEMENTARY_v0.10.1.md   ← this file
```

---

*Prepared 2026-10-15 from the v0.10.1 source toolkit and v0.7.4 per-section source files.*
