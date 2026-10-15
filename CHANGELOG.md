# Changelog

All notable changes to `mrnavax-rare` are documented here. The format is
loosely based on [Keep a Changelog](https://keepachangelog.com/), and this
project adheres to the same forward-looking trajectory as the v0.5 → v0.7.4
milestones.

## [v0.10.1] — 2026-10-15

### AAV wet-lab validation sweep — v0.10.1 closes the real-world gaps

The v0.10 release shipped a structural `MockAAVVectorDesigner` with
honest-disclosure notes about its gaps. v0.10.1 closes four of those
gaps with evidence-anchored extensions, validated against four
real published programs (see `paper/AAV_WET_LAB_VALIDATION.md` for the
full cross-program synthesis):

- **4D-710** (4D Molecular Therapeutics, NCT05248230) — Phase 1/2 in
  CF, uses 4D-A101 capsid + codon-optimized CFTRΔR minigene
- **SP-101 / SPIRO-2101** (Spirovant Sciences) — SAAVe Phase 1/2 in
  CF, uses AAV2.5T capsid + fCFTRΔR + doxorubicin enhancer
- **DLX2.0-SCN1A** (Allen Institute + Seattle Children's, Mich
  et al. 2025 *Sci Transl Med* 17:eadn5603) — dual-AAV split-intein
  + hDLXI5/6i GABAergic-interneuron enhancer for Dravet
- **VX-522** (Vertex / Moderna, NCT05668741) — **DISCONTINUED May 2025**
  due to LNP-induced lung inflammation. The v0.10 `design` (LNP-mRNA)
  CF lung path is at clinical risk; the v0.10.1 `aav` subsystem is the
  more promising frontier.

### What's new in v0.10.1

- **Minigene support** — `AAVSpec.minigene` selects a published
  truncation strategy. v0.10.1 ships `CFTRΔR(708–835)` (4D-710 / SP-101).
  Honest disclosure: the ΔR-only truncation gets full-length CFTR
  closer to the ceiling (5,559 → 5,175 bp) but does NOT bring it under
  4.7 kb; 4DMT's "microCFTR" uses additional truncations + a minimal
  promoter that v0.10.1 does not yet model.
- **Codon optimization** — `AAVSpec.codon_optimized` (bool) wires the
  CDS through `mrnavax.codon_lineardesign.optimize_lineardesign` if
  the backend is available. Graceful fallback if the backend is not
  importable — the flag stays `True` and a note is added (no silent
  fallback to unoptimized).
- **Split-intein delivery** — `AAVSpec.split_intein` (2-tuple) emits
  a two-cassette payload (N-half + C-half) for very large genes like
  SCN1A. Each half is sized to fit under 4.7 kb (e.g. SCN1A 6,030 bp
  / 2 + 200 bp intein tag = 3,215 bp CDS per half + 1,116 bp cassette
  structure = 4,331 bp per half).
- **Cell-type enhancer** — `AAVSpec.cell_type_enhancer` records a
  cell-type-specific tag (e.g. `hDLXI5/6i` for GABAergic
  interneurons). A **safety note is added when a pan-neuronal
  enhancer (e.g. `hSyn1`) is paired with SCN1A** — Mich 2025
  documented dose-dependent preweaning mortality with hSyn1-SCN1A in
  DS mice.
- **AAV-PHP.eB capsid** — added to `AAV_CAPSIDS` (the first
  non-wildtype capsid; publicly available via MTA from Caltech, used
  in the Mich 2025 SCN1A program).
- **Proprietary capsid support** — `MockAAVVectorDesigner` recognizes
  `4D-A101` (4DMT) and `AAV2.5T` (Spirovant) and emits a caveat note
  documenting the proprietary / not-in-public-registry gap.

### Honest disclosure on v0.10.1

- **No new wet-lab evidence produced by mrnavax-rare.** The 279 + 1
  tests are unit tests of structural scaffolding, not in-vitro /
  in-vivo validation. The wet-lab evidence cited in
  `paper/AAV_WET_LAB_VALIDATION.md` §2 is from published peer-
  reviewed papers and ClinicalTrials.gov records.
- **Proprietary capsid gap is real.** 4DMT 4D-A101 and Spirovant
  AAV2.5T are not publicly available. The mock emits structural
  specs for them but does NOT validate tropism / packaging / safety
  against the developers' published data. v0.10.1 documents the gap;
  it does not solve it.
- **VX-522's discontinuation is a caution, not a refutation.** The
  LNP-mRNA CF lung delivery failed in the clinic. This is strong
  evidence that AAV is the more promising CF lung therapeutic
  modality. It does NOT mean LNP-mRNA is dead for CF or for other
  indications.
- **hSyn1-induced mortality in the Mich 2025 paper is a critical
  safety signal.** Any AIDD pipeline that recommends a pan-neuronal
  SCN1A promoter is recommending something with published lethality
  in DS mice. The v0.10.1 safety note is non-negotiable.

### Test integrity

- `python3 -m pytest tests/` → **279 + 1 skipped (TDC auto-skip), 0 regressions**
- 23 new tests in `tests/test_aav_v0101.py` cover: minigene math +
  error path, codon-optimization flag plumbing + graceful fallback,
  split-intein two-payload emission + per-half ceiling check, hSyn1 +
  SCN1A safety note, hDLXI5/6i + SCN1A non-safety, AAV-PHP.eB capsid +
  tissue dispatch, proprietary-capsid caveat emission.
- Pre-existing 256 tests from v0.10.0 still pass — no test was deleted
  or weakened to make room for v0.10.1.

## [v0.10.0] — 2026-10-14
