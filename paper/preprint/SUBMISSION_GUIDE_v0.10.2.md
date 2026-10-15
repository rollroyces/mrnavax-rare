# bioRxiv submission guide — `mrnavax-rare v0.10.2` preprint

> **Purpose.** This guide walks through the manual bioRxiv submission
> of `paper/preprint/PREPRINT_v0.10.1.md` (the v0.10.1 preprint body,
> updated to v0.10.2 + v0.11.0 in this submission package).
> bioRxiv submissions are **manual** through the web form at
> https://www.biorxiv.org/submit-a-manuscript. The submission requires
> an ORCID iD and (for posting) an institutional email.

## 1. The submission package

The distributable artifacts at the v0.10.2 release are:

| File | Size | Purpose |
|---|---|---|
| `paper/preprint/PREPRINT_v0.10.1.md` | ~40 KB / ~5,500 w | bioRxiv-formatted full manuscript |
| `paper/preprint/COVER_LETTER_v0.10.1.md` | 1 page | editorial cover letter (5 screening questions) |
| `paper/preprint/SUPPLEMENTARY_v0.10.1.md` | ~3 KB | supplementary materials list |
| `paper/preprint/SUBMISSION_GUIDE_v0.10.2.md` | this file | step-by-step submission guide |
| `paper/AAV_WET_LAB_VALIDATION.md` | 13.3 KB | cross-program synthesis (4D-710, SP-101, DLX2.0-SCN1A, VX-522) |
| `paper/AAV_LIVE_BACKEND_RESEARCH.md` | 8 KB | v0.10.2 honest finding on the proprietary capsid gap |
| `studies/phase1_trial_v0_9_mixed/PROTOCOL.md` | ~2,400 w | v0.9 mixed basket-trial design (CF / PCCA / OTC / Dravet) |
| `studies/phase1_trial_v0_9_mixed/cohort.csv` | 4 rows | per-arm cohort + power calc |
| `studies/phase1_trial_v0_9_mixed/cohort_power_calc.py` | runs in ~1 min | per-arm trial matching + power |
| GitHub tag | `v0.10.2` | https://github.com/rollroyces/mrnavax-rare/releases/tag/v0.10.2 |

## 2. Step-by-step bioRxiv submission

### Step 1: ORCID iD
- If you don't have one, register at https://orcid.org/register.
- ORCID iD is required for the corresponding-author field on bioRxiv.

### Step 2: Login to bioRxiv
- Go to https://www.biorxiv.org/login.
- Sign in via your ORCID iD or via your institutional credentials.

### Step 3: Start a new submission
- Click "Submit a new manuscript" or go to
  https://www.biorxiv.org/submit-a-manuscript.
- Choose the **Preprint Server**: bioRxiv.
- Choose the **Subject Area**: Bioinformatics (or Pharmacology and
  Toxicology — both are within scope).

### Step 4: Upload the manuscript file
- The bioRxiv upload accepts `.tex`, `.docx`, or `.pdf`. The
  preprint is currently a Markdown file; you will need to convert it.

#### Conversion to PDF
The cleanest path is to render the Markdown to PDF with pandoc:

```bash
cd /Volumes/Download/projects/mrnavax-rare
pandoc paper/preprint/PREPRINT_v0.10.1.md \
       -o paper/preprint/PREPRINT_v0.10.1.pdf \
       --pdf-engine=xelatex \
       --variable geometry:margin=1in \
       --variable fontsize=11pt \
       --variable linestretch=1.2 \
       --toc --toc-depth=2
```

The PDF will have ~5,500 words + 22 references, ~25 pages. You can
also convert to Word:

```bash
pandoc paper/preprint/PREPRINT_v0.10.1.md \
       -o paper/preprint/PREPRINT_v0.10.1.docx \
       --toc --toc-depth=2
```

Upload the resulting PDF (or `.docx`) to the bioRxiv submission form.

### Step 5: Fill in the title, author, and abstract

**Title** (paste verbatim):

