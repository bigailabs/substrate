import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = REPO_ROOT / "scripts" / "pom0" / "preflight.py"
STARTER = REPO_ROOT / "docs" / "pom0-model-factory" / "starter-kit"


def run_preflight(manifest: Path, root: Path):
    return subprocess.run(
        [sys.executable, str(PREFLIGHT), str(manifest), "--root", str(root)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


class POM0PreflightTests(unittest.TestCase):
    def test_pom0_example_manifest_passes(self):
        result = run_preflight(STARTER / "submission-manifest.example.json", STARTER)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS submission is eligible for POM-0 scoring intake", result.stdout)

    def test_pom0_score_only_manifest_fails(self):
        fixture = REPO_ROOT / "tests" / "pom0" / "fixtures" / "invalid-score-only" / "submission-manifest.json"
        result = run_preflight(fixture, fixture.parent)

        self.assertEqual(result.returncode, 1)
        self.assertIn("not_leaderboard_only", result.stdout)
        self.assertIn("paths must be an object", result.stdout)

    def test_pom0_hash_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            for name in ["submission-manifest.example.json", "pom0-report.json", "student_model.json", "job-spec.json"]:
                (tmp_path / name).write_bytes((STARTER / name).read_bytes())

            manifest_path = tmp_path / "submission-manifest.example.json"
            data = json.loads(manifest_path.read_text())
            data["artifact"]["sha256"] = "1" * 64
            manifest_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
            result = run_preflight(manifest_path, tmp_path)

        self.assertEqual(result.returncode, 1)
        self.assertIn("artifact.sha256 does not match paths.artifact", result.stdout)


if __name__ == "__main__":
    unittest.main()
