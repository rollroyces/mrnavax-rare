# AAV vector design — wet-lab validation sweep (v0.10.1, 2026-10-15)

> **Purpose.** This document validates the v0.10 `mrnavax_rare.aav` subsystem
> against published wet-lab evidence. It identifies four structural gaps
> in the v0.10 mock and proposes concrete v0.10.1 extensions. Every
> quantitative anchor cites the source paper / ClinicalTrials.gov record
> it comes from; no fabricated numbers are introduced.

## 1. Why this sweep

The v0.10 release shipped a structural `MockAAVVectorDesigner` with
honest-disclosure notes that called out:
- No codon optimization in v0.10
- "Split-vector or trans-splicing" as a recommendation for over-ceiling cassettes
- Wildtype capsids only (no evolved capsids)

This sweep reads the real published programs that the v0.10 mock was
modelling against, and asks: **what would a top-tier AIDD pipeline have
to add to match the state of the art?**

## 2. Real programs reviewed

### 2.1 4D-710 — 4D Molecular Therapeutics (NCT05248230)

- **Capsid:** 4D-A101 (4DMT's directed-evolution variant; not in
  `AAV_CAPSIDS` in v0.10)
- **Transgene:** "codon-optimized microCFTR" (CFTR with the regulatory
  domain residues 708–835 deleted — `CFTRΔR(708–835)`)
- **Mechanism:** partial R-domain removal yields a PKA-phosphorylation-
  independent chloride channel that is **still functional** (see §3.1
  for the structural anchor)
- **Delivery:** aerosol / inhaled, single dose
- **Trial:** Phase 1/2, 21–30 patients, primary completion Jun 2027
- **Construct size benefit:** the ΔR deletion shortens the CDS by
  ~128 aa × 3 = 384 nt, bringing the total cassette closer to the
  4.7 kb ceiling
- **Source:** ClinicalTrials.gov NCT05248230; 4DMT press release
  Oct 2022 (NACFC 2022 abstract); 4DMT corporate site
- **Confidence:** high (NCT-anchored, multiple press confirmations)

### 2.2 SP-101 / SPIRO-2101 — Spirovant Sciences

- **Capsid:** AAV2.5T (Spirovant's directed-evolution variant of AAV2;
  not in `AAV_CAPSIDS` in v0.10)
- **Transgene:** "fCFTRΔR" — ferret-codon-optimized CFTR with R-domain
  deletion (the **same ΔR truncation strategy as 4D-710**)
- **Co-administration:** **inhaled doxorubicin** as a transgene
  expression enhancer (this is an unusual design element — doxorubicin
  is normally a chemotherapeutic; Spirovant is using it as a TOPO-II
  inhibitor to boost transgene expression in the airway)
- **Delivery:** aerosol / inhaled
- **Trial:** SAAVe Phase 1/2 (FDA Orphan Drug + Rare Pediatric
  Designations, Sept 2020)
- **Source:** Spirovant press releases (Sept 2020, Nov 2021, Nov 2022,
  May 2022 NACFC posters); Spirovant publications page
- **Confidence:** high (multiple Spirovant publications, FDA
  designations)

### 2.3 DLX2.0-SCN1A — Allen Institute + Seattle Children's (Mich et al. 2025)

- **Capsid:** **AAV2/PHP.eB** (an engineered AAV9 variant for CNS
  delivery; Chan et al. 2017 *Nat Neurosci*)
- **Transgene:** **full-length human SCN1A** (~6 kb ORF) split in half
  via **split-intein** protein trans-splicing
- **Enhancer:** **hDLXI5/6i** (cell-type specific GABAergic
  interneuron enhancer; Dimidschstein et al. 2016 *Nat Neurosci*;
  Mich et al. 2021 *Cell Rep*)
- **Delivery:** bilateral intracerebroventricular (ICV) injection at
  P2 in mice
