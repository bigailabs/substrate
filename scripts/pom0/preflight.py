#!/usr/bin/env python3
"""Preflight a Cathedral POM-0 ModelFactory submission manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlparse


SCHEMA_VERSION = "cathedral.pom0.submission_manifest.v1"
REPORT_SCHEMA_VERSION = "polaris.model_factory.pom0.report.v1"
COMPETITION_ID = "pom0-model-factory-issue-router"
ALLOWED_TYPES = {
    "distilled_model",
    "lora_adapter",
    "router",
    "prompt_compression_recipe",
    "specialized_judge",
    "cached_tool_plan_policy",
    "trace_dataset_with_eval_harness",
}
REQUIRED_PATHS = {"job_spec", "report", "artifact"}
REQUIRED_ATTESTATIONS = {
    "not_leaderboard_only",
    "not_public_benchmark_only",
    "reproducible_from_job_spec",
    "does_not_count_self_deploy_as_demand",
    "artifact_hash_matches",
}
MIN_QUALITY_RETENTION = 0.95


def nested(data: dict, path: str):
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_rate(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0 <= value <= 1


def is_positive_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def is_https_url_or_none(value: object) -> bool:
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def resolve_manifest_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_file():
        digest.update(path.read_bytes())
        return digest.hexdigest()
    if path.is_dir():
        for child in sorted(p for p in path.rglob("*") if p.is_file()):
            digest.update(str(child.relative_to(path)).encode("utf-8"))
            digest.update(b"\0")
            digest.update(child.read_bytes())
            digest.update(b"\0")
        return digest.hexdigest()
    raise FileNotFoundError(path)


def load_json(path: Path, failures: list[str], label: str) -> dict | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        failures.append(f"{label} not found: {path}")
    except json.JSONDecodeError as exc:
        failures.append(f"{label} is not valid JSON: {exc}")
    return None


def validate(data: dict, manifest_path: Path, root: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    if nested(data, "schema_version") != SCHEMA_VERSION:
        failures.append(f"schema_version must be {SCHEMA_VERSION}")

    if nested(data, "competition_id") != COMPETITION_ID:
        failures.append(f"competition_id must be {COMPETITION_ID}")

    artifact_type = nested(data, "artifact.type")
    if artifact_type not in ALLOWED_TYPES:
        failures.append(f"artifact.type must be one of: {', '.join(sorted(ALLOWED_TYPES))}")

    summary = nested(data, "artifact.summary")
    if not isinstance(summary, str) or len(summary.strip()) < 30:
        failures.append("artifact.summary must explain the intervention in at least 30 characters")

    artifact_sha = nested(data, "artifact.sha256")
    if not isinstance(artifact_sha, str) or len(artifact_sha) != 64:
        failures.append("artifact.sha256 must be a 64-character sha256 hex digest")

    paths = nested(data, "paths")
    resolved_paths: dict[str, Path] = {}
    if not isinstance(paths, dict):
        failures.append("paths must be an object")
    else:
        for key in REQUIRED_PATHS:
            resolved = resolve_manifest_path(root, paths.get(key))
            if resolved is None:
                failures.append(f"paths.{key} is required")
            elif not resolved.exists():
                failures.append(f"paths.{key} does not exist: {resolved}")
            else:
                resolved_paths[key] = resolved

    report = None
    if "report" in resolved_paths:
        report = load_json(resolved_paths["report"], failures, "report")
        if report and report.get("schema_version") != REPORT_SCHEMA_VERSION:
            failures.append(f"report.schema_version must be {REPORT_SCHEMA_VERSION}")

    if "artifact" in resolved_paths and isinstance(artifact_sha, str) and len(artifact_sha) == 64:
        actual_hash = sha256_path(resolved_paths["artifact"])
        if actual_hash != artifact_sha:
            failures.append("artifact.sha256 does not match paths.artifact")

    if report:
        report_hash = nested(report, "artifact.sha256")
        if isinstance(artifact_sha, str) and report_hash != artifact_sha:
            failures.append("report.artifact.sha256 must match manifest artifact.sha256")

    metrics = nested(data, "metrics")
    if not isinstance(metrics, dict):
        failures.append("metrics must be an object")
    else:
        if not is_rate(metrics.get("quality_retention")):
            failures.append("metrics.quality_retention must be between 0 and 1")
        elif float(metrics["quality_retention"]) < MIN_QUALITY_RETENTION:
            failures.append(f"metrics.quality_retention must be at least {MIN_QUALITY_RETENTION}")
        if not is_positive_number(metrics.get("latency_speedup")) or float(metrics["latency_speedup"]) <= 1:
            failures.append("metrics.latency_speedup must be greater than 1")
        if not is_rate(metrics.get("serving_cost_reduction")) or float(metrics["serving_cost_reduction"]) <= 0:
            failures.append("metrics.serving_cost_reduction must be greater than 0 and at most 1")
        if not is_positive_number(metrics.get("student_artifact_bytes")):
            failures.append("metrics.student_artifact_bytes must be a positive number")

    deployment = nested(data, "deployment")
    if not isinstance(deployment, dict):
        failures.append("deployment must be an object")
    else:
        status = deployment.get("status")
        if status not in {"local_artifact", "deployed"}:
            failures.append("deployment.status must be local_artifact or deployed")
        if status == "deployed" and not is_https_url_or_none(deployment.get("one_click_polaris_url")):
            failures.append("deployment.one_click_polaris_url must be an https URL when deployed")
        if status == "local_artifact":
            warnings.append("deployment is local_artifact, so this is eligible for dry-run scoring only")

    attribution = nested(data, "usage_attribution")
    if not isinstance(attribution, dict):
        failures.append("usage_attribution must be an object")
    else:
        if attribution.get("status") not in {"pending", "active"}:
            failures.append("usage_attribution.status must be pending or active")
        if not isinstance(attribution.get("artifact_event_name"), str) or not attribution["artifact_event_name"].strip():
            failures.append("usage_attribution.artifact_event_name is required")
        for key in [
            "exclude_creator_owned_usage",
            "exclude_platform_owned_usage",
            "exclude_refunded_usage",
            "exclude_abuse_flagged_usage",
        ]:
            if attribution.get(key) is not True:
                failures.append(f"usage_attribution.{key} must be true")

    attestations = nested(data, "disqualifier_attestations")
    if not isinstance(attestations, dict):
        failures.append("disqualifier_attestations must be an object")
    else:
        for key in REQUIRED_ATTESTATIONS:
            if attestations.get(key) is not True:
                failures.append(f"disqualifier_attestations.{key} must be true")

    if failures:
        warnings.append("preflight failing means the submission is ineligible for POM-0 scoring")
    elif manifest_path.name == "submission-manifest.example.json":
        warnings.append("example manifest passes shape checks, replace placeholders before real submission")

    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight a Cathedral POM-0 ModelFactory submission manifest.")
    parser.add_argument("manifest", type=Path, help="Path to submission-manifest.json")
    parser.add_argument("--root", type=Path, default=None, help="Root directory used to resolve relative file paths")
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    root = (args.root.resolve() if args.root else manifest_path.parent.resolve())
    failures: list[str] = []
    data = load_json(manifest_path, failures, "manifest")
    if data is None:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 2

    failures, warnings = validate(data, manifest_path, root)

    print("Cathedral POM-0 preflight")
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

    print("\nPASS submission is eligible for POM-0 scoring intake")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
