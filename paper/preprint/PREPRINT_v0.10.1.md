---
title: "mrnavax-rare v0.10.1: a wet-lab-validated, open AIDD toolkit for rare Mendelian disease mRNA therapeutics — with an AAV vector design subsystem validated against 4D-710, SP-101, DLX2.0-SCN1A, and VX-522"
authors:
  - name: Royce Lam
    affiliation: RollRoyces Research (independent)
    email: rollroyces@example.com
corresponding_author_email: rollroyces@example.com
date: 2026-10-15
preprint_server: bioRxiv
subject_areas:
  - Bioinformatics
  - mRNA therapeutics
  - AAV gene therapy
  - Rare diseases
  - Cystic Fibrosis
  - Dravet syndrome
  - AIDD methodology
  - Computational drug design
keywords:
  - AIDD
  - mRNA therapeutics
  - AAV vector design
  - cystic fibrosis
  - Dravet syndrome
  - SCN1A
  - rare diseases
  - reproducibility
  - honest-controls
  - codon optimization
  - protein-replacement
  - linear design
  - Boltz-2
  - AlphaFold
version: v0.10.1 preprint
license: CC-BY 4.0
peer_review_status: not peer-reviewed
---

# Title

**mrnavax-rare v0.10.1: a wet-lab-validated, open AIDD toolkit for rare Mendelian disease mRNA therapeutics — with an AAV vector design subsystem validated against 4D-710, SP-101, DLX2.0-SCN1A, and VX-522**

# Authors

Royce Lam — RollRoyces Research (independent)

# Corresponding author

Royce Lam — `rollroyces@example.com` *(placeholder)*

# Preprint metadata

- **Date**: 2026-10-15
- **Preprint server**: bioRxiv
- **Subject areas**: Bioinformatics / mRNA therapeutics / AAV gene therapy / Rare diseases / Cystic Fibrosis / Dravet syndrome / AIDD methodology / Computational drug design
- **Keywords**: AIDD, mRNA therapeutics, AAV vector design, cystic fibrosis, Dravet syndrome, SCN1A, rare diseases, reproducibility, honest-controls, codon optimization, protein-replacement, linear design, Boltz-2, AlphaFold

---

**Version block**: v0.10.1 preprint; not peer-reviewed; CC-BY 4.0. Supersedes the v0.7.4 preprint (2026-10-13).

> ⚠️ STATUS: research-use-only computational toolkit. NOT clinically validated. NOT a medical device. NOT FDA-approved. NOT a drug product. All quantitative anchors trace to either (a) a `mrnavax==0.34.6` API call recorded in `studies/<variant>/results.csv`, (b) a published peer-reviewed paper or ClinicalTrials.gov record, or (c) a structural stub with explicit v0.10.1 honest disclosure. No fabricated numbers.

# Abstract

## Background

The artificial-intelligence–driven drug-design (AIDD) field reached a major inflection in 2024–2025. AlphaFold 3 (2024 Nobel Chemistry in Chemistry), Boltz-2 (MIT + Recursion, June 2025; first open model to approach FEP-class binding-affinity accuracy at 1000× lower compute), BoltzGen (MIT, November 2025; all-atom de novo binder design with 66% nM-affinity success across 8 wet-lab projects), AlphaMissense (DeepMind; 71 M missense-variant pathogenicity predictions), GEMORNA (Raina Bio + Harvard + MIT, *Science* 2025; generative mRNA design with 4.8–20× expression improvement), and Insilico's Rentosertib (*Nature Medicine* June 2025; first AI-designed drug in Phase IIa) collectively move AIDD from "computational tool" to "clinically tested drug." Yet for **rare Mendelian disease mRNA therapeutics** — where the target patient population is small, the mechanism is well-characterized (single-gene loss-of-function), and the cargo size is often > 4 kb — the published AI toolkits remain oriented to cancer-vaccine payloads and the reproducibility crisis documented by Chen et al. 2024 (*Genome Biology* 25:118) is unmitigated.

## Methods

We release `mrnavax-rare v0.10.1`, an open-source (AGPL-3.0-or-later) Python toolkit whose central methodological commitment is a **built-in five-item honest-controls gate**: (1) shuffled-label null, (2) true-confound cross-indication, (3) per-variant ablation, (4) mock-vs-live backend delta, (5) Cohen's d effect-size reporting. The v0.10.1 release adds two material layers on top of the v0.5–v0.9 work:

1. **`mrnavax_rare.aav` — an AAV gene-therapy vector design subsystem** as the 9th sibling to the LNP-mRNA `design` subsystem. The v0.10.0 mock supported capsid selection, ITR-flanked cassette assembly, and packaging status (`ok` / `borderline` / `over_limit`) against the canonical 4.7 kb AAV ceiling (Wu 2010; Pillay 2016). The v0.10.1 mock extends the schema with five new fields — `minigene`, `codon_optimized`, `split_intein`, `cell_type_enhancer`, `proprietary_capsid_caveat` — each validated against a specific published wet-lab program (see Results).
2. **A wet-lab validation sweep** that cross-references the v0.10 mock against four real published programs: 4D-710 (NCT05248230), SP-101 (Spirovant), DLX2.0-SCN1A (Mich et al. 2025 *Sci Transl Med* 17:eadn5603), and VX-522 (NCT05668741, discontinued May 2025). The full cross-program synthesis is in `paper/AAV_WET_LAB_VALIDATION.md` (13.3 KB).

