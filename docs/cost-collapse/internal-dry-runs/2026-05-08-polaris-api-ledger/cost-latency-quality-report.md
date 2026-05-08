# Cost, Latency, And Task-Quality Report

## Artifact

- artifact id: dry-run-optimized-artifact-v0
- artifact type: trace dataset with eval harness
- creator: Polaris internal dry run
- competition id: bittensor-subnet-analyst-compression

## Baseline

- Polaris workflow id: polaris-cost-collapse-dry-run-v0
- trace window: 2026-05-08T16:29:42Z..2026-05-08T16:29:48Z
- median credits per task: 1.0
- median latency seconds: 120.0
- failure rate: 0.0
- baseline deployment link: https://polaris.computer/deploy/dry-run-optimized-artifact-v0
- baseline proof: https://api.polaris.computer/api/cost-collapse/proof/d13a313a-01f9-4d26-b1a6-69e61620ad37

## Optimized Artifact

- one-click Polaris deployment link: https://polaris.computer/deploy/dry-run-optimized-artifact-v0
- attribution URL: https://api.polaris.computer/api/cost-collapse/attribution/dry-run-optimized-artifact-v0
- optimized proof: https://api.polaris.computer/api/cost-collapse/proof/c32c1055-cd0b-4915-b72a-01dbbfafd37e
- eval proof: https://api.polaris.computer/api/cost-collapse/proof/2edaa951-81e1-424a-9e9f-f4f75fa5f78b
- health URL: https://api.polaris.computer/health
- ready URL: https://api.polaris.computer/health
- runtime profile: cost-collapse-dry-run

## Eval

- held-out eval id: cost-collapse-internal-ledger-dry-run-v0
- eval command: `python3 scripts/cost-collapse/record_dry_run.py --base-url https://api.polaris.computer`
- number of tasks: 1 dry-run fixture
- outcome retention: 0.90
- citation correctness: 0.90
- risk-detection score: 0.90
- demand-vs-supply score: 0.90

## Delta

| Metric | Baseline | Optimized | Delta |
|---|---:|---:|---:|
| credits per task | 1.00 | 0.35 | 65% lower |
| latency seconds | 120.0 | 45.0 | 62.5% lower |
| failure rate | 0.0 | 0.0 | no change |
| outcome quality | 1.00 | 0.90 | 10% lower |
| citation correctness | 1.00 | 0.90 | 10% lower |

## Known Tradeoffs

This dry run validates Polaris run records, proof links, attribution links, and exclusion logic. It does not prove a real model improvement or external demand.

## Maintenance Plan

Re-run after changes to Polaris cost-collapse endpoints, Cathedral preflight, reward eligibility flags, or artifact manifest schema.
