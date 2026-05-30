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

cat "$output_file"

if grep -q "already exists" "$output_file"; then
  echo "Publish dry-run reached the registry; current version already exists."
  rm -f "$output_file"
  exit 0
fi

rm -f "$output_file"
exit "$status"
