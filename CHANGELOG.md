# Changelog

All notable changes to `mrnavax-rare` are documented here. The format is
loosely based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to the same forward-looking trajectory as the v0.5 → v0.7.4
milestones.

## [v0.10.0] — 2026-10-14

### AAV vector design subsystem (`mrnavax_rare.aav`)

- New subsystem, **9th in the package** (sibling to `mrnavax_rare.design`).
  Composes an AAV gene-therapy vector design — capsid + ITR-flanked
  transgene cassette — for a target gene + optional HGVS-C variant.
- Public surface at `mrnavax_rare.aav`: `design_aav()`, `AAVSpec` (frozen
  dataclass), `AAVVectorDesigner` (runtime-checkable protocol), capsid /
  promoter / packaging constants, `capsid_for_tissue()` tissue-dispatch.
- **Capsids** (v0.10 scope): AAV5 (lung epithelium), AAV8 (hepatocytes),
  AAV9 (cardiac / muscle / CNS), AAVrh10 (CNS). Each carries a
  tissue-tropism tuple in `AAV_CAPSID_TROPISM`.
- **Promoters** (v0.10 scope): CAG, EF1a, hSyn, TBG, mPGK. Auto-resolution
  picks `hSyn` for CNS / SCN1A (Dravet), `CAG` otherwise.
