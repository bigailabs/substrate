# Miner Brief: Bittensor Subnet Analyst Compression

## Competition

Make a Polaris-hosted Bittensor subnet analyst workflow cheaper, faster, or better without losing the useful output.

Prompt:

> This Polaris-hosted analyst costs X credits and takes Y seconds to answer Z. Find the smallest intervention that preserves the outcome for less.

## Baseline Workflow

The baseline analyst answers subnet research questions using Bittensor chat evidence, repo metadata, chain state, and public docs. A useful answer must cite evidence, separate demand from supply, flag reliability risk, and state what would change the conclusion.

Baseline fields to freeze before public launch:

- Polaris workflow id
- baseline trace window
- baseline median credits per task
- baseline median latency
- baseline failure rate
- held-out task set id

## Target Task

Answer hidden subnet-analysis prompts such as:

- Which subnet looks most useful for a new agent workflow, and why?
- Where does a subnet show demand instead of induced supply?
- What reliability or incentive failure mode is most likely?
- Which evidence is stale, missing, or contradicted?

## Allowed Interventions

Miners may submit:

- distilled small analyst model
- LoRA or adapter
- routing policy that calls the expensive model only on hard cases
- prompt-compression recipe
- evidence retrieval pack
- cheaper subnet-risk judge
- cached tool-plan policy
- trace dataset paired with a deployable eval harness
- failure diagnosis that removes unnecessary expensive work

## Required Output

Every submission must include:

- `job-spec.yaml`
- `submission-manifest.json`
- `cost-latency-quality-report.md`
- held-out eval result artifact
- deployed optimized artifact or deployable harness
- one-click Polaris deployment link
- usage attribution path

## Reward Tiers

| Tier | What it means | Gate |
|---|---|---|
| Eligible | Artifact can be scored | Preflight passes and deployment link works |
| Quality bonus | Artifact preserves useful output | Hidden eval meets minimum retention |
| Cost bonus | Artifact reduces cost or latency | Reported delta verifies under Cathedral control |
| Usage bonus | Other users deploy it | Attributed external usage and credit spend |
| Maintenance | Artifact keeps earning | It remains deployable and does not drift |

## Disqualifiers

- model-only artifact
- public benchmark only
- missing Polaris deploy link
- missing usage attribution path
- eval result not reproducible from the job spec
- quality loss hidden by cost-only reporting
- miner self-deploy counted as demand
- creator-owned, refunded, or abuse-flagged usage counted as usage bonus

## Handoff To Demand Side

Accepted artifacts move to demand validation only after eligibility passes. Demand validation tests whether a real external user deploys it, understands the tradeoff, and would repeat usage.
