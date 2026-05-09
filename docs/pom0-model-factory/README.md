# Cathedral POM-0 ModelFactory Validation Kit

Cathedral rewards reusable model work that makes Polaris jobs cheaper, faster, smaller, or more reliable while preserving quality.

POM-0 is the first ModelFactory competition shape. It is intentionally narrow:

- one fixed task
- one teacher
- one student artifact
- one held-out eval report
- one artifact hash
- one preflight gate before validators score anything

## First Competition

The first competition is:

```text
pom0-model-factory-issue-router
```

The task routes Polaris and Cathedral operating issues into work lanes:

- core compute
- provider access
- runtime chat
- billing ledger
- model factory
- security compliance

This is not the final public model. It is the smallest validated loop for ModelFactory and Cathedral rewards.

## Eligible Submission

Every submission must include:

- reproducible job spec
- POM-0 report from Polaris ModelFactory
- deployable or local artifact
- artifact sha256 hash
- quality, latency, cost, and size metrics
- usage attribution status
- abuse-exclusion attestations

Leaderboard-only claims are not eligible.

## Local Preflight

Run:

```bash
python3 scripts/pom0/preflight.py \
  docs/pom0-model-factory/starter-kit/submission-manifest.example.json \
  --root docs/pom0-model-factory/starter-kit
```

Or:

```bash
just pom0-preflight
```

Passing preflight means the artifact is eligible for scoring intake. It does not mean the artifact wins.

## Reward Order

Validators score in this order:

1. Quality gate
2. Artifact validity and reproducibility
3. Latency, serving cost, and size improvement
4. Maintenance
5. Downstream Polaris usage, once attribution is active

Usage bonus remains pending until Polaris emits signed attribution events for deployed POM artifacts.
