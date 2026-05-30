#!/usr/bin/env python3
"""Validate local Tessl eval criteria files."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def error(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def criteria_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.name == "criteria.json":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("criteria.json")))
        else:
            raise FileNotFoundError(path)
    return sorted(files)


def validate_criteria(path: Path) -> list[str]:
    failures: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]

    if not isinstance(data, dict):
        return [f"{path}: criteria root must be an object"]

    if data.get("type") != "weighted_checklist":
        failures.append(f"{path}: type must be weighted_checklist")

    checklist = data.get("checklist")
    if not isinstance(checklist, list) or not checklist:
        failures.append(f"{path}: checklist must be a non-empty array")
        checklist = []

    for index, item in enumerate(checklist, start=1):
        if not isinstance(item, dict):
            failures.append(f"{path}: checklist item {index} must be an object")
            continue

        name = item.get("name")
        description = item.get("description")
        max_score = item.get("max_score")

        if not isinstance(name, str) or not name.strip():
            failures.append(f"{path}: checklist item {index} needs a non-empty name")
        if not isinstance(description, str) or not description.strip():
            failures.append(f"{path}: checklist item {index} needs a non-empty description")
        if not isinstance(max_score, int) or max_score <= 0:
            failures.append(f"{path}: checklist item {index} needs a positive integer max_score")

    task_file = path.with_name("task.md")
    if not task_file.is_file():
        failures.append(f"{path}: missing sibling task.md")

    return failures


def main() -> int:
    if len(sys.argv) < 2:
        return error("usage: validate_eval_criteria.py <eval-directory-or-criteria.json> [...]")

    try:
        files = criteria_files([Path(arg) for arg in sys.argv[1:]])
    except FileNotFoundError as exc:
        return error(f"path not found: {exc.filename}")

    if not files:
        return error("no criteria.json files found")

    failures: list[str] = []
    for path in files:
        failures.extend(validate_criteria(path))

    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} criteria file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
