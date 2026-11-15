---
name: shell-scripting
title: "Shell Scripting: Bash, POSIX and PowerShell"
description: "Write safe Bash, POSIX sh and PowerShell scripts: strict mode and its limits, quoting, error handling, traps, temp files, ShellCheck, testing."
license: Apache-2.0
compatibility: "Bash 4.4+ or POSIX sh on Linux and macOS; PowerShell 7 or Windows PowerShell 5.1. ShellCheck and PSScriptAnalyzer optional."
domains: developer devops
rules:
  - content(bash)
  - content(shell script)
  - content(powershell)
  - content(posix)
  - content(shellcheck)
  - match((?i)\b(bash|shell|zsh|powershell|pwsh|sh)\s+(scripts?|one-?liners?|functions?)\b)
  - match((?i)\b(pipefail|shebang|psscriptanalyzer|heredoc|errexit|nounset)\b)
  - match((?i)\b\w+\.(sh|ps1)\b)
---

## Overview

Use this when you write, review or fix a Bash, POSIX `sh` or PowerShell script. The outcome is a script that fails loudly, handles odd file names and empty input, cleans up after itself, and says which shell it needs.

## Mental model

A shell script is glue between programs, and its two classic failures are silent success after a failed step and the shell re-splitting text you meant as one value. Choose the shell by where the script runs, turn on the strictest sensible mode, and treat every variable, file name and command output as data that may contain spaces, newlines or a leading dash.

## Rules

### Choose the shell

| Situation | Use |
|---|---|
| Must run on minimal images (Alpine BusyBox, Debian `dash`) or as `/bin/sh` | POSIX `sh`: no arrays, no `[[ ]]`, no `local` assumptions; test with `dash` |
| Linux or macOS tooling where you control the interpreter | Bash; check `bash --version` on the target, because the system Bash on macOS can be older than the 4.4 this skill assumes; state the minimum |
| Windows administration, objects not text | PowerShell 7 (`pwsh`); Windows PowerShell 5.1 (`powershell.exe`) only when the target has nothing else |
| Parsing JSON, YAML or dates with branching logic | Python or the platform's own language instead of shell text tools |

State the interpreter in the shebang (`#!/usr/bin/env bash`) and, for Bash, the minimum version in a comment.

### Bash header

```bash
#!/usr/bin/env bash
set -euo pipefail
shopt -s inherit_errexit   # Bash 4.4+
IFS=$'\n\t'

tmpdir=$(mktemp -d)
cleanup() { rm -rf -- "$tmpdir"; }
trap cleanup EXIT
```

- `set -e` is not a safety net. It is ignored in a command used as an `if`, `while`, `&&` or `||` condition, and by default it is off inside `$(...)`; `inherit_errexit` turns it on there. A failed command that is an argument to another (`echo "$(false)"`) loses its status. Check the exit code of commands that matter: `if ! result=$(cmd); then ...`.
- `set -u` makes an unset variable an error. Write `${VAR:-default}` where unset is valid, and `"${arr[@]}"` for arrays (Bash before 4.4 errors on an empty array under `set -u`).
- `set -o pipefail` makes a pipeline fail if any stage fails. `grep -q` in a pipeline can then fail with SIGPIPE; capture output first when that matters.
- Use `trap ... EXIT` for cleanup, and `mktemp` for temporary files and directories, never a fixed name in `/tmp`.

### Quoting and data

- Quote every expansion: `"$var"`, `"$@"`, `"${arr[@]}"`. Unquoted expansions split on whitespace and expand globs.
- Never parse `ls`. Loop over globs (`for f in ./*.log`) or use `find ... -print0 | while IFS= read -r -d '' f`. Prefix paths with `./` or use `--` so a name starting with `-` is not read as an option.
- Read lines with `while IFS= read -r line`. Without `-r` a backslash is eaten.
- Use `[[ ... ]]` in Bash and `[ ... ]` in POSIX. Test numbers with `-eq` or `(( ))`, strings with `=` or `==`.
- Use `$(...)`, not backticks. Use `printf '%s\n' "$x"` rather than `echo` when the value may start with `-` or contain escapes.
- Keep secrets out of the command line (visible in `ps`): read them from a file descriptor, environment of the child only, or a credentials file with mode 600.

