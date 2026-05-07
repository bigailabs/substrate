# Preflight Eligibility Checklist

Use this checklist before a submission enters Cathedral scoring.

## Required Files

- [ ] `job-spec.yaml` exists and describes how to reproduce the artifact.
- [ ] `submission-manifest.json` follows the v1 schema.
- [ ] `cost-latency-quality-report.md` includes baseline and optimized metrics.
- [ ] held-out eval result file exists.
- [ ] artifact or deployable harness exists.

## Deployment

- [ ] one-click Polaris deployment link is present.
- [ ] health URL is present.
- [ ] ready URL is present.
- [ ] usage attribution URL is present.
- [ ] artifact event name is present.

## Metrics

- [ ] optimized credits per task are lower than baseline credits per task.
- [ ] optimized latency is lower than baseline latency, or the quality report explains why latency increased.
- [ ] outcome retention is at least the competition threshold.
- [ ] citation correctness is reported.
- [ ] known tradeoffs are disclosed.

## Disqualifiers

- [ ] not model-only
- [ ] not public-benchmark-only
- [ ] not dataset-only
- [ ] reproducible from job spec
- [ ] does not count self-deploy usage as demand

## Result

Preflight passing means eligible for scoring. It does not mean the artifact wins or deserves emissions.