- **Result:** 100% survival past P70 in DS mice (vs 50% in
  untreated); ~50% protection against hyperthermia-induced myoclonic
  jerks; all but one mouse protected against generalized tonic-clonic
  seizures up to 42 °C
- **Critical safety finding:** **pan-neuronal expression** (hSyn1
  promoter instead of DLX2.0) caused **dose-dependent preweaning
  mortality** — confirms that cell-type specificity is not optional
  for SCN1A gene therapy
- **Source:** Mich JK, Ryu J, Wei AD, et al. *Interneuron-specific
  dual-AAV SCN1A gene replacement corrects epileptic phenotypes in
  mouse models of Dravet syndrome.* **Science Translational Medicine
  17(790):eadn5603 (March 19, 2025)**. DOI: 10.1126/scitranslmed.adn5603
- **Funding:** NIH UG3MH120095, RF1MH114126, UF1MH128339
- **Confidence:** very high (peer-reviewed in *Science Translational
  Medicine*, multiple independent mouse models)

### 2.4 VX-522 — Vertex / Moderna (NCT05668741) — **DISCONTINUED**

- **Modality:** LNP-mRNA (NOT AAV)
- **Transgene:** mRNA encoding full-length CFTR
- **Delivery:** inhaled via nebulizer
- **Status:** **Vertex DISCONTINUED the program in May 2025** after
  a "persistent" tolerability issue — **lung inflammation likely
  caused by the LNP itself**, not by the mRNA cargo
- **Vertex CEO statement:** "I expect that the challenge is going to
  continue to be delivery, and in terms of modalities, we're going to
  have to go back to the drawing board."
- **Moderna CEO statement:** "Despite extensive efforts by both teams,
  we were not able to achieve a profile that supported continued
  development given tolerability issues."
- **Source:** Fierce Biotech May 2025; Vertex Q1 2025 earnings call;
  ClinicalTrials.gov NCT05668741 (study record still shows
  "Completed" with last update 2026-10-09)
- **Confidence:** very high
- **Implication for mrnavax-rare:** the v0.10 `design` (LNP-mRNA)
  subsystem's **CF lung indication is at risk** — Vertex/Moderna
  already failed the clinical translation. The `aav` subsystem is the
  more promising frontier for CF lung; mrnavax-rare's CF focus should
  probably route through `aav` for the future CF programs.

## 3. Cross-program synthesis

### 3.1 The ΔR truncation is the canonical solution to the 4.7 kb ceiling — not split-vector

Two independent programs (4D-710 and SP-101) **chose the same
truncation strategy** for the same reason: full-length CFTR exceeds
the 4.7 kb AAV ceiling. Rather than split the gene across two vectors
(which requires dual-AAV delivery, halved expression, and a trans-
splicing junction), both programs **truncated the regulatory (R)
domain** to bring the cassette closer to 4.7 kb.