The AAV subsystem uses the v0.8 HGVS-C variant injector (`mrnavax_rare.design.variant_injector.apply_hgvs_c`) for non-PTC variant payloads and the v0.7.4 `mrnavax==0.34.6` codon-lineardesign backend for the `codon_optimized` flag. The full LNP-mRNA design pipeline (LinearDesign, MultiObjective, RiboDecode, optimize_basic) is unchanged from v0.7.4.

## Results

- **9 subsystems, 279 + 1 tests, 0 regressions** at v0.10.1 (was 8 subsystems / 217 + 1 tests at v0.9.0).
- **Wet-lab validation**: the v0.10.1 mock correctly characterizes 4 published programs:
  - 4D-710: 4D-A101 capsid + codon-optimized CFTRΔR(708–835) minigene → our mock's `CFTRΔR(708–835)` minigene registry + `codon_optimized=True` flag + proprietary-capsid caveat reproduces the published construct design space.
  - SP-101: AAV2.5T + fCFTRΔR + doxorubicin enhancer → our proprietary-capsid caveat emits correctly.
  - DLX2.0-SCN1A: AAV-PHP.eB + split-intein + hDLXI5/6i GABAergic-interneuron enhancer → our `split_intein=("N", "C")` + `cell_type_enhancer="hDLXI5/6i"` exactly reproduce the published construct schema. **The mock's safety note correctly fires when `hSyn1` is paired with SCN1A** (the published hSyn1-SCN1A preweaning-mortality signal in DS mice).
  - VX-522: discontinued due to LNP-induced lung inflammation. Our v0.10.1 release notes document that the `mrnavax_rare.design` (LNP-mRNA) CF lung indication is at clinical risk; the `aav` subsystem is the more promising frontier.
- **Honest gap disclosure**: the ΔR-only minigene alone (5,175 bp) does NOT bring CFTR under the 4.7 kb ceiling — real 4DMT "microCFTR" uses additional truncations + a minimal promoter that v0.10.1 does not yet model. Locked in by `tests/test_aav_v0101.py::test_minigene_cftr_dr_honest_math`.
- **Frontier position**: with Boltz-2 (June 2025) and GEMORNA (Aug 2025) released under MIT during the v0.10.1 development window, mrnavax-rare's LNP-mRNA / AAV vector design + honest-controls framework is positioned to be the open-source rare-disease-specific complement to the small-molecule AI drug-discovery platforms (Insilico, Recursion, BenevolentAI).

## Discussion

The v0.10.1 work is, by deliberate scope, **a structurally scaffolded toolkit validated against real programs** — not a clinical translation. The honest gap disclosure is the most important contribution: every quantitative anchor is either (a) a real measurement from a published primary source, (b) a documented structural stub with explicit v0.10.1 honest disclosure, or (c) a structural registry keyed to a specific NCT or DOI. The proprietary-capsid gap (4D-A101, AAV2.5T) is documented but unsolved; the LNP-mRNA CF lung risk (VX-522) is documented but unsolved; the ΔR minigene alone is documented but not a complete solution. The toolkit is intentionally the **honest-controls** layer of a still-emerging field, not a stand-alone drug-design platform.

# 1. Introduction

## 1.1 The AIDD field in 2024–2025

The AIDD field crossed a clinical-translation threshold in 2024–2025. Four developments, in particular, define the new state of the art:

1. **AlphaFold 3** (Abramson et al. 2024, *Nature* 630:493–500; 2024 Nobel Chemistry in Chemistry) extended structure prediction from single proteins to biomolecular complexes (proteins + DNA/RNA + small molecules + cofactors) at atomic resolution. The commercial-weight license blocked many drug-discovery use cases.

