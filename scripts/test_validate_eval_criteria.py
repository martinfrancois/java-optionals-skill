#!/usr/bin/env python3
"""Fixture tests for the invocation and runtime-reference overlap rules in validate_eval_criteria.py."""

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


def write_scenario(
    root: Path,
    suite: str,
    name: str,
    prompt: str,
    invocation: str = "natural",
    rationale: str | None = None,
    evidence_type: str = "ordinary_lift",
) -> Path:
    scenario = root / suite / name
    scenario.mkdir(parents=True)
    (scenario / "task.md").write_text(task(prompt), encoding="utf-8")
    (scenario / "capability.txt").write_text("java-optionals\n", encoding="utf-8")
    items = checklist()
    categories = {item["name"]: item.pop("category") for item in items}
    criteria = {"context": "Fixture scenario.", "type": "weighted_checklist", "checklist": items}
    (scenario / "criteria.json").write_text(json.dumps(criteria, indent=2) + "\n", encoding="utf-8")
    metadata = {"invocation": invocation, "task_type": "implementation", "evidence_type": evidence_type}
    if rationale is not None:
        metadata["runtime_reference_overlap_rationale"] = rationale
    (scenario / "criteria-meta.json").write_text(
        json.dumps({"metadata": metadata, "categories": categories}, indent=2) + "\n", encoding="utf-8"
    )
    return scenario


class ValidatorTestCase(unittest.TestCase):
    def write_references(self, root: Path, text: str) -> None:
        references = root / "skills" / "java-optionals" / "references"
        references.mkdir(parents=True, exist_ok=True)
        (references / "examples.md").write_text(f"# Examples\n\n{text}\n", encoding="utf-8")

    def run_validator(self, root: Path, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *(str(path.relative_to(root)) for path in paths)],
            cwd=root, text=True, capture_output=True, check=False,
        )


class InvocationRuleTests(ValidatorTestCase):
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


COPIED_EXAMPLE = (
    "```java\n"
    "Optional<Workspace> chosen = configuredWorkspace(options)\n"
    "        .or(() -> environmentWorkspace(environment))\n"
    "        .map(workspace -> workspace.withRegion(defaultRegion))\n"
    "        .filter(Workspace::isActive);\n"
    "return chosen.map(Workspace::displayName).orElseGet(fallbackNames::next);\n"
    "```"
)
IMPORTS = (
    "package com.example.workspace;\n\n"
    "import java.nio.file.Files;\n"
    "import java.nio.file.Path;\n"
    "import java.util.Optional;\n"
    "import java.util.concurrent.atomic.AtomicInteger;\n"
    "import java.util.function.Supplier;\n"
)
NEAR_CALL = "```java\nledgerTotal(invoiceLines, discountRate);\n```"
NEAR_REFERENCE = "```java\nreturn ledgerTotal(invoiceLines, discountRate);\n```"


class RuntimeReferenceOverlapTests(ValidatorTestCase):
    def test_main_task_copying_runtime_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", f"Tidy this lookup.\n\n{COPIED_EXAMPLE}")
            unique = self.run_validator(root, root / "evals")
            self.write_references(root, COPIED_EXAMPLE)
            copied = self.run_validator(root, root / "evals")
        self.assertEqual(unique.returncode, 0, unique.stderr)
        self.assertNotEqual(copied.returncode, 0)
        self.assertIn("overlaps runtime references too closely", copied.stderr)

    def test_shipped_java_file_copying_runtime_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            scenario = write_scenario(root, "evals", "01-natural", "Tidy `Example.java` for readability.")
            code = COPIED_EXAMPLE.removeprefix("```java\n").removesuffix("```")
            (scenario / "Example.java").write_text(code, encoding="utf-8")
            self.write_references(root, COPIED_EXAMPLE)
            result = self.run_validator(root, root / "evals")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("overlaps runtime references too closely", result.stderr)

    def test_shared_import_lines_alone_pass(self) -> None:
        scenario_code = f"```java\n{IMPORTS}\nfinal class Ledger {{\n    int balance() {{ return 0; }}\n}}\n```"
        reference_code = f"```java\n{IMPORTS}\nfinal class Catalog {{\n    int size() {{ return 1; }}\n}}\n```"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", f"Tidy this class.\n\n{scenario_code}")
            self.write_references(root, reference_code)
            result = self.run_validator(root, root / "evals")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("warning:", result.stderr)

    def test_shared_java_keywords_and_optional_calls_do_not_warn(self) -> None:
        def holder(type_name: str, method: str, value: str) -> str:
            return (
                "```java\n"
                f"public final class {type_name} {{\n"
                f"    private static String {method}(Optional<String> {value}) {{\n"
                f"        if ({value}.isPresent()) {{ return {value}.orElseThrow(); }}\n"
                f"        return {value}.orElseGet(() -> {value}.isEmpty() ? null : this.toString());\n"
                "    }\n"
                "}\n"
                "```"
            )

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", f"Tidy this class.\n\n{holder('Ledger', 'entry', 'draft')}")
            self.write_references(root, holder("Catalog", "label", "ticket"))
            result = self.run_validator(root, root / "evals")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("warning:", result.stderr)

    def test_main_task_copying_reference_prose_fails(self) -> None:
        prose = (
            "When the fallback reads a file or asks the user, keep the explicit branch so the checked "
            "exception stays visible and the prompt runs only when no configured value exists."
        )
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", f"Tidy this resolver. {prose}")
            self.write_references(root, prose)
            result = self.run_validator(root, root / "evals")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("0 shared identifiers (none)", result.stderr)

    def test_near_overlap_warns_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-natural", f"Tidy this call.\n\n{NEAR_CALL}")
            self.write_references(root, NEAR_REFERENCE)
            result = self.run_validator(root, root / "evals")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("warning: evals/01-natural: task.md is close to runtime references", result.stderr)

    def test_reference_scenario_copying_runtime_reference_only_warns(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals-reference", "02-natural", f"Tidy this lookup.\n\n{COPIED_EXAMPLE}")
            write_scenario(
                root,
                "evals-regression",
                "03-natural",
                f"Tidy this lookup.\n\n{COPIED_EXAMPLE}",
                evidence_type="solved_regression",
            )
            self.write_references(root, COPIED_EXAMPLE)
            result = self.run_validator(root, root / "evals-reference", root / "evals-regression")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("warning: evals-reference/02-natural: task.md is close to runtime references", result.stderr)
        self.assertNotIn("evals-regression/03-natural", result.stderr)

    def test_rationale_suppresses_failure_and_warnings(self) -> None:
        rationale = "Shares names with an example, but not its code."
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            write_scenario(root, "evals", "01-copied", f"Tidy this lookup.\n\n{COPIED_EXAMPLE}", rationale=rationale)
            write_scenario(root, "evals", "02-near", f"Tidy this call.\n\n{NEAR_CALL}", rationale=rationale)
            write_scenario(
                root, "evals-reference", "03-copied", f"Clean up this lookup.\n\n{COPIED_EXAMPLE}", rationale=rationale
            )
            self.write_references(root, f"{COPIED_EXAMPLE}\n\n{NEAR_REFERENCE}")
            main = self.run_validator(root, root / "evals")
            reference = self.run_validator(root, root / "evals-reference")
        self.assertEqual(main.returncode, 0, main.stderr)
        self.assertEqual(reference.returncode, 0, reference.stderr)
        self.assertNotIn("runtime references", main.stderr + reference.stderr)


if __name__ == "__main__":
    unittest.main()
