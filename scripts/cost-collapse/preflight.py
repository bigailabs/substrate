#!/usr/bin/env python3
"""Preflight a Cathedral cost-collapse submission manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_TYPES = {
    "distilled_model",
    "lora_adapter",
    "router",
    "prompt_compression_recipe",
    "specialized_judge",
    "cached_tool_plan_policy",
    "retrieval_pack",
    "trace_dataset_with_eval_harness",
    "failure_diagnosis",
}

REQUIRED_ATTESTATIONS = {
    "not_model_only",
    "not_public_benchmark_only",
    "not_dataset_only",
    "reproducible_from_job_spec",
    "does_not_count_self_deploy_as_demand",
}

REQUIRED_PATHS = {
    "job_spec",
    "report",
    "eval_results",
    "artifact",
}

MIN_OUTCOME_RETENTION = 0.85
MIN_CITATION_CORRECTNESS = 0.85


def nested(data: dict, path: str):
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_https_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def is_positive_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def is_rate(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1


def resolve_manifest_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def validate(data: dict, manifest_path: Path, root: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    if nested(data, "schema_version") != "cathedral.cost_collapse.submission_manifest.v1":
        failures.append("schema_version must be cathedral.cost_collapse.submission_manifest.v1")

    if nested(data, "competition_id") != "bittensor-subnet-analyst-compression":
        failures.append("competition_id must be bittensor-subnet-analyst-compression")

    artifact_type = nested(data, "artifact.type")
    if artifact_type not in ALLOWED_TYPES:
        failures.append(f"artifact.type must be one of: {', '.join(sorted(ALLOWED_TYPES))}")

    summary = nested(data, "artifact.summary")
    if not isinstance(summary, str) or len(summary.strip()) < 20:
        failures.append("artifact.summary must explain the intervention in at least 20 characters")

    for field in [
        "deployment.one_click_polaris_url",
        "deployment.health_url",
        "deployment.ready_url",
        "usage_attribution.attribution_url",
    ]:
        if not is_https_url(nested(data, field)):
            failures.append(f"{field} must be an https URL")

    polaris_url = nested(data, "deployment.one_click_polaris_url")
    if isinstance(polaris_url, str) and "polaris" not in urlparse(polaris_url).netloc:
        warnings.append("deployment.one_click_polaris_url does not appear to point at a Polaris host")

    paths = nested(data, "paths")
    if not isinstance(paths, dict):
        failures.append("paths must be an object")
    else:
        for key in REQUIRED_PATHS:
            resolved = resolve_manifest_path(root, paths.get(key))
            if resolved is None:
                failures.append(f"paths.{key} is required")
            elif not resolved.exists():
                failures.append(f"paths.{key} does not exist: {resolved}")

    metrics = nested(data, "metrics")
    if not isinstance(metrics, dict):
        failures.append("metrics must be an object")
    else:
        for key in [
            "baseline_credits_per_task",
            "optimized_credits_per_task",
            "baseline_latency_seconds",
            "optimized_latency_seconds",
        ]:
            if not is_positive_number(metrics.get(key)):
                failures.append(f"metrics.{key} must be a positive number")
        for key in ["baseline_failure_rate", "optimized_failure_rate"]:
            if not is_rate(metrics.get(key)):
                failures.append(f"metrics.{key} must be between 0 and 1")

        baseline_cost = metrics.get("baseline_credits_per_task")
        optimized_cost = metrics.get("optimized_credits_per_task")
        if is_positive_number(baseline_cost) and is_positive_number(optimized_cost):
            if optimized_cost >= baseline_cost:
                failures.append("optimized_credits_per_task must be lower than baseline_credits_per_task")

        baseline_latency = metrics.get("baseline_latency_seconds")
        optimized_latency = metrics.get("optimized_latency_seconds")
        if is_positive_number(baseline_latency) and is_positive_number(optimized_latency):
            if optimized_latency > baseline_latency:
                warnings.append("optimized latency is higher than baseline latency, demand handoff must explain why")

        baseline_failure = metrics.get("baseline_failure_rate")
        optimized_failure = metrics.get("optimized_failure_rate")
        if is_rate(baseline_failure) and is_rate(optimized_failure):
            allowed_failure = max(float(baseline_failure) + 0.05, float(baseline_failure) * 1.5)
            if float(optimized_failure) > allowed_failure:
                failures.append("optimized_failure_rate increases too much vs baseline_failure_rate")

    quality = nested(data, "quality")
    if not isinstance(quality, dict):
        failures.append("quality must be an object")
    else:
        if not is_rate(quality.get("outcome_retention")):
            failures.append("quality.outcome_retention must be between 0 and 1")
        elif float(quality["outcome_retention"]) < MIN_OUTCOME_RETENTION:
            failures.append(f"quality.outcome_retention must be at least {MIN_OUTCOME_RETENTION}")

        if not is_rate(quality.get("citation_correctness")):
            failures.append("quality.citation_correctness must be between 0 and 1")
        elif float(quality["citation_correctness"]) < MIN_CITATION_CORRECTNESS:
            failures.append(f"quality.citation_correctness must be at least {MIN_CITATION_CORRECTNESS}")

        tradeoffs = quality.get("known_tradeoffs")
        if not isinstance(tradeoffs, str) or len(tradeoffs.strip()) < 20:
            failures.append("quality.known_tradeoffs must disclose material tradeoffs")

    attribution = nested(data, "usage_attribution")
    if not isinstance(attribution, dict):
        failures.append("usage_attribution must be an object")
    else:
        if attribution.get("exclude_creator_owned_usage") is not True:
            failures.append("usage_attribution.exclude_creator_owned_usage must be true")
        if not isinstance(attribution.get("artifact_event_name"), str) or not attribution["artifact_event_name"].strip():
            failures.append("usage_attribution.artifact_event_name is required")

    attestations = nested(data, "disqualifier_attestations")
    if not isinstance(attestations, dict):
        failures.append("disqualifier_attestations must be an object")
    else:
        for key in REQUIRED_ATTESTATIONS:
            if attestations.get(key) is not True:
                failures.append(f"disqualifier_attestations.{key} must be true")

    if failures:
        warnings.append("preflight failing means the submission is ineligible for scoring")
    elif manifest_path.name == "submission-manifest.example.json":
        warnings.append("example manifest passes shape checks, replace placeholders before real submission")

    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight a Cathedral cost-collapse submission manifest.")
    parser.add_argument("manifest", type=Path, help="Path to submission-manifest.json")
    parser.add_argument("--root", type=Path, default=None, help="Root directory used to resolve relative file paths")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    root = (args.root.resolve() if args.root else manifest_path.parent.resolve())

    try:
        data = json.loads(manifest_path.read_text())
    except FileNotFoundError:
        print(f"FAIL manifest not found: {manifest_path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"FAIL manifest is not valid JSON: {exc}", file=sys.stderr)
        return 2

    failures, warnings = validate(data, manifest_path, root)

    print("Cathedral cost-collapse preflight")
    print(f"manifest: {manifest_path}")
    print(f"root: {root}")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  WARN {warning}")

    if failures:
        print("\nFailures:")
        for failure in failures:
            print(f"  FAIL {failure}")
        return 1

    print("\nPASS submission is eligible for scoring intake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
