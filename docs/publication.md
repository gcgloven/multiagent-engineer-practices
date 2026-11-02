# Publishing this repository

Publish the source repository containing this document. Local workspace exports, audit records, project experiments, configuration and runtime evidence belong in the ignored `obsolete/` directory. Local tools and settings also remain excluded through `.multica`, `setup.local.toml` and the existing environment/configuration patterns.

## Review the public file set

Before the first commit, inspect both staged and untracked files:

```bash
git status --short
git ls-files --cached --others --exclude-standard
git check-ignore obsolete/README.md .multica setup.local.toml
```

The file list should contain reusable source, documentation, fictional examples, dependency pins, attribution and licenses. It should not contain real workspace IDs, user conversations, private project data, local paths, credentials or execution logs. Inspect staged content with `git diff --cached` before committing. An ignore rule does not remove a file already tracked by Git.

Run the [local validation checks](../VALIDATION.md), regenerate the bundle and inspect the generated archive members. Keep third-party license notices and source attribution in the public package.

## Export a reviewed revision

After reviewing and committing the source, export that commit:

```bash
git archive --format=tar.gz --prefix=multica-engineer-practices/ \
  -o ../multica-engineer-practices-source.tar.gz HEAD
```

Git source archives honor the supplied `export-ignore` rules. A recursive filesystem ZIP or upload can include ignored files; use the reviewed Git file set for publication. Keep `obsolete/` separately for local safekeeping. Any local compatibility links into that archive depend on its current location.

Review Git history and remotes before changing repository visibility. Source cleanup and pattern scans support inspection; they cannot identify an undisclosed private identifier whose meaning is known only to its owner.
