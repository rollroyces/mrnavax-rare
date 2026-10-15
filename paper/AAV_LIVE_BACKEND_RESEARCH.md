# AAV live-backend research note (v0.10.2, 2026-10-15)

> **Purpose.** This note records the v0.10.2 AAV live-backend research —
> i.e. whether there exists a public, installable, open viral-vector
> design tool that the v0.10.1 ``LiveAAVVectorDesigner`` could
> integrate with. The v0.10.1 wet-lab validation surfaced 4D-A101 and
> AAV2.5T as proprietary; this note asks whether the field has any
> open equivalent.

## 1. The honest finding: there is no public open viral-vector-design tool

After a search of the 2024–2026 literature, the honest finding is:

> **There is no public, installable, open viral-vector-design tool
> that the v0.10.1 ``LiveAAVVectorDesigner`` can integrate with.**
> The v0.10.1 ``NotImplementedError`` stub is the honest state of the
> public-tool ecosystem as of October 2026.

This finding is the reason the v0.10.1 release notes documented the
**proprietary capsid gap** (4D-A101, AAV2.5T) as a known limitation
rather than as something v0.10.1 would solve.

## 2. The closest open tools — and what they can/can't do

Three open tools in the 2024–2026 AAV engineering space:

### 2.1 BindCraft (EPFL, *Nature* 2025)

- **Source**: Pacesa M., Nickel L., Schellhaas C. et al. *One-shot
  design of functional protein binders with BindCraft.* **Nature**
  (2025). DOI: 10.1038/s41586-025-09429-6
- **URL**: https://news.epfl.ch/news/bindcraft-generates-novel-peptides-to-improve-gene/
- **Capability**: **de novo protein binder design** — generates
  miniproteins that bind a target receptor.
- **AAV application**: The Correia Lab has **already applied BindCraft
  to AAV capsid engineering** — they generated "de-targeted" AAV
  vectors plus BindCraft-designed miniproteins that confer new
  receptor specificity.
- **What BindCraft can do for mrnavax-rare**: the v0.10.2
  ``LiveAAVVectorDesigner`` could integrate BindCraft as a *peptide
  insertion* backend.
- **What BindCraft cannot do**: BindCraft is a **protein binder**
  tool, not a full capsid-evolution or capsid-rational-design tool.

### 2.2 Boltz-2 / BoltzGen (MIT, 2025)

- **Source**: Passaro, Corso, Wohlwend et al. *Boltz-2: Towards
  Accurate and Efficient Binding Affinity Prediction.* bioRxiv 14
  June 2025; MIT Jameel Clinic + Recursion. MIT-licensed.
- **Capability**: **structure prediction + de novo binder design**
  for proteins, nucleic acids, ligands.
- **What Boltz-2 can do for mrnavax-rare**: predict the structure
  of a designed AAV capsid + bound receptor.
- **What Boltz-2 cannot do**: capsid engineering. Capsid design
  still requires directed evolution (4DMT / Spirovant proprietary) or
  rational design with BindCraft-style peptide insertion.

### 2.3 Directed evolution platforms (proprietary)

- **4D Molecular Therapeutics**: 4D-A101 capsid (AAV5-derived,
  directed evolution). Proprietary.
- **Spirovant Sciences**: AAV2.5T capsid (AAV2-derived, directed
  evolution). Proprietary.
- **Academic capsid-evolution libraries** are research-use; no public
  tool exposes the screening workflow as a callable service.

## 3. The AI-based AAV engineering review (Tan et al. 2025, *Adv Sci*)

- **Source**: Tan F., Dong Y., Qi J., Yu W., Chai R. *Artificial
  Intelligence-Based Approaches for AAV Vector Engineering.*
  **Adv Sci (Weinh)** 12(9):2411062 (2025 Feb 11).
  DOI: 10.1002/advs.202411062. PMID: 39932449. PMCID: PMC11884542.
- **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11884542/
- **Finding**: Tan et al. 2025 survey 7 FDA-approved AAV gene
  therapies (as of Dec 2024) and ~331 AAV gene therapy clinical
  trials. They classify AI-based AAV engineering into:
  1. Capsid sequence generation (academic, no public tool).
  2. Tropism prediction (academic, no public tool).
  3. Immunogenicity prediction (academic, no public tool).
  4. Manufacturing yield optimization (academic, no public tool).
- **Honest finding**: every one of these four AI-based AAV
  engineering capabilities is in academic papers, not in public
  installable tools. The closest "near-public" capability is
  BindCraft's de novo binder design (EPFL 2025).

## 4. Implication for mrnavax-rare v0.10.2

The v0.10.1 ``LiveAAVVectorDesigner`` remains a
``NotImplementedError`` stub. The honest v0.10.2 position:

- **BindCraft integration is a v0.11+ target**, not a v0.10.2
  deliverable.
- **The proprietary capsid gap (4D-A101, AAV2.5T) remains
  unsolved** — there is no public sequence or structure file for
  these capsids. mrnavax-rare users who want to model those
  programs exactly will continue to need direct license / partnership
  with 4DMT or Spirovant.
- **The wildtype capsid surface (AAV5 / AAV8 / AAV9 / AAVrh10 /
  AAV-PHP.eB) is the most mrnavax-rare can do in v0.10.2 without
  external partnerships**.

## 5. v0.10.2 → v0.11+ forward work

If a user wants to integrate BindCraft in v0.11, the integration
shape would be:

```python
spec = design_aav(
    target_gene="SCN1A",
    cds_wildtype=scn1a_cds,
    tissue="cns",
    capsid="AAV-PHP.eB",
    cell_type_enhancer="hDLXI5/6i",
    peptide_insertion={
        "site": "VR-VIII",
        "design_backend": "bindcraft",
        "target_receptor": "GABAergic interneuron marker",
    },
)
```

The v0.11 ``LiveAAVVectorDesigner`` would call the BindCraft API,
splice the designed miniprotein into the capsid VR-VIII insertion
site, validate the resulting capsid structure with Boltz-2, and
emit an ``AAVSpec`` with the modified capsid.

## 6. Honest disclosure

- The BindCraft / Boltz-2 / Tan-2025 citation chain is real and
  publicly verifiable.
- The proprietary capsid gap (4D-A101, AAV2.5T) is real and
  documented in the v0.10.1 release notes.
- The "no public open viral-vector-design tool" finding is
  consistent with the 2024–2026 literature — the field is in
  active development but the tools are academic, not packaged.
- mrnavax-rare is positioned to be a downstream consumer of
  BindCraft / Boltz-2 / future open capsid-engineering tools, not
  a replacement for them.
