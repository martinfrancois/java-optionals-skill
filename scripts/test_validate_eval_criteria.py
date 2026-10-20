#!/usr/bin/env python3
"""Fixture tests for the invocation rules in validate_eval_criteria.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_eval_criteria.py"


def task(prompt: str) -> str:
    return f"# Fixture\n\nCreate `Example.java`. Assume Java 17.\n\n{prompt}\n"


def checklist() -> list[dict[str, object]]:
    return [
        {"name": "Creates artifact", "category": "safety", "max_score": 5, "description": "Creates Example.java."},
        {"name": "Preserves behavior", "category": "safety", "max_score": 5, "description": "Returns the requested output."},
        {"name": "Uses Optional well", "category": "optional_quality", "max_score": 85, "description": "Binds the value once."},
        {"name": "Keeps it focused", "category": "maintainability", "max_score": 5, "description": "Adds nothing unrequested."},
    ]


def write_scenario(root: Path, suite: str, name: str, prompt: str, invocation: str = "natural") -> Path:
    scenario = root / suite / name
    scenario.mkdir(parents=True)
    (scenario / "task.md").write_text(task(prompt), encoding="utf-8")
    (scenario / "capability.txt").write_text("java-optionals\n", encoding="utf-8")
    items = checklist()
    categories = {item["name"]: item.pop("category") for item in items}
    criteria = {"context": "Fixture scenario.", "type": "weighted_checklist", "checklist": items}
    (scenario / "criteria.json").write_text(json.dumps(criteria, indent=2) + "\n", encoding="utf-8")
    metadata = {"invocation": invocation, "task_type": "implementation", "evidence_type": "ordinary_lift"}
    (scenario / "criteria-meta.json").write_text(
        json.dumps({"metadata": metadata, "categories": categories}, indent=2) + "\n", encoding="utf-8"
    )
    return scenario


class InvocationRuleTests(unittest.TestCase):
    def run_validator(self, root: Path, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *(str(path.relative_to(root)) for path in paths)],
            cwd=root, text=True, capture_output=True, check=False,
        )

    def test_main_without_natural_scenario_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-explicit", "Use `$java-optionals` to tidy `Example`.", "explicit")
            result = self.run_validator(root, root / "evals")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must include a natural invocation scenario", result.stderr)

    def test_main_alone_with_only_natural_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", "Tidy `Example` for readability.")
            result = self.run_validator(root, root / "evals")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_main_and_reference_need_both_invocation_styles(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", "Tidy `Example` for readability.")
            write_scenario(root, "evals-reference", "02-natural", "Clean up `Other` for readability.")
            missing = self.run_validator(root, root / "evals", root / "evals-reference")
            write_scenario(root, "evals-reference", "03-explicit", "Use `$java-optionals` to tidy `Third`.", "explicit")
            both = self.run_validator(root, root / "evals", root / "evals-reference")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("both natural and explicit invocation scenarios", missing.stderr)
        self.assertEqual(both.returncode, 0, both.stderr)

    def test_task_names_skill_but_metadata_says_natural_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scenario = write_scenario(root, "evals-reference", "26-mixed", "Use `$java-optionals` to tidy `Example`.")
            result = self.run_validator(root, scenario)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("natural scenario explicitly invokes the skill", result.stderr)


if __name__ == "__main__":
    unittest.main()
