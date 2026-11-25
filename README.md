# How Are Multi-Adapter LLM Serving Systems Evaluated? Data and scripts

Data release for the paper "How Are Multi-Adapter LLM Serving Systems Evaluated? An Empirical Study of Baselines, Workloads and Artifacts in 62 Multi-LoRA Serving Papers" (Georgii Kliukovkin, 2026).

## Contents

| Path | What it is |
|---|---|
| `data/systems.csv`, `data/systems.py` | The coded table: one row per system (62 rows). Every number in the paper is computed from it. Field legend at the top of `systems.py`. |
| `data/coded_records_second_pass.json` | Per-paper records with the second-pass corrections. |
| `data/coded_records_added.jsonl`, `data/coded_records_added_2026-11-24.jsonl` | Records for systems added after the first pass. |
| `data/coding_schema.md` | The 25-field coding schema. |
| `data/repo_audit_2026-11-23.jsonl`, `data/repos_opened_2026-11-24.jsonl` | Repository and artifact audit. |
| `data/engine_docs_check.md` | What engine and orchestration-layer documentation states about multi-adapter serving. |
| `data/search_log.md` | Search queries and screening log. |
| `census/` | Census of public LoRA adapters on the Hugging Face Hub (24 November 2026): listing, summary tables, collection scripts. |
| `scripts/stats.py` | Recomputes the corpus statistics: `python3 scripts/stats.py systems` (run from `data/`). |
| `scripts/build2.py`, `scripts/fig1.py`, `scripts/selfcheck.py` | Table and figure generation and the consistency check used for the paper. |

## Caveats

The coding was done by one author with model assistance and a second pass over 52 of the 62 papers; accuracy of the coded fields after the second pass was not measured. Three records were coded once from publisher pages, one of them from four of eleven pages. Repository facts are as of 23 to 25 November 2026. See the Methodology and Limits sections of the paper.

Corrections are welcome: open an issue with the system name, the field, and the passage of the paper that supports the change.

## License

Data and documentation: CC BY 4.0. Scripts: MIT.

## Citation

```bibtex
@misc{kliukovkin2026multiadapter,
  author = {Kliukovkin, Georgii},
  title  = {How Are Multi-Adapter LLM Serving Systems Evaluated? An Empirical Study of Baselines, Workloads and Artifacts in 62 Multi-LoRA Serving Papers},
  year   = {2026},
  note   = {arXiv preprint}
}
```