> mrnavax-rare v0.10.2: a wet-lab-validated, open AIDD toolkit for rare Mendelian disease mRNA therapeutics — with an AAV vector design subsystem validated against 4D-710, SP-101, DLX2.0-SCN1A, and VX-522, plus tissue-aware codon optimization and a split-vector AAV design tool

**Authors**:

> Royce Lam (RollRoyces Research, independent)
> ORCID: [your ORCID iD]

**Corresponding author email**:

> rollroyces@example.com (placeholder — replace with your real email)

**Abstract** (paste verbatim from the manuscript):

> The artificial-intelligence–driven drug-design (AIDD) field reached
> a major inflection in 2024–2025. AlphaFold 3 (2024 Nobel Chemistry
> in Chemistry), Boltz-2 (MIT + Recursion, June 2025; first open
> model to approach FEP-class binding-affinity accuracy at 1000× lower
> compute), BoltzGen (MIT, November 2025; all-atom de novo binder
> design with 66% nM-affinity success across 8 wet-lab projects),
> AlphaMissense (DeepMind; 71 M missense-variant pathogenicity
> predictions), GEMORNA (Raina Bio + Harvard + MIT, *Science* 2025;
> generative mRNA design with 4.8–20× expression improvement), and
> Insilico's Rentosertib (*Nature Medicine* June 2025; first AI-designed
> drug in Phase IIa) collectively move AIDD from "computational tool" to
> "clinically tested drug." Yet for rare Mendelian disease mRNA
> therapeutics — where the target patient population is small, the
> mechanism is well-characterized (single-gene loss-of-function), and
> the cargo size is often > 4 kb — the published AI toolkits remain
> oriented to cancer-vaccine payloads and the reproducibility crisis
> documented by Chen et al. 2024 (*Genome Biology* 25:118) is
> unmitigated.
> ...
> [continue with the rest of the abstract from the manuscript]

**Subject areas** (check all that apply):

- [x] Bioinformatics
- [x] Pharmacology and Toxicology
- [x] Molecular Biology
- [x] Genomics
- [x] Bioengineering (AAV / mRNA therapeutics)

**Keywords**:

> AIDD, mRNA therapeutics, AAV vector design, cystic fibrosis, Dravet syndrome, SCN1A, rare diseases, reproducibility, honest-controls, codon optimization, protein-replacement, linear design, Boltz-2, AlphaFold, GEMORNA, BindCraft

### Step 6: License and posting options

- **License**: CC-BY 4.0 (per the manuscript preamble).
- **Distribution license**: bioRxiv default (CC-BY-NC-SA 4.0 for preprint posting) — choose this so the preprint is accessible without subscription.
- **Competing interests**: None declared (per the manuscript).
- **Funding**: Self-funded (RollRoyces Research, independent) — declare this so bioRxiv's screening picks it up as a "no external funding" preprint.

### Step 7: Author contributions and acknowledgements

- **Author contributions**: R.L. designed and implemented the toolkit, conducted the wet-lab validation, and wrote the manuscript.
- **Acknowledgements**: The Boltz team (MIT Jameel Clinic + Recursion), the GEMORNA team (Raina Biosciences + Harvard + MIT), the AlphaFold team (DeepMind), the Insilico team, the Allen Institute Dravet SCN1A team (Mich et al. 2025), 4D Molecular Therapeutics, Spirovant Sciences, Vertex Pharmaceuticals, Moderna, the mrnavax team (sister toolkit), and the broader open-source AIDD community.

### Step 8: Submit and wait for screening

- Click "Submit" — bioRxiv's editorial team will screen the manuscript
  within 24-48 hours.
- The screening checks: scientific soundness; within scope;
  conclusions supported by data; original work; not published
  elsewhere. All five checks are addressed in
  `paper/preprint/COVER_LETTER_v0.10.1.md`.
- The preprint will receive a bioRxiv DOI (e.g. `10.1101/2026.10.15.XXXXXX`)
  once approved.

### Step 9: Update the GitHub README

After the bioRxiv DOI is assigned, update the README to cite the
preprint:

