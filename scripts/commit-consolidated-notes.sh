#!/usr/bin/env bash
set -euo pipefail

if [[ -z "$(git status --porcelain -- notes)" ]]; then
  echo "No note changes to commit."
  exit 0
fi

branch="${GITHUB_REF_NAME:?}"
patch_file="${RUNNER_TEMP:?}/consolidated-notes.patch"

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -- notes
git diff --cached --binary -- notes > "$patch_file"
git commit -m "Consolidate workspace notes"

for attempt in 1 2 3; do
  echo "Publishing consolidated notes (attempt $attempt/3)."
  git fetch origin "$branch"
  if ! git rebase FETCH_HEAD; then
    git rebase --abort
    echo "Consolidated notes conflict with newer branch changes; the generated patch is retained at $patch_file." >&2
    exit 1
  fi
  if git push origin "HEAD:$branch"; then
    exit 0
  fi
done

echo "Could not publish consolidated notes after three attempts; the generated patch is retained at $patch_file." >&2
exit 1