### Structure

- Put logic in functions with `local` variables; one `main "$@"` at the bottom.
- Parse options with `getopts` (POSIX) or a `case` loop with `--` handling; print usage to stderr and exit 2 on bad input.
- Send diagnostics to stderr, results to stdout. Return distinct exit codes for distinct failures and document them.
- Make destructive scripts support a `--dry-run` that prints the commands, and confirm before deleting.
- Make scripts idempotent: running twice leaves the same state (`mkdir -p`, `ln -sfn`, check before append).
- Lock a script that must not run twice at once with `flock` (Linux) or an atomic `mkdir` lock directory.

### Tools

- Run ShellCheck on every script (`shellcheck -x script.sh`) and fix warnings rather than disabling them; a `# shellcheck disable=SCnnnn` carries a reason.
- Format with `shfmt`. Test with `bats` (Bash) or a `pester`/CI smoke run, and run the script once on the oldest target image.

### PowerShell

```powershell
#Requires -Version 7.0
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true   # 7.4+; off by default
```

- `$ErrorActionPreference = 'Stop'` turns non-terminating cmdlet errors into terminating ones that `try/catch` can handle. It does not cover native executables: check `$LASTEXITCODE`, or on PowerShell 7.4+ set `$PSNativeCommandUseErrorActionPreference` (default `$false`, so it is opt-in).
- `Set-StrictMode -Version Latest` errors on uninitialized variables and bad property or index access. It is a runtime mode scoped to where it is set, and a newer PowerShell can make `Latest` stricter, so pin a number in shared modules.
- Pass objects, not text: `Get-Process | Where-Object CPU -gt 100`; avoid parsing formatted output. Use `-LiteralPath` for paths with wildcard characters, and splat arguments with a hashtable or array rather than building a command string.
- Write advanced functions with `[CmdletBinding(SupportsShouldProcess)]` and call `$PSCmdlet.ShouldProcess()` so `-WhatIf` and `-Confirm` work for anything that changes state.
- Don't use `Invoke-Expression` on input. Keep secrets in `SecureString` or a vault, not in plain parameters or logs.
- Analyze with PSScriptAnalyzer (`Invoke-ScriptAnalyzer`) and test with Pester. Check the lifecycle of the PowerShell version you target before depending on it; 7.4 reached end of support on 2026-11-10 and 7.6 is the current LTS (as of 2026-11).

## Examples

Bad: `for f in $(ls *.log); do rm $f; done`. It breaks on spaces and cannot report a failed `rm`.

Good:

```bash
for f in ./*.log; do
  [[ -e "$f" ]] || continue
  rm -- "$f"
done
```

Bad: `echo "Deploying" ; ./deploy.sh ; echo "done"` with no error check, so "done" prints after a failed deploy.

Good: the Bash header above, then `./deploy.sh` alone; the script stops at the failure with the non-zero status.

## Checklist

- [ ] Shebang and minimum shell version stated; strict mode on, with its blind spots handled explicitly.
- [ ] Every expansion quoted; no `ls` parsing; file names starting with `-` handled.
- [ ] Temporary files from `mktemp`, removed in a trap.
- [ ] Secrets absent from arguments and logs.
- [ ] Destructive actions have `--dry-run` (or `-WhatIf`) and confirmation.
- [ ] ShellCheck or PSScriptAnalyzer run clean; one test run on the oldest target.
- [ ] Not run against production data without the user's approval.

## References

- [Bash manual: the Set builtin and Shopt builtin](https://www.gnu.org/software/bash/manual/bash.html)
- [BashFAQ/105: why set -e does not do what you expect](https://mywiki.wooledge.org/BashFAQ/105)
- [ShellCheck](https://www.shellcheck.net/)
- [PowerShell error handling](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling) and [preference variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables)
- [PowerShell support lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle)
