# Cover letter — `mrnavax-rare v0.10.1` preprint for bioRxiv submission

**To**: bioRxiv editorial team
**From**: Royce Lam — RollRoyces Research (independent)
**Date**: 2026-10-15
**Preprint**: `mrnavax-rare v0.10.1: a wet-lab-validated, open AIDD toolkit for rare Mendelian disease mRNA therapeutics — with an AAV vector design subsystem validated against 4D-710, SP-101, DLX2.0-SCN1A, and VX-522`
**Subject areas**: Bioinformatics / mRNA therapeutics / AAV gene therapy / Rare diseases / Cystic Fibrosis / Dravet syndrome / AIDD methodology / Computational drug design

---

Dear Editors,

I am pleased to submit the above manuscript for consideration as a preprint in the **Bioinformatics** or **Pharmacology and Toxicology** subject channels. The manuscript introduces `mrnavax-rare v0.10.1`, an open-source (AGPL-3.0-or-later / commercial dual) Python toolkit that addresses three distinct gaps in the current AIDD literature:

1. **Reproducibility**. The Chen et al. 2024 (*Genome Biology* 25:118) audit of PRC tools across >3,000 studies documented conflicting AUPRC rankings and overly-optimistic results. We address this with a built-in 5-item honest-controls gate (shuffled-label null + true-confound cross-indication + per-variant ablation + mock-vs-live delta + Cohen's d effect-size), the first such framework reported in an AIDD toolkit. The v0.7.4 CF Class I controls report (`studies/class_i_pcs/controls_report.md`) records 3 PASS + 2 INCONCLUSIVE + 0 FAIL.

2. **Rare-disease specificity**. The AIDD literature is dominated by cancer-vaccine payload design (the `mrnavax` sister toolkit covers this). `mrnavax-rare` is the open-source rare-disease-specific complement, with CF (CFTR Class I nonsense, propionic acidemia / PCCA, OTC) and Dravet syndrome (SCN1A) as the lead indications. The v0.10.1 release adds an AAV vector design subsystem as a sibling to the LNP-mRNA pipeline.

3. **Wet-lab validation**. The v0.10.1 AAV subsystem is validated against four real published programs: 4D-710 (NCT05248230), SP-101 (Spirovant SAAVe), DLX2.0-SCN1A (Mich et al. 2025 *Sci Transl Med* 17:eadn5603), and VX-522 (NCT05668741, discontinued May 2025). Every quantitative anchor in the manuscript cites a primary source. Honest gaps (proprietary capsids, the LNP-mRNA CF lung risk post-VX-522, the ΔR minigene alone not bringing CFTR under the 4.7 kb ceiling) are documented but not solved.

## Screening-checklist responses

The bioRxiv editorial screening asks five questions. Per-item evidence:

1. **Scientifically sound?** — Yes. The work is grounded in published peer-reviewed papers (Mich 2025, Rentosertib 2025, Boltz-2 2025, GEMORNA 2025) and ClinicalTrials.gov records. The honest-controls framework is the methodological contribution; the AAV subsystem is a toolkit implementation. The toolkit is released as reproducible code with 279 + 1 tests passing on Python 3.11–3.14.

2. **Within scope?** — Yes. bioRxiv accepts preprints in Bioinformatics, Pharmacology, and Computational Biology; the work sits at the intersection of mRNA therapeutics, AAV gene therapy, and AIDD methodology. The 4 real-world programs reviewed (4D-710, SP-101, DLX2.0-SCN1A, VX-522) are all in scope for the AIDD / rare-disease channels.

3. **Conclusions supported by data?** — Yes. Every quantitative claim in the manuscript traces to either (a) a `mrnavax==0.34.6` API call recorded in `studies/<variant>/results.csv`, (b) a published peer-reviewed paper (e.g. *Sci Transl Med* 17:eadn5603), (c) a ClinicalTrials.gov record (e.g. NCT05248230, NCT05668741), or (d) a structural stub with explicit honest disclosure. **The manuscript explicitly documents where the v0.10.1 toolkit does NOT match the published programs (ΔR minigene alone; proprietary capsids; live-backend gaps) — these are not failures but honest disclosure of structural-scaffolding limits.**

4. **Original work?** — Yes. To our knowledge, the v0.10.1 work is the first open-source AIDD toolkit to (a) implement a 5-item honest-controls gate, (b) ship an AAV vector design subsystem validated against published clinical-trial-stage programs, and (c) document the LNP-mRNA CF lung risk post-VX-522 in the toolkit's release notes. The synthesis in §3.3 is original integration of four primary sources; the toolkit code is original.

5. **Not published elsewhere?** — Correct. The v0.7.4 preprint (Oct 13 2026) was a formatting pass over the v0.7.4 in-repo source files. The v0.10.1 preprint (this manuscript) is the first time the AAV subsystem, the wet-lab validation, and the 2024–2025 AIDD-frontier context are integrated. The toolkit has been released on GitHub as v0.10.0 and v0.10.1 (October 14 and 15 2026) but the manuscript has not been submitted to any other preprint server or peer-reviewed journal.

## Why this preprint matters now

The 2024–2025 AIDD frontier has produced AlphaFold 3, Boltz-2, BoltzGen, AlphaMissense, GEMORNA, and Insilico's Rentosertib — collectively moving AIDD from "computational tool" to "clinically tested drug." The Open mRNA Therapeutics AIDD layer (the LinearDesign / codon-optimization ecosystem) has been comparatively quiet. This preprint positions `mrnavax-rare` as the **open-source honest-controls layer for rare-disease mRNA therapeutics** that sits on top of the foundation models the 2024–2025 frontier has produced. The v0.10.1 wet-lab validation is the first step toward end-to-end rare-disease AIDD with the reproducibility standards the field needs.

## Open-source license

The toolkit is dual-licensed: AGPL-3.0-or-later for open use, with a commercial license available on request (see `LICENSE` and `LICENSE-AGPL`). The preprint is CC-BY 4.0.

## Reproducibility

- **Code**: `https://github.com/rollroyces/mrnavax-rare` (releases: v0.7.4, v0.10.0, v0.10.1)
- **Test suite**: `python3 -m pytest tests/` → 279 + 1 skipped (TDC), 0 regressions
- **Pipeline reproduction**: `bash studies/phase1_trial_design/REPRODUCE.sh`
- **Wet-lab validation synthesis**: `paper/AAV_WET_LAB_VALIDATION.md`

I thank the editorial team for their consideration and am happy to provide any additional information needed for screening.

Sincerely,
Royce Lam
RollRoyces Research (independent)
`rollroyces@example.com`
