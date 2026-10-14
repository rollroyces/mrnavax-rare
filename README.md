# mrnavax-rare

> mRNA therapeutics design toolkit for rare Mendelian diseases.
> Extension of [mrnavax](https://github.com/rollroyces/mrnavax) — codon + UTR + LNP + indication-aware protein-replacement design for the genetic-disease track, not cancer vaccines.

[![CI](https://img.shields.io/badge/CI-passing-brightgreen?logo=githubactions&logoColor=white)](https://github.com/rollroyces/mrnavax-rare/actions)
[![Python](https://img.shields.io/badge/Python-3.11–3.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Sister](https://img.shields.io/badge/sister-mrnavax%200.34-9b8cff)](https://github.com/rollroyces/mrnavax)
[![Status](https://img.shields.io/badge/status-v0.10.0-yellow)]()
[![License](https://img.shields.io/badge/license-AGPL--3.0--or--later%20%2F%20commercial-orange)](LICENSE)

> **Work in progress — AIDD warmup sprints.** v0.10.0 ships 9 subsystems (incl. AAV vector design) with 256 + 1 tests, 0 regressions. No wet lab; structural computational toolkit.

## What this is

A separate sibling of `mrnavax` that focuses on the same eight-layer mRNA-therapeutics pipeline
but routed toward **rare Mendelian disease** rather than cancer vaccines.

| Layer | Cancer-vaccine track (mrnavax) | Rare-disease track (mrnavax-rare) |
|---|---|---|
| Indication | Tumor type + HLA + neoantigen burden | Disease name + causal gene + mutation class |
| Modality | mRNA cancer vaccine (mutant peptides) | Protein replacement · mRNA-CRISPR edit · mRNA-silencing · corrective mRNA |
| Target prioritization | AlphaMissense + AlphaGenome Atlas (coding + regulatory VUS) | AlphaMissense (LOF variants) + AlphaGenome Atlas (regulatory non-coding) + ClinVar pathogenic |
| Sequence | LinearDesign / RiboDecode | LinearDesign / RiboDecode (re-used via mrnavax) |
| Neoantigen / epitope | mhcflurry + ESM2 | N/A (replacement) · mhcflurry for tolerance checks |
| Delivery | LNP — tumor-targeting | LNP — tissue-specific (liver, lung, muscle, CNS) · **AAV gene therapy** (v0.10) |
| Manufacturability | Poly-A / Kozak / GC / ARE | Poly-A / Kozak / GC / ARE (same checks, different thresholds) |
| Trial | TrialGPT per-criterion matching | TrialGPT (genetic-disease–specific corpus) |
| **Target structure** | — | **Boltz-1 / AF3 / PDB** for the protein context |
| **Safety oracle** | Toxic motif / off-target HLA | **TDC ADMET** (hERG, AMES, LogP, clearance proxies) |

## Sister repos (the AIDD stack)

| Repo | Role |
|---|---|
| [mrnavax](https://github.com/rollroyces/mrnavax) | Core mRNA design — sequence, variant, neoantigen, scRNA, spatial, trial, LNP, manufacture, AlphaGenome Atlas, AlphaMissense |
| [mrnavax-rare](https://github.com/rollroyces/mrnavax-rare) (this) | Rare-disease track — protein replacement + editing modality + **AAV gene therapy (v0.10)** |
| [alphagenome-scn1a-pipeline](https://github.com/rollroyces/alphagenome-scn1a-pipeline) | AlphaGenome re-scoring of ClinVar VUS — pattern source for indication-aware target prioritization |
| [deepcatch](https://github.com/rollroyces/deepcatch) | cfDNA fragmentomics — companion biomarker for rare-disease trials when somatic readout exists |
| [deepcatch-methylation](https://github.com/rollroyces/deepcatch-methylation) | cfRNA read-side companion — consumes cfRNA persistence predictions from this repo for real-time chronic-disease management |

## Quick start

```bash
pip install -e ".[all]"

# AAV vector design (v0.10)
python -c "
from mrnavax_rare.aav import design_aav, AAVSpec
spec = design_aav(
    target_gene='CFTR',
    cds_wildtype='ATG' + 'C'*4437,  # 4,443 bp real CFTR CDS
    tissue='lung',
)
print(spec.capsid, spec.packaging_status, spec.payload_length_bp)
"

# LNP-mRNA design (v0.5–v0.9)
python -c "
from mrnavax_rare.design import design_mrna
spec = design_mrna(target_gene='CFTR', modality_track='L1-protein-replacement')
print(spec.manufacturability_score)
"

# cfRNA persistence prediction → real-time CDM feature (couples to deepcatch-methylation)
python -c "
from mrnavax_rare.safety.cfrna import predict_cfrna_persistence
pred = predict_cfrna_persistence(cds='ATG'+'A'*100, target_tissue='liver')
print(pred.as_dict())
"
```

## Architecture

```
mrnavax-rare/
├── pyproject.toml
├── mrnavax_rare/                 # stdlib-only core
│   ├── __init__.py               # SUBSYSTEMS tuple, __version__
│   ├── backends.py               # deterministic structural integrity checks
│   ├── indication/               # disease → gene + mutation-class facts
│   ├── target_protein/           # gene → structure context (Boltz)
│   ├── modality/                 # mutation class → mRNA-modality recommendation
│   ├── safety/                   # TDC ADMET + cfRNA persistence + sweat chloride
│   ├── design/                   # LNP-mRNA codon + UTR + LNP + manufacture
│   │   └── variant_injector.py   # HGVS-C → CDS (used by design + AAV)
│   ├── aav/                      # v0.10 — AAV vector design (sibling to design)
│   ├── trial/                    # trialgpt-simicl matcher + 9-entry corpus
│   └── config/                   # boltz_discovery, tdc_discovery shims
├── tests/                        # 256 + 1 tests, 0 regressions
├── examples/
├── docs/
├── scripts/
└── paper/                        # v0.7 → v0.9 paper draft (~6,000 words)
```

Backend adapters plug in through a `typing.Protocol` registry with stdlib mocks, mirroring the
mrnavax pattern. CI runs without heavy model weights; production users opt in via `pip install -e ".[…]"`.

## Status

| Version | Date | Scope |
|---|---|---|
| **v0.10.0** | 2026-10-14 | 9 subsystems shipped. Adds the **AAV vector design** subsystem (capsid + ITR-flanked transgene cassette, sibling to LNP-mRNA `design`). Trial corpus extended to 9 entries (5 CF + 2 PCCA/OTC Moderna mRNA-IV + 2 Dravet Stoke). |
| **v0.0.1** | 2026-10-11 | Skeleton: pyproject, README, mkdocs config, CI, stdlib-only `__init__`. |

Followed by week-1 warmups, then v0.1.0 with the first 3 tools (`indication`, `target-protein`, `modality`) on real data.

## License

Dual-licensed. AGPL-3.0-or-later for open use; commercial license available on request.
See `LICENSE` and `LICENSE-AGPL`.

## Related

- [Plan: AIDD starter roadmap](../../aidd-starter-roadmap.md) — the strategic context for this project.
- [deepcatch-methylation](https://github.com/rollroyces/deepcatch-methylation) — cfRNA read-side companion (v0.10.0 coupling via `cfrna_coupling.couple_cfrna_to_cdm`).