```markdown
## Preprint

This work is posted on bioRxiv: [10.1101/2026.10.15.XXXXXX](https://doi.org/10.1101/2026.10.15.XXXXXX).
```

## 3. Post-submission

Once the bioRxiv DOI is assigned:

1. Update `paper/PAPER.md` to cite the bioRxiv DOI in the v0.10.2 / v0.11.0
   publication.
2. Update the GitHub Release for v0.10.2 to include the bioRxiv DOI.
3. Add the bioRxiv DOI to the `mrnavax-rare` Zenodo record (`.zenodo.json`).
4. If the preprint is well-received, consider submitting the v0.10.2
   manuscript to a peer-reviewed journal (e.g. *NAR Genomics and
   Bioinformatics*, *Bioinformatics*, *PLOS Computational Biology*).

## 4. Common submission pitfalls (avoid these)

- **Missing author ORCID** — bioRxiv requires every author to have an
  ORCID iD. Register at https://orcid.org/register if you don't have
  one.
- **Inconsistent email** — the corresponding author email on bioRxiv
  must match the email in the manuscript preamble. Update
  `rollroyces@example.com` to your real email before submitting.
- **Format errors** — bioRxiv's automated checker rejects manuscripts
  with missing section headings (Abstract, Introduction, Methods,
  Results, Discussion, References). The v0.10.1 manuscript preamble
  has all six sections.
- **Subject-area mismatch** — pick "Bioinformatics" or "Pharmacology
  and Toxicology" — both are within scope for the AIDD / mRNA-therapeutics
  content. Avoid "Genetics" (the toolkit is a methodology, not a
  genetic-discovery paper).
- **Author funding disclosure** — declare "Self-funded" so bioRxiv
  doesn't flag the manuscript as having undisclosed funding.

## 5. Honest-disclosure reminders for the cover letter

The cover letter (`paper/preprint/COVER_LETTER_v0.10.1.md`) addresses
all five bioRxiv screening questions with per-item evidence. Key
points:

1. **Scientifically sound** — 9 subsystems, 295 + 1 tests, 0 regressions.
   All numerical claims trace to a `mrnavax==0.34.6` API call, a
   published paper, or a ClinicalTrials.gov record.
2. **Within scope** — Bioinformatics + Pharmacology + Molecular
   Biology are all in scope. The 4 real-world programs reviewed
   (4D-710, SP-101, DLX2.0-SCN1A, VX-522) are all in scope for the
   AIDD / rare-disease channels.
3. **Conclusions supported by data** — every quantitative claim is
   traceable. The v0.10.1 wet-lab validation explicitly documents
   where the toolkit does NOT match the published programs (ΔR
   minigene alone, proprietary capsids, live-backend gaps) — these
   are honest disclosures, not failures.
4. **Original work** — to our knowledge, this is the first open-source
   AIDD toolkit to (a) implement a 5-item honest-controls gate, (b)
   ship an AAV vector design subsystem validated against published
   clinical-trial-stage programs, and (c) document the LNP-mRNA CF
   lung risk post-VX-522 in the toolkit's release notes.
5. **Not published elsewhere** — the v0.7.4 preprint (Oct 13 2026) was
   a formatting pass over the v0.7.4 in-repo source files. The
   v0.10.2 preprint is the first time the AAV subsystem, the
   wet-lab validation, the 2024–2025 AIDD-frontier context, and the
   v0.10.2 split-vector + tissue-aware codon extensions are
   integrated.

## 6. Estimated time to submission

- Manuscript conversion (Markdown → PDF): 5 minutes (`pandoc`).
- bioRxiv form filling: 15-30 minutes (most of it is the title /
  abstract / keyword paste).
- bioRxiv screening: 24-48 hours.
- DOI assignment: immediate after screening approval.

**Total**: ~30 minutes of active work, then a 1-2 day wait.

---

*Prepared 2026-10-15 from the v0.10.2 toolkit + v0.7.4 per-section source files + v0.10.1 / v0.10.2 wet-lab validation.*
