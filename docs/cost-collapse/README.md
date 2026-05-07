# Cathedral Cost-Collapse Supply Kit

Cathedral rewards reusable optimization assets that make Polaris-hosted agent workflows cheaper, faster, or better while preserving the target outcome.

This kit is the supply-side launch package for the first cost-collapse sprint.

## First Competition

The first competition is:

> Bittensor Subnet Analyst Compression

The target workflow is an expensive Polaris-hosted subnet analyst agent. Miners produce the cheapest validated intervention that preserves evidence quality, citation quality, and risk detection.

Allowed interventions include:

- model distillation
- LoRA or adapter
- router
- prompt-compression recipe
- cheaper judge
- cached tool-plan policy
- retrieval pack
- trace dataset paired with a deployable eval harness
- failure diagnosis that removes unnecessary expensive work

The winning artifact is not necessarily a model. It is the cheapest validated intervention that keeps the outcome useful.

## Eligibility Rule

Every eligible submission must include:

- reproducible job specification
- held-out task eval result
- cost, latency, and task-quality report
- one-click Polaris deployment link
- usage attribution path

Standalone HuggingFace models, public-benchmark-only improvements, datasets without deployable harnesses, and miner self-deploy usage are not eligible for rewards.

## Kit Map

- `bittensor-subnet-analyst-compression/miner-brief.md`
- `bittensor-subnet-analyst-compression/public-call.md`
- `bittensor-subnet-analyst-compression/recruiting-dm.md`
- `bittensor-subnet-analyst-compression/scoring-and-disqualification.md`
- `bittensor-subnet-analyst-compression/demand-handoff-template.md`
- `starter-kit/job-spec.template.yaml`
- `starter-kit/submission-manifest.schema.json`
- `starter-kit/submission-manifest.example.json`
- `starter-kit/cost-latency-quality-report.template.md`
- `starter-kit/preflight-eligibility-checklist.md`
- `starter-kit/invalid-submissions.md`

## Local Preflight

Run the checker before sending any submission to a validator or demand-side deployment test:

```bash
python3 scripts/cost-collapse/preflight.py \
  docs/cost-collapse/starter-kit/submission-manifest.example.json \
  --root docs/cost-collapse/starter-kit
```

The preflight checker validates the manifest shape, referenced files, required deployment and attribution links, cost and latency deltas, minimum quality retention, and disqualifier flags.

Preflight passing does not mean the artifact wins. It only means the artifact is eligible for scoring.

## Launch Gate

Do not open rewards until these fields are frozen:

- baseline Polaris workflow id
- hidden or rotating held-out eval id
- baseline cost and latency window
- minimum quality-retention threshold
- Polaris deployment link format
- usage attribution event schema
- reward tiers and decay rule

Until those exist, this package is a private dry-run kit for credible miners and builders.
