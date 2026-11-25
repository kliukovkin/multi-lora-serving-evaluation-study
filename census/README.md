# Census of public LoRA adapters on the Hugging Face Hub (24 November 2026)

`data/census.jsonl.gz` (gzip): one record per repository tagged `base_model:adapter:<model>` for seven base models (8,530 repositories; 7,077 with a readable `adapter_config.json` at the repository root, 7,051 of them LoRA with a valid rank; 1,246 without a configuration at the root; 207 gated). Fields: base model tag, repository id, downloads (preceding 30 days), likes, creation date, configuration status, PEFT type, rank, alpha, target modules, DoRA and rsLoRA flags, adapter file size.

`scripts/census.py` collects the listing through the public Hub API; `scripts/analyze.py` produces the summary statistics quoted in the paper.

Limits: the adapter tag is set by repository authors and can be wrong; ten authors contribute 32% of the sample; checkpoints of one training run and duplicates are not removed; downloads are not request traffic; one snapshot.