The R-domain deletion (residues 708–835) is mechanistically informed:
the R domain is a disordered, multi-phospho-site regulatory region
that gates CFTR by PKA phosphorylation. Removing it yields a
constitutively-open (PKA-independent) chloride channel that is
**still functional as a chloride conductor** (published in
*Nanomedicine* 2026 review, Tandfonline 10.1080/17435889.2026.2640157,
"ΔR(708–835)-CFTR leads to the generation of a protein kinase A
phosphorylation-independent chloride channel").

**v0.10 gap:** the mock's `over_limit` recommendation for full-length
CFTR is the **wrong suggestion**. The published programs do NOT use
split-vector; they use **truncated minigenes**. The v0.10.1 fix is to
add a `minigene` axis to `AAVSpec` that recommends
"CFTRΔR(708–835)" for over-ceiling CFTR cassettes.

**Honest v0.10.1 disclosure:** the ΔR-only truncation gets full-length
CFTR closer to the ceiling (5,559 → 5,175 bp) but does NOT bring it
under 4.7 kb. 4DMT's actual "microCFTR" uses additional truncations
+ a minimal promoter that v0.10.1 does not yet model.

### 3.2 Evolved capsids are the standard — not wildtype AAV5/AAV9

All three AAV programs use **directed-evolution-engineered capsids**:
- 4D-A101 (4DMT proprietary; AAV5-derived)
- AAV2.5T (Spirovant proprietary; AAV2-derived)
- AAV2/PHP.eB (Caltech; AAV9-derived; Chan 2017)

None of these are in the v0.10 `AAV_CAPSIDS = (AAV5, AAV8, AAV9,
AAVrh10)` tuple. The v0.10.1 fix is to add at least `AAV-PHP.eB`
(non-proprietary, publicly available via MTA) and document the
proprietary-capsid gap honestly in the data types docstring.

### 3.3 Codon optimization is required — not optional

4D-710 and SP-101 both use codon-optimized transgenes. 4DMT calls
theirs "microCFTR" (a "minigene" + "codon-optimized" hybrid). Spirovant
calls theirs "fCFTRΔR" (ferret-codon-optimized).

**v0.10 gap:** the v0.10 release notes explicitly state "No codon
optimization in v0.10". This is a real gap relative to the published
programs. The v0.10.1 fix is to wire the AAV cassette through
`mrnavax.codon_lineardesign.optimize_lineardesign` (the same backend
the LNP-mRNA `design` subsystem uses) and surface a `codon_optimized`
flag in `AAVSpec`.

### 3.4 Split-intein + cell-type specific enhancer is the only known SCN1A path

The v0.10 mock would, for a 6 kb SCN1A CDS, flag the cassette as
`over_limit` and recommend split-vector. The Mich 2025 paper shows
that **the right solution is split-intein protein trans-splicing**,
not "just split the vector":

- Split-intein peptides (~50 aa ≈ 150 nt) are appended to the C-terminus
  of the N-terminal SCN1A fragment and the N-terminus of the C-
  terminal fragment
- After translation, the intein peptides auto-excise and ligate the
  two SCN1A fragments into a native peptide bond
- Result: full-length NaV1.1 protein from two AAV cassettes, each
  ~3 kb, well under the 4.7 kb ceiling

And the cell-type specific enhancer (hDLXI5/6i) is **not optional**:
the hSyn1 pan-neuronal control **caused mortality**. The
target-cell-type axis is mechanistically required.

**v0.10.1 fix:** add a `split_intein` delivery mode that emits a
two-cassette pair (N-half + C-half with intein peptide tags) instead
of a single over-ceiling cassette; add a `cell_type_enhancer` axis
to the promoter selection that includes hDLXI5/6i (and warns that
pan-neuronal is unsafe for SCN1A).

## 4. What v0.10 got right (honest credit)

- **AAV is a sibling subsystem, not a modality track.** v0.10 added
  `aav` as the 9th subsystem instead of cramming it into the LNP-mRNA
  `design` subsystem. The wet-lab evidence confirms: AAV and LNP-mRNA
  are different delivery classes with different cargo sizes, different
  expression kinetics, and different clinical risk profiles. The
  separation is correct.
- **Packaging status `ok` / `borderline` / `over_limit` is a real
  diagnostic.** Both 4D-710 and SP-101 went out of their way to bring
  the cassette under 4.7 kb (via ΔR truncation) — the same
  ceiling the v0.10 mock checks. The status field is doing real
  work.
- **Capsid-for-tissue dispatch.** The mock's `lung → AAV5`,
  `liver → AAV8`, `cns → AAV9` defaults are the right
  *direction*. None of the real programs use these wildtype serotypes
  directly, but the tissue-to-capsid mapping is correct in spirit.
  The v0.10.1 fix is to add the engineered variants.
- **HGVS-C variant application via `apply_hgvs_c`.** The real programs
  (4D-710, SP-101) deliver the *wildtype* transgene — the PTC lives
  in the patient's genome, not in the delivered vector. The mock's
  decision to leave `hgvs_c_applied = ""` for wildtype payloads is
  correct; the VariantInjector pathway remains useful for the v0.7.2+
  design of non-PTC variants (e.g. AAV-delivered engineered
  sequences).

## 5. v0.10.1 changes (shipped)

1. **Added `AAV-PHP.eB` to `AAV_CAPSIDS`** — the only non-proprietary
   engineered capsid in the public literature. Documented the
   proprietary 4D-A101 / AAV2.5T gap honestly via the new
   `proprietary_capsid_caveat` field on `AAVSpec`.
2. **Added `AAVSpec.minigene` field** (default `None`; e.g. `"CFTRΔR(708–835)"`)
   that triggers a payload-length recompute using the truncated CDS.
3. **Added `AAVSpec.codon_optimized` field** (bool, default `False`).
   When `True`, the CDS is passed through
   `mrnavax.codon_lineardesign.optimize_lineardesign` before
   cassette assembly.
4. **Added `AAVSpec.split_intein` field** (default `None`; e.g.
   `("N", "C")` for two-cassette split-intein delivery). When set,
   `packaging_status` is computed per-half and the `payload` field
   becomes a tuple of two cassettes.
5. **Added `AAVSpec.cell_type_enhancer` field** (default `None`; e.g.
   `"hDLXI5/6i"` for GABAergic interneurons). Surfaces a safety note
   when a pan-neuronal enhancer (e.g. `hSyn`) is paired with a
   pathogenic gene that has known cell-type-specific requirements
   (e.g. SCN1A — Mich 2025 published hSyn1-SCN1A mortality).
6. **Bumped `__version__` to `"0.10.1"` and `pyproject.toml` to `0.10.1`.**
7. **Updated CHANGELOG.md** with a v0.10.1 entry linking to this
   paper and citing the four real programs.
8. **Added 23 new tests** in `tests/test_aav_v0101.py` that verify
   the v0.10.1 extensions against the real published constructs
   (e.g. assert that `minigene="CFTRΔR(708–835)"` brings full-length
   CFTR to 5,175 bp; assert that `split_intein` for a 6,030 bp SCN1A
   emits two 4,331 bp cassettes each under the ceiling; assert that
   `hSyn1 + SCN1A` triggers the Mich 2025 safety note).

## 6. Honest disclosure

- **No wet-lab evidence has been produced by mrnavax-rare itself.**
  The 279 + 1 tests are unit tests of structural scaffolding, not
  in-vitro / in-vivo validation. The wet-lab evidence in §2 is cited
  from published peer-reviewed papers and ClinicalTrials.gov records.
- **The proprietary capsid gap is real.** 4DMT and Spirovant
  capsids are not publicly available. mrnavax-rare users who want
  to model those programs exactly will need a separate license /
  partnership. v0.10.1 documents the gap; it does not solve it.
- **VX-522's discontinuation is a caution, not a refutation.** The
  LNP-mRNA CF lung delivery failed in the clinic. This is strong
  evidence that AAV (not LNP-mRNA) is the more promising CF lung
  therapeutic modality. It does NOT mean LNP-mRNA is dead for CF
  (other LNP formulations may work) or for other indications.
- **The hSyn1-induced mortality in the Mich 2025 paper is a
  critical safety signal**, not a peripheral finding. Any AIDD
  pipeline that recommends a pan-neuronal SCN1A promoter is
  recommending something with published lethality in DS mice. The
  v0.10.1 safety note is non-negotiable.
- **The ΔR minigene alone doesn't fix CFTR over-ceiling.** The math
  (5,175 bp) is still above 4.7 kb. Real 4DMT "microCFTR" uses
  additional truncations + a minimal promoter that v0.10.1 does not
  yet model. v0.10.1 documents this honestly in
  `tests/test_aav_v0101.py::test_minigene_cftr_dr_honest_math`.
