# Invalid Submission Examples

## Model-Only Upload

Invalid:

- uploads a HuggingFace model
- cites a public benchmark
- has no Polaris deployment link
- has no usage attribution path

Why it fails:

Cathedral optimizes Polaris-hosted workflows, not standalone model leaderboards.

## Dataset-Only Upload

Invalid:

- uploads traces or labels
- has no deployable evaluator
- has no optimized artifact
- cannot run a held-out eval from the job spec

Why it fails:

Datasets are only useful when paired with a deployable evaluator, harness, or optimized artifact.

## Cost-Only Claim

Invalid:

- reduces credits per task
- hides quality loss
- does not report citation correctness or failure rate

Why it fails:

Cost collapse must preserve the target outcome. Cheap wrong answers are not eligible.

## Self-Deploy Demand

Invalid:

- creator deploys the artifact repeatedly
- credits are free, refunded, platform-owned, or abuse-flagged
- usage is presented as downstream demand

Why it fails:

Usage bonuses require external attributed usage. Creator-owned usage is learning, not demand.