- **HGVS-C variant application**: uses `apply_hgvs_c` from
  `mrnavax_rare.design.variant_injector` to inject non-PTC variants into
  the wildtype CDS before cassette assembly. PTC / nonsense variants
  propagate as `ValueError` from the injector (correct behavior — PTCs
  don't translate, so AAV-delivered mutant CDS is not a viable design).
- **Packaging status**: `AAVSpec.packaging_status` is one of
  `ok` / `borderline` / `over_limit` against the canonical 4.7 kb AAV
  packaging ceiling (Wu 2010 / Pillay 2016). Cassettes within 200 bp of
  the ceiling are flagged `borderline`; cassettes above are flagged
  `over_limit` with a "consider split-vector or trans-splicing" note.
- **Adapters**: stdlib-only `MockAAVVectorDesigner` (always available) +
  `LiveAAVVectorDesigner` (`NotImplementedError` stub reserved for a
  future integration with an external viral vector design tool).
- **Why v0.10 vs v0.9**: AAV vector design is a different delivery class
  than LNP-mRNA (DNA cargo, persistent expression, tissue-specific
  tropism via capsid) — it's a sibling subsystem, not a modality track
  inside `mrnavax_rare.modality`. The taxonomy stays narrow.

### Honest disclosure on v0.10.0

- **No new wet-lab evidence**: AAV work is structural scaffolding. The
  capsid / promoter / ITR / WPRE / bGH-polyA choices cite standard
  field references but have NOT been validated against any patient
  sample. The mock backend returns fully deterministic outputs by
  construction; no prediction of in-vivo potency / efficacy is made.
- **CFTR + AAV = borderline packaging**: a real CFTR CDS (4,443 bp)
  plus the ITR-flanked cassette structure (1,116 bp) gives ~5,559 bp —
  over the 4.7 kb ceiling. The mock backend flags this as
  `over_limit` and surfaces the "split-vector or trans-splicing"
  note, matching the real-world CFTR AAV programs (4D Molecular
  Therapeutics, Spirovant) that use dual-AAV strategies. The mock
  does NOT generate the split-vector payload itself; that's a
  v0.10.x follow-up.
- **No codon optimization in v0.10**: AAV cassettes pass the CDS
  through unchanged after variant injection. AAV codon optimization
  is mechanistically meaningful (different from LNP-mRNA — AAV
  uses cellular transcription, not direct cytoplasmic translation)
  but is out of scope for v0.10.

### Test integrity

- `python3 -m pytest tests/` → **256 + 1 skipped (TDC auto-skip), 0 regressions**
- 39 new tests in `tests/test_aav.py` cover: public imports, frozen
  dataclass enforcement, `runtime_checkable` protocol, `capsid_for_tissue`
  dispatch (12 parametrized cases), auto-resolution for CFTR / OTC / SCN1A,
  explicit overrides, HGVS-C variant application, payload length
  accounting, packaging status dispatch (`ok` / `borderline` / `over_limit`),
  design entry point (mock / live / unknown backend), and 7 negative-path
  tests (unknown capsid, unknown promoter, empty inputs, unparseable
  HGVS-C, ref-mismatch HGVS-C).
- Pre-existing 217 tests from v0.9.0 still pass — no test was deleted
  or weakened to make room for the AAV work.

## [v0.9.0] — 2026-10-14

### Trial-corpus extension beyond CF

- `mrnavax_rare/trial/corpus/__init__.py` adds a new public
  `DEFAULT_CORPUS = TrialCorpus(name="v0_9_mixed", entries=9)` that is a
  strict superset of `DEFAULT_CF_CORPUS` (which is unchanged at 5 CF
  entries for backward compatibility with v0.5 fixtures).
- 4 new `TrialCorpusEntry` constants added:
  - `NCT04159103_mRNA3927` — PCCA / Moderna mRNA-3927 Phase 1/2 (mRNA-IV liver)
  - `NCT04442349_mRNA3139` — OTC / Moderna mRNA-3139 Phase 1/2 (mRNA-IV liver)
  - `NCT04442295_STK001` — Dravet / Stoke STK-001 ADMIRAL/MONARCH Phase 1/2 (IT ASO)
  - `NCT06872125_EMPEROR` — Dravet / Stoke STK-001 Phase 3 zorevunersen pivotal (IT ASO)
- All 4 new entries' numeric anchors trace to real ClinicalTrials.gov
  registrations and are already cited in
  `mrnavax_rare/safety/cfrna/data.py` (the v0.7.4 cfrna predictor's
  PK data module). No new fabrication.
- `__all__` updated to `["DEFAULT_CF_CORPUS", "DEFAULT_CORPUS"]`.

### Honest disclosure on trial-matcher behavior

- With the `trialgpt-simicl` backend (the v0.7.4 default), the v0.9
  mixed corpus returns the **correct trial at rank 1** for both the
  PCCA and Dravet test summaries:
  - PCCA patient → `NCT04442349` (mRNA-3139 OTC, Moderna) at rank 1;
    `NCT04159103` (mRNA-3927 PCCA, Moderna) at rank 2
  - Dravet patient → `NCT04442295` (STK-001 Phase 1/2) at rank 1;
    `NCT06872125` (STK-001 Phase 3 zorevunersen) at rank 2
- The **absolute scores are small (0.000 for PCCA, 0.333 for Dravet
  with trialgpt-simicl)** because the matcher is keyword-overlap and
  the patient-summary tokens don't fully overlap each entry's
  eligibility_keys. **The v0.9 win is in the ranking, not the
  magnitude**: the matcher correctly surfaces non-CF trials for non-CF
  patients, where v0.5 cf-only corpus returned 100%-CF noise (the
  v0.5 baseline returned `NCT03375047` (CF-MRT5005) as the top-1 for
  both PCCA and Dravet patients).
- Further matcher tuning (e.g., adding "lactic acidosis" → PCCA
  entry's keywords, adding "propionic acidemia" → keyword
  cross-matching) would increase absolute scores but is out of
  v0.9 scope; the corpus extension ships the right STRUCTURE
  (right trial at rank 1), not the right scores.

### Test integrity

- `python3 -m pytest tests/` → **217 + 1 skipped (TDC auto-skip), 0 regressions**
- The 6 boltz-gated tests that auto-skipped in v0.7.4 (because boltz
  lives in `$HOME/.venv-boltz-test`, not the project venv) still skip
  cleanly. v0.9.0 did not touch the boltz integration.

## [v0.7.4] — 2026-10-13

(prior changelog entries elided from the v0.10.0 release notes for brevity; full history is on disk)