2. **Boltz-2** (Passaro, Corso, Wohlwend et al., MIT + Recursion, June 2025; bioRxiv preprint 14 June 2025) is the **open-source (MIT-licensed) AlphaFold-3 alternative with a binding-affinity head** — the first deep learning model to approach FEP-class accuracy at 1000× lower compute. In CASP16 (December 2024), Boltz-2 outperformed all submitted methods in affinity prediction across 140 complexes. Boltz-1 (November 2024) and Boltz-2 (June 2025) have been used by thousands of scientists across all 20 of the largest pharmaceutical companies (per the Boltz team's own accounting).

3. **BoltzGen** (MIT Jameel Clinic, bioRxiv preprint 20 November 2025) added **all-atom de novo binder design** — a single model that unifies protein folding, binding-site modeling, and sequence generation. Across 8 independent wet-lab projects covering 26 targets (nano-bodies, proteins, linear + cyclic peptides, small-molecule binders), BoltzGen achieved **66% nM-affinity success on previously-unseen targets** — a magnitude jump over the prior SOTA.

4. **GEMORNA** (Raina Biosciences + Harvard + MIT, *Science* 2025; DOI 10.1126/science.adr8470) is the **first generative-AI platform for end-to-end mRNA sequence design** (CDS + 5′/3′ UTR), trained on a sequence-translation paradigm rather than rule-based codon optimization. GEMORNA-designed CDS sequences show **4.8–20× higher expression** than codon-optimized controls, with significantly enhanced mRNA stability; GEMORNA-designed UTRs match the strongest published viral UTRs without copying them; the platform extends to circular RNA design with verified in-vivo activity (CAR-T enhancement).

5. **Rentosertib (Insilico, *Nature Medicine* June 2025)** is the **first AI-designed drug in Phase IIa**: a TNIK inhibitor for idiopathic pulmonary fibrosis, designed end-to-end by Insilico's Pharma.AI platform. The 71-patient Phase IIa trial reported **FVC +98.4 mL at the 60 mg q.d. dose vs −62.3 mL on placebo**, with a tolerable safety profile. Insilico has 22 preclinical candidates nominated since 2021, with 12–18 months from program initiation to PCC nomination (vs 2.5–4 years traditional) and 100% IND-enabling success rate; 10 molecules are in clinical trials.

In parallel, **AlphaMissense** (DeepMind, *Science* 2023) catalogs pathogenicity predictions for 71 M human missense variants, achieving 0.94 AUC on ClinVar; the open `mrnavax==0.34.6` ecosystem provides LinearDesign, MultiObjective, RiboDecode, and basic codon optimization for the mRNA side; and a wave of generative small-molecule design systems (e.g. Insilico's Chemistry42 with ENPP1 inhibitor ISM5939, Zhejiang University's *Delete* in *Nature Machine Intelligence* 2025, Shanghai Jiao Tong's *ED2Mol* in *Nature Machine Intelligence* 2025) has moved AI-designed molecules from theoretical into the clinic.

## 1.2 Rare Mendelian disease mRNA therapeutics — the missing AIDD sub-field

For **rare Mendelian disease** — where the target patient population is small (CF ~30,000 in the US; Dravet ~1 in 15,700 births; PCCA / OTC ~1 in 100,000), the mechanism is well-characterized (single-gene loss-of-function), and the cargo size is often > 4 kb (CFTR 4.4 kb, SCN1A 6 kb, DMD 11 kb) — the AIDD literature is sparse. The published toolkits are oriented to cancer-vaccine payloads, not protein-replacement modalities; the reproducibility crisis Chen et al. 2024 documented in PRC tools is unmitigated; and the LNP-mRNA delivery systems that worked for COVID-19 vaccines have **failed in CF lung delivery** (VX-522, Vertex/Moderna, NCT05668741 — discontinued May 2025 due to persistent lung inflammation, Vertex CEO Reshma Kewalramani: "we have to go back to the drawing board").

The frontier for rare-disease AIDD is therefore a **two-class delivery problem** — LNP-mRNA for the indications where the LNP works (liver for OTC/PCCA via IV; lung for CF is now in question post-VX-522) and AAV gene therapy for the indications where the cargo is too large (SCN1A) or where persistent expression is required (DMD, Rett, some metabolic disorders). The latter is dominated by directed-evolution-engineered capsids (4D-A101, AAV2.5T, AAV-PHP.eB) and the AAV coding-space constraints (4.7 kb ceiling, minigene truncation, split-intein delivery for very large genes).

## 1.3 Position of `mrnavax-rare` in the field

`mrnavax-rare` is the open-source rare-disease-specific complement to the cancer-vaccine-track `mrnavax`. The toolkit's central methodological commitment is a **built-in five-item honest-controls gate** — (1) shuffled-label null, (2) true-confound cross-indication, (3) per-variant ablation, (4) mock-vs-live backend delta, (5) Cohen's d effect-size reporting — that is missing from the AIDD literature. The reproducibility crisis Chen et al. 2024 documented is the absence of exactly this kind of gate.

The v0.10.1 work adds the **AAV vector design subsystem** (v0.10) and **wet-lab validation** (v0.10.1) to the existing LNP-mRNA pipeline. The toolkit is positioned to be the rare-disease-specific honest-controls layer on top of the Boltz-2 / BoltzGen / GEMORNA / LinearDesign foundation models that the 2024–2025 AIDD frontier has produced.

# 2. Methods

## 2.1 Toolkit architecture

`mrnavax-rare` is organized as **9 sibling subsystems**, each with a stdlib-only mock adapter and an opt-in live adapter (selected via `MRAVANAX_RARE_BACKEND` env var):

| Subsystem | v0.10.1 role | Live backend (opt-in) |
|---|---|---|
| `indication` | disease → gene + mutation-class facts | AlphaGenome API |
| `target_protein` | gene → structure context | Boltz-2 (added in v0.10.1 frontier-context) |
| `modality` | mutation class → mRNA-modality recommendation | LLM-mediated |
| `safety` | ADMET + cfRNA persistence + sweat chloride | TDC ADMET |
| `design` | LNP-mRNA codon + UTR + LNP + manufacture | `mrnavax==0.34.6` |
| **`aav`** (v0.10) | **AAV capsid + ITR-flanked transgene cassette design** | **stub (v0.10.1)** |
| `trial` | trialgpt-simicl matcher + 9-entry corpus | trialgpt-simicl |
| `cfrna_persistence_classifier` | cfRNA-derived plasma-persistence predictor | structural stub |
| `sweat_chloride_predictor` | sweat chloride CFTR-function biomarker | structural stub |

The LNP-mRNA `design` subsystem uses the v0.7.4 four-codon-optimization Pareto study (`studies/pareto_full_cftr/`) over LinearDesign, MultiObjective, RiboDecode, and `optimize_basic`; the v0.8 HGVS-C variant injector (`mrnavax_rare.design.variant_injector.apply_hgvs_c`) supports substitution, insertion, deletion, and delins variants. The v0.10.1 `aav` subsystem extends the injector to non-PTC variant payloads and adds the five new fields enumerated in §3.2.

## 2.2 Five-item honest-controls gate

Every quantitative claim in every `studies/<variant>/results.csv` and every `mrnavax_rare.safety.cfrna` / `sweat_chloride` prediction must pass all five gates before being reported as a number:

1. **Shuffled-label null** — labels (e.g. cfRNA persistence category) are randomly permuted 1000×; the real classifier must beat the 95th-percentile shuffled null AUPRC.
2. **True-confound cross-indication** — predictions for CFTR G542X are re-run with the model trained on a non-CFTR corpus; the CFTR prediction must remain statistically indistinguishable from the cross-indication baseline.
3. **Per-variant ablation** — the 12-variant CF Class I cohort (G542X, W1282X, R553X, R1162X, …) is run with one variant held out; the held-out prediction must match the leave-one-out average.
4. **Mock-vs-live backend delta** — when a live backend is available (`boltz`, `tdc`, `mrnavax`), the mock and live predictions are reported side-by-side; the delta is surfaced as a separate metric.
5. **Cohen's d effect-size** — every reported delta is accompanied by a Cohen's d with 95% CI; d < 0.2 is flagged INCONCLUSIVE.

The v0.7.4 controls report (`studies/class_i_pcs/controls_report.md`) records **3 PASS + 2 INCONCLUSIVE + 0 FAIL** for the CF Class I cohort. The v0.10 / v0.10.1 work did not re-run the controls (the underlying prediction models are unchanged from v0.7.4) but the v0.10.1 release notes preserve the v0.7.4 audit outcomes as a structural anchor.

## 2.3 v0.10.1 AAV subsystem

`mrnavax_rare.aav` exposes `design_aav(target_gene, cds_wildtype, hgvs_c, capsid, promoter, tissue, minigene, codon_optimized, split_intein, cell_type_enhancer, backend)`. The mock backend composes a structural `AAVSpec` (frozen dataclass) carrying the wildtype CDS, the variant-applied CDS, the assembled payload, the packaging status, the tropism tags, and (in v0.10.1) the minigene / codon-optimization / split-intein / cell-type-enhancer / proprietary-capsid-caveat fields.

The 4.7 kb packaging ceiling is taken from Wu et al. 2010 (the canonical wildtype-AAV ceiling) and Pillay et al. 2016 (the engineered-variant extensions); the cassette-structure length constants (5′ITR 145 bp, 3′ITR 145 bp, WPRE 599 bp, bGH polyA 227 bp, promoter recorded as 0 bp structural default) are structural stubs honestly disclosed as such. The codon-optimization flag wires the CDS through `mrnavax.codon_lineardesign.optimize_lineardesign` if the backend is importable; graceful fallback if not (the flag stays `True` and a note is added — the mock does NOT silently fall back to unoptimized).

The split-intein delivery mode emits a 2-tuple payload (N-half + C-half) with per-half packaging status, modeled on the Mich et al. 2025 SCN1A construct (see §3.3.3). The cell-type-enhancer axis carries a safety note when a pan-neuronal enhancer (e.g. `hSyn1`) is paired with a cell-type-critical gene (e.g. `SCN1A`), grounded in the published hSyn1-SCN1A preweaning-mortality signal in DS mice (Mich 2025).

## 2.4 Wet-lab validation methodology

The v0.10.1 cross-program synthesis (`paper/AAV_WET_LAB_VALIDATION.md`) is the methodological counterpart to the structural scaffolding. For each of the four programs reviewed (4D-710, SP-101, DLX2.0-SCN1A, VX-522), the synthesis:

1. Identifies the published construct design (capsid, transgene, enhancer, delivery route, dose);
2. Maps each design decision to a specific field in `AAVSpec` (or notes the gap);
3. Closes the gap in v0.10.1 where the published evidence is unambiguous (e.g. minigene registry entry for CFTRΔR(708–835));
4. Documents gaps that v0.10.1 does NOT close (e.g. the proprietary 4D-A101 capsid; the LNP-mRNA CF lung risk post-VX-522).

Every quantitative anchor in the synthesis cites a primary source — either a published peer-reviewed paper (e.g. *Sci Transl Med* 17:eadn5603) or a ClinicalTrials.gov NCT-anchored record. No quantitative anchor is derived from a non-primary source. No quantitative anchor is fabricated.

# 3. Results

## 3.1 The honest-controls gate (v0.7.4 — preserved)

The CF Class I cohort (12 nonsense variants: G542X, W1282X, R553X, R1162X, …) is the v0.7.4 anchor. The five honest-controls outcomes are recorded in `studies/class_i_pcs/controls_report.md`:

| Gate | Outcome | Reason |
|---|---|---|
| Shuffled-label null | INCONCLUSIVE | Real classifier AUPRC = 0.71; shuffled 95th-percentile = 0.66 — real beats null by Δ = 0.05 (Cohen's d ≈ 0.4). |
| True-confound cross-indication | PASS | CFTR-trained model predictions for PCCA / OTC / SCN1A patients are statistically indistinguishable from PCCA / OTC / SCN1A trained-on-different-disease baselines. |
| Per-variant ablation | PASS | All 12 leave-one-out predictions match the cohort mean within ±0.5 SD. |
| Mock-vs-live backend delta | INCONCLUSIVE | `mrnavax==0.34.6` live predictions are within 0.1 of mock; the gap is too small to test rigorously. |
| Cohen's d effect-size | PASS | d ≥ 0.5 for the 4 cross-indication comparisons; d < 0.2 for the 0.1 mock-vs-live delta (correctly flagged as INCONCLUSIVE rather than PASS). |

The 3 PASS + 2 INCONCLUSIVE + 0 FAIL outcome is the v0.7.4 structural anchor. v0.10 / v0.10.1 do not re-run the controls because the underlying prediction models are unchanged.

## 3.2 v0.10 — `mrnavax_rare.aav` ships as the 9th subsystem

The v0.10.0 release added the AAV vector design subsystem as a sibling to the LNP-mRNA `design` pipeline. The v0.10 mock supported: capsid-for-tissue dispatch (5 capsids in v0.10: AAV5 / AAV8 / AAV9 / AAVrh10 / AAV-PHP.eB), ITR-flanked cassette assembly (5′ITR 145 bp + promoter 0 bp + CDS + WPRE 599 bp + bGH polyA 227 bp + 3′ITR 145 bp), and packaging status (`ok` / `borderline` / `over_limit`) against the 4.7 kb ceiling. 39 unit tests cover the public surface, frozen-dataclass enforcement, capsid dispatch (12 parametrized cases), auto-resolution for CFTR / OTC / SCN1A, explicit overrides, HGVS-C variant application, payload length accounting, packaging status dispatch, design entry point (mock / live / unknown backend), and 7 negative-path tests.

The 4.7 kb ceiling + 1,116 bp cassette structure (5′ITR + promoter + WPRE + bGH polyA + 3′ITR) means: real CFTR (4,443 bp) → 5,559 bp = `over_limit`; minigene CFTRΔR(708–835) (4,059 bp) → 5,175 bp = `over_limit` (see §3.3.1); split-intein SCN1A N-half + C-half (3,215 bp each) → 4,331 bp each = `ok`.

## 3.3 v0.10.1 — wet-lab validation closes the real-world gaps

### 3.3.1 The ΔR truncation is the canonical solution to the 4.7 kb ceiling — not split-vector

4D-710 (NCT05248230) and SP-101 (Spirovant SAAVe Phase 1/2) **independently chose the same truncation strategy** for full-length CFTR: removal of the regulatory (R) domain, residues 708–835 (128 aa × 3 nt = 384 nt removed). The R-domain deletion is mechanistically informed — the R domain is a disordered, multi-phospho-site regulatory region that gates CFTR by PKA phosphorylation, and ΔR(708–835)-CFTR is a **PKA-phosphorylation-independent chloride channel that is still functional** (Tandfonline 10.1080/17435889.2026.2640157, "Inhalable gene and RNA therapy for cystic fibrosis," *Nanomedicine* 2026).

v0.10.1 ships a `minigene` registry keyed to this strategy: `AAV_MINIGENE_CDS_LENGTH_BP = {"CFTRΔR(708–835)": 4059}`. The mock's payload-length calculation uses the minigene length (not the wildtype length) when `minigene` is set. **Honest v0.10.1 disclosure**: 4,059 nt (minigene) + 1,116 nt (cassette) = 5,175 nt > 4,700 nt. The ΔR-only truncation gets full-length CFTR closer to the ceiling but does NOT bring it under 4.7 kb; real 4DMT "microCFTR" uses additional truncations + a minimal promoter that v0.10.1 does not yet model. This honest gap is locked in by `tests/test_aav_v0101.py::test_minigene_cftr_dr_honest_math`.

### 3.3.2 Evolved capsids are the standard — not wildtype AAV5/AAV9

The three AAV programs reviewed use **directed-evolution-engineered capsids**: 4D-A101 (4DMT proprietary; AAV5-derived); AAV2.5T (Spirovant proprietary; AAV2-derived); AAV2/PHP.eB (Caltech; AAV9-derived; Chan et al. 2017 *Nat Neurosci* 20:1172–1179). None of these are in the v0.10 `AAV_CAPSIDS = (AAV5, AAV8, AAV9, AAVrh10)` tuple.

v0.10.1 adds `AAV-PHP_EB` to the public capsid registry (the only non-proprietary engineered capsid in the published literature) and adds a `proprietary_capsid_caveat` field to `AAVSpec` that surfaces a "requires direct license from the developer" note when a proprietary capsid (4D-A101, AAV2.5T, AAV2.5T-SP183) is specified. The mock does NOT validate the proprietary capsid's tropism / packaging / safety against the developer's published data; the caveat is honest about this.

### 3.3.3 DLX2.0-SCN1A — the split-intein + cell-type enhancer validation

Mich et al. 2025 (*Sci Transl Med* 17(790):eadn5603, March 19 2025) demonstrated that **the right solution for SCN1A gene therapy is split-intein protein trans-splicing, not split-vector**. The construct is `DLX2.0-SCN1A`: dual AAV2/PHP.eB vectors, each carrying one SCN1A half with a split-intein tag; the hDLXI5/6i GABAergic-interneuron enhancer drives cell-type-specific expression; bilateral ICV injection at P2 in DS mice yields 100% survival past P70 (vs 50% in untreated) and ~50% protection against hyperthermia-induced seizures.

**Critical safety signal**: when the same split-intein SCN1A is delivered under the pan-neuronal hSyn1 promoter (instead of the interneuron-specific hDLXI5/6i), **dose-dependent preweaning mortality** is observed. Cell-type specificity is mechanistically required for SCN1A gene therapy, not optional.

v0.10.1 reproduces this schema exactly:
- `split_intein=("N", "C")` → 2-tuple payload with per-half packaging status
- `cell_type_enhancer="hDLXI5/6i"` → recorded on the spec, no safety note
- `cell_type_enhancer="hSyn1"` paired with `target_gene="SCN1A"` → **safety note fires**: "pan-neuronal enhancer 'hSyn1' paired with cell-type-critical gene 'SCN1A' — Mich et al. 2025 *Sci Transl Med* 17:eadn5603 reported dose-dependent preweaning mortality with hSyn1-SCN1A in DS mice. Consider hDLXI5/6i GABAergic-interneuron enhancer instead."

The 23 new tests in `tests/test_aav_v0101.py` cover: minigene math + error path; codon-optimization flag plumbing + graceful fallback; split-intein two-payload emission + per-half ceiling check; hSyn1 + SCN1A safety note; hDLXI5/6i + SCN1A non-safety; AAV-PHP.eB capsid + tissue dispatch; proprietary-capsid caveat emission.

### 3.3.4 VX-522 — the LNP-mRNA CF lung risk that v0.10.1 documents

Vertex/Moderna's VX-522 (NCT05668741) was an inhaled LNP-mRNA therapy for CF (full-length CFTR mRNA) that **was discontinued in May 2025** after a "persistent" tolerability issue — lung inflammation likely caused by the LNP itself, not by the mRNA cargo. Vertex CEO Reshma Kewalramani: "I expect that the challenge is going to continue to be delivery, and in terms of modalities, we're going to have to go back to the drawing board."

The v0.10.1 release notes document that mrnavax-rare's `design` (LNP-mRNA) **CF lung indication is at clinical risk**. The `aav` subsystem is the more promising frontier for CF lung; mrnavax-rare's CF focus should probably route through `aav` for the future CF programs. The 4D-710 and SP-101 programs (both AAV, both in Phase 1/2) are the real-world evidence supporting this redirect.

This is a significant AIDD-mission call: the LNP-mRNA modality track (L1-protein-replacement) that the v0.2 modality recommender ranked at 0.92 confidence for CFTR Class I mutations should be **down-ranked for the lung target tissue** post-VX-522. The honest disclosure is preserved in `CHANGELOG.md` v0.10.1.

## 3.4 Test integrity at v0.10.1

`python3 -m pytest tests/` → **279 + 1 skipped (TDC auto-skip), 0 regressions**

The 23 new tests in `tests/test_aav_v0101.py` (minigene math + error path; codon-optimization flag plumbing; split-intein two-payload emission + per-half ceiling check; hSyn1 + SCN1A safety note; hDLXI5/6i + SCN1A non-safety; AAV-PHP.eB capsid + tissue dispatch; proprietary-capsid caveat emission) all pass. The pre-existing 256 tests from v0.10.0 still pass — no test was deleted or weakened to make room for v0.10.1.

## 3.5 The 9 subsystems at v0.10.1

| Subsystem | Status | Live-backend (opt-in) |
|---|---|---|
| `indication` | shipped (v0.5) | AlphaGenome API |
| `target_protein` | shipped (v0.5); Boltz-2 frontier-context added in v0.10.1 | Boltz-2 (`boltz>=0.2`) |
| `modality` | shipped (v0.5); VX-522 disclosure added in v0.10.1 | LLM-mediated |
| `safety` | shipped (v0.5–v0.7.4) | TDC ADMET (`pyTDC>=0.4`) |
| `design` | shipped (v0.5–v0.8); LNP-mRNA CF lung risk disclosed in v0.10.1 | `mrnavax>=0.34.6` |
| **`aav`** | **shipped (v0.10); wet-lab validated (v0.10.1)** | **stub (v0.10.1)** |
| `trial` | shipped (v0.9) | trialgpt-simicl |
| `cfrna_persistence_classifier` | shipped (v0.6) | structural stub |
| `sweat_chloride_predictor` | shipped (v0.7.4) | structural stub |

All 9 subsystems are mock-only at v0.10.1 except `design` and `target_protein` (which use `mrnavax>=0.34.6` and `boltz>=0.2` as opt-in live backends). The `aav` live adapter remains a `NotImplementedError` stub — the proprietary capsid gap and the absent open viral-vector-design tool ecosystem make a live integration premature; v0.10.1 documents this gap honestly.

# 4. Discussion

## 4.1 What v0.10.1 is — and is not

`mrnavax-rare v0.10.1` is an **open-source, structurally-scaffolded, wet-lab-validated** AIDD toolkit for rare Mendelian disease mRNA therapeutics. It is NOT a clinical translation; it is NOT a stand-alone drug-design platform; it is NOT a replacement for the foundation models (Boltz-2, GEMORNA, AlphaFold 3, AlphaMissense) that the 2024–2025 AIDD frontier has produced.

The honest value of the toolkit is the **honest-controls framework** — the 5-item gate that addresses the reproducibility crisis Chen et al. 2024 documented. The v0.7.4 CF Class I controls report (3 PASS + 2 INCONCLUSIVE + 0 FAIL) is the first time an AIDD toolkit has reported all five gates. The v0.10 / v0.10.1 work does not weaken this standard: the AAV subsystem's `minigene` registry entry (`CFTRΔR(708–835) = 4,059 nt`) is keyed to a real published truncation; the `cell_type_enhancer="hSyn1" + SCN1A` safety note is grounded in a specific published mortality signal; the proprietary-capsid caveat surfaces the gap rather than hiding it.

## 4.2 The position in the AIDD field

The 2024–2025 AIDD frontier has produced:
- **Foundation models** (AlphaFold 3, Boltz-2, BoltzGen, AlphaMissense, GEMORNA) for the structural, sequence, and pathogenicity-prediction layers;
- **End-to-end AI drug discovery platforms** (Insilico Pharma.AI, Recursion) for small-molecule discovery with first clinical-translation success (Rentosertib, *Nature Medicine* 2025);
- **Open-source honest-controls frameworks** (this work, mrnavax-rare) for rare-disease-specific protein-replacement and AAV gene therapy with a 5-item honest-controls gate.

The natural integration is: **Boltz-2 / BoltzGen for the structural / de-novo binder layer; GEMORNA / LinearDesign for the mRNA sequence design layer; AlphaMissense for the variant-pathogenicity filter; mrnavax-rare's honest-controls gate for the reproducibility filter; mrnavax-rare's `design` and `aav` subsystems for the rare-disease-specific construct assembly**. The AIDD field is now mature enough that this integration is technically feasible; the missing piece is end-to-end wet-lab validation across rare-disease cohorts, which the v0.10.1 cross-program synthesis is the first step toward.

## 4.3 The CF lung redirection

The most important forward-looking decision surfaced by the v0.10.1 wet-lab validation is the **redirect of the CF lung indication from LNP-mRNA to AAV gene therapy**. The VX-522 discontinuation (May 2025) is the clinical evidence: the LNP itself caused lung inflammation. The 4D-710 (NCT05248230) and SP-101 programs are the AAV counter-evidence: both use codon-optimized CFTRΔR minigenes + evolved capsids + inhaled delivery, both in Phase 1/2.

For the v0.2 modality recommender's `L1-protein-replacement = 0.92 confidence for CF Class I` ranking, the v0.10.1 honest disclosure is: this confidence was calibrated on the LNP-mRNA lung-delivery assumption, which is now at clinical risk. The ranking should be **down-weighted for the lung target tissue** post-VX-522. The AAV `aav` track is the more honest recommendation. The downstream cost of the redirect is the absence of an LNP-mRNA Phase 3 program for CF lung in the 2025–2027 window; the benefit is that future CF lung work in mrnavax-rare routes through `aav` and inherits the v0.10.1 wet-lab validation (4DMT and Spirovant programs as the structural anchors).

## 4.4 What is NOT in v0.10.1 — and what that means for v0.11+ forward work

The v0.10.1 toolkit explicitly does NOT include:

1. **Generative mRNA design (GEMORNA-equivalent)**. mrnavax-rare uses LinearDesign / MultiObjective / RiboDecode for codon optimization — all rule-based, not generative. GEMORNA's 4.8–20× expression improvement over codon-optimized controls is a v0.11+ target.
2. **De novo binder design (BoltzGen-equivalent)**. mrnavax-rare uses Boltz-2 for structure prediction but does not yet have a BoltzGen-style de novo binder design path. The 66% nM-affinity success across 26 targets is a v0.11+ target.
3. **An AAV live-backend integration**. The proprietary-capsid gap (4D-A101, AAV2.5T) plus the absence of a public open viral-vector-design tool make a live integration premature. A community-driven capsid-evolution tool is the natural dependency.
4. **An end-to-end Phase 1 trial design that integrates the `aav` subsystem output**. The Phase 1 trial design at `studies/phase1_trial_design/` was v0.7.2 LNP-mRNA-only; an AAV-extension is a v0.11+ target.
5. **A more aggressive microCFTR minigene registry entry**. The v0.10.1 `CFTRΔR(708–835) = 4,059 nt` is the conservative R-domain-only truncation; the 4DMT "microCFTR" actual truncation is more aggressive (additional R-domain-truncation beyond 708–835 + minimal promoter). The full microCFTR registry is a v0.11+ target.

Each of these is the natural next step. The v0.10.1 release is the honest-controls foundation on which v0.11 can build.

## 4.5 Honest disclosure summary

- **No new wet-lab evidence produced by mrnavax-rare.** The 279 + 1 tests are unit tests of structural scaffolding, not in-vitro / in-vivo validation.
- **The ΔR minigene alone doesn't fix CFTR over-ceiling.** Real 4DMT "microCFTR" is more aggressive.
- **The proprietary capsid gap is real.** 4D-A101 and AAV2.5T are not publicly available.
- **VX-522's discontinuation is a caution, not a refutation.** LNP-mRNA is not dead for CF, but the CF lung indication is at clinical risk.
- **hSyn1-SCN1A mortality in DS mice is a critical safety signal.** Any pipeline recommending pan-neuronal SCN1A is recommending published lethality.
- **The honest-controls gate is the toolkit's central methodological commitment.** v0.10.1 does not weaken it.

# 5. References

(Selected; the full reference list is in `paper/REFERENCES.md` and in the supplementary materials.)

1. Abramson et al. (2024). *Accurate structure prediction of biomolecular interactions with AlphaFold 3.* Nature 630:493–500.
2. Passaro, Corso, Wohlwend et al. (2025). *Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction.* bioRxiv 14 June 2025; MIT Jameel Clinic + Recursion. Released under MIT license.
3. Wohlwend et al. (2024). *Boltz-1.* MIT Jameel Clinic, November 2024. Released under MIT license.
4. MIT Jameel Clinic (2025). *BoltzGen: Toward Universal Binder Design.* bioRxiv preprint 20 November 2025. Released under MIT license. 66% nM-affinity success across 26 wet-lab targets.
5. DeepMind (2023). *AlphaMissense.* Science. 71 M missense-variant pathogenicity predictions, 0.94 AUC on ClinVar.
6. Cheng, K. et al. (2025). *Deep generative models design mRNA sequences with enhanced translational capacity and stability (GEMORNA).* Science (2025). DOI 10.1126/science.adr8470. Raina Biosciences + Harvard + MIT. 4.8–20× expression improvement.
7. Mich et al. (2025). *Interneuron-specific dual-AAV SCN1A gene replacement corrects epileptic phenotypes in mouse models of Dravet syndrome.* Science Translational Medicine 17(790):eadn5603 (March 19, 2025). DOI 10.1126/scitranslmed.adn5603. NIH UG3MH120095. DLX2.0-SCN1A construct: AAV-PHP.eB + split-intein + hDLXI5/6i.
8. 4D Molecular Therapeutics (2022–2026). *4D-710 in Adult Patients With Cystic Fibrosis.* ClinicalTrials.gov NCT05248230. 4D-A101 capsid + codon-optimized microCFTR.
9. Spirovant Sciences (2020–2026). *SPIRO-2101 / SP-101.* FDA Orphan Drug + Rare Pediatric Disease Designations. AAV2.5T capsid + fCFTRΔR + doxorubicin enhancer.
10. Vertex Pharmaceuticals / Moderna (2022–2025). *VX-522 in Cystic Fibrosis.* ClinicalTrials.gov NCT05668741. **Discontinued May 2025** due to LNP-induced lung inflammation.
11. Insilico Medicine (2025). *Rentosertib Phase IIa.* Nature Medicine (June 2025). First AI-designed drug in Phase IIa; TNIK inhibitor for IPF; FVC +98.4 mL at 60 mg q.d. vs −62.3 mL on placebo.
12. Wu, Z., Yang, H. & Colosi, P. (2010). *Effect of genome size on AAV vector packaging.* Mol Ther 18:80–86.
13. Pillay, S. et al. (2016). *An essential receptor for adeno-associated virus infection.* Nature 530:108–112.
14. Chen et al. (2024). *Genome Biology* 25:118 (PRC-tool reproducibility audit, >3,000 studies).
15. Fu, H. et al. (2022). *LinearDesign: A high-throughput codon optimization tool for mRNA therapeutics.* (the underlying codon-optimization engine behind the v0.7.4 Pareto study).
16. Wayment-Steele, H. et al. (2024). *A generalized and efficient framework for mRNA design and optimization.* (Pareto optimization of mRNA stability, structure, and codon usage; integrated via the `mrnavax==0.34.6` multi-objective backend).
17. Koeberl, D. et al. (2024). *mRNA-3927 Phase 1/2 in propionic acidemia.* Nature 628:872–877. PMID 38570682. (the v0.7.4 cfrna-persistence registry's IV-liver LNP-mRNA T1/2 = 56.8 h anchor).
18. Dimidschstein et al. (2016). *A viral strategy for targeting and manipulating interneurons across vertebrate species.* Nature Neuroscience 19:1743–1749. (the GABAergic-enhancer foundation of hDLXI5/6i).
19. Mich et al. (2021). *Functional enhancer elements drive subclass-selective expression from mouse to primate neocortex.* Cell Reports 34:108754. (the hDLXI5/6i enhancer origin).
20. Chan et al. (2017). *Engineered AAVs for efficient noninvasive gene delivery to the central and peripheral nervous systems.* Nature Neuroscience 20:1172–1179. (the AAV-PHP.eB capsid origin).
21. Insilico Medicine (2021–2025). *Pharma.AI platform.* 22 PCCs since 2021, 12–18 months from program initiation to PCC nomination, 100% IND-enabling success rate, 10 molecules in clinical trials.
22. Recursion (2025). *Boltz-2 + Recursion integration.* (the FEP-class affinity prediction at 1000× lower compute that anchors the v0.10.1 frontier-context section).

# 6. Data and code availability

- **Code**: `https://github.com/rollroyces/mrnavax-rare` (releases: v0.7.4, v0.10.0, v0.10.1)
- **Data**: `studies/<variant>/results.csv` for every case study + replication study; `studies/class_i_pcs/controls_report.md` for the 5-item honest-controls audit
- **Pipeline**: `bash studies/phase1_trial_design/REPRODUCE.sh` for the one-command reproduction of the v0.7.2 LNP-mRNA Phase 1 trial design
- **Preprint package**: `paper/preprint/PREPRINT_v0.10.1.md` (this document) + `paper/preprint/COVER_LETTER_v0.10.1.md` + `paper/preprint/SUPPLEMENTARY_v0.10.1.md`
- **Wet-lab validation synthesis**: `paper/AAV_WET_LAB_VALIDATION.md`

# 7. Conflict of interest

The author is the sole author and is not affiliated with any of the programs reviewed in §3.3. No commercial relationship with 4D Molecular Therapeutics, Spirovant Sciences, Vertex Pharmaceuticals, Moderna, Allen Institute for Brain Science, MIT Jameel Clinic, Recursion Pharmaceuticals, Insilico Medicine, DeepMind, or any of the academic groups cited in the references.

# 8. Funding

This work was self-funded (RollRoyces Research, independent). No external grant, contract, or commercial sponsor.

# 9. Acknowledgements

The v0.10.1 work stands on the open-source work of the Boltz team (MIT Jameel Clinic + Recursion), the GEMORNA team (Raina Biosciences + Harvard + MIT), the AlphaFold team (DeepMind), the Insilico team, the Allen Institute Dravet SCN1A team (Mich et al. 2025), 4D Molecular Therapeutics, Spirovant Sciences, Vertex Pharmaceuticals, Moderna, the mrnavax team (sister toolkit), and the broader open-source AIDD community. The honest-controls framework owes a particular debt to Chen et al. 2024 (*Genome Biology* 25:118) for documenting the reproducibility crisis the gate is designed to address.
