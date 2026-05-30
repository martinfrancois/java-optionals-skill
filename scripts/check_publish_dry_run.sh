#!/usr/bin/env bash
set -euo pipefail

path="${1:-.}"
output_file="$(mktemp)"

if tessl plugin publish --dry-run --skip-evals "$path" >"$output_file" 2>&1; then
  cat "$output_file"
  rm -f "$output_file"
  exit 0
else
  status=$?
fi

if grep -q "already exists" "$output_file"; then
  rm -f "$output_file"
  echo "Current manifest version already exists in the registry; checking next patch version instead."
  tessl plugin publish --dry-run --skip-evals --bump patch "$path"
  echo "Publish dry-run reached the registry; next patch version is available."
  exit 0
fi

cat "$output_file"
rm -f "$output_file"
exit "$status"
