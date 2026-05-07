# Scoring And Disqualification

## Scoring Inputs

| Input | Description | Required |
|---|---|---|
| outcome retention | Held-out task quality vs baseline | Yes |
| citation correctness | Evidence is cited and not hallucinated | Yes |
| demand reasoning | Separates customer demand from induced supply | Yes |
| risk detection | Flags reliability, incentive, and attribution risk | Yes |
| cost reduction | Credits per task vs baseline | Yes |
| latency reduction | Seconds per task vs baseline | Yes |
| failure rate | Failed or unusable outputs vs baseline | Yes |
| deployment reliability | Polaris deployment works repeatedly | Yes |
| external usage | Non-creator deploys and credit spend | Bonus |

## Suggested Score Shape

Eligibility is binary. If eligibility fails, no score is published.

For eligible submissions:

- quality gate: minimum 0.85 outcome retention
- citation gate: no fabricated evidence in held-out samples
- cost score: baseline credits per task divided by optimized credits per task
- latency score: baseline seconds divided by optimized seconds
- robustness penalty: hidden-eval failure rate and obvious gaming attempts
- usage bonus: external attributed paid usage after deployment

## Disqualification Rules

Disqualify a submission if it:

- cannot be reproduced from the job spec
- lacks a working Polaris deployment link
- lacks a usage attribution path
- submits only a model card, dataset, notebook, or public benchmark score
- hides material quality loss
- requires manual founder setup
- counts miner-owned usage as external demand
- uses refunded, platform-owned, or abuse-flagged credits for usage bonus
- leaks private eval tasks or trains directly on hidden labels
- breaks after the first run and is not repaired inside the maintenance window

## Maintenance Rule

Passing once does not create permanent emissions. Base rewards decay unless the artifact remains deployable, passes maintenance checks, or earns real attributed usage.
