---
description: Run BAML tests with optional filter
argument-hint: [filter] [-p parallel] [-v verbose]
---

# Run BAML Tests

Execute BAML test suite with options.

## Quick Usage

```bash
# Run all tests
baml-cli test

# Filter by name
baml-cli test --filter "$ARGUMENTS"

# Parallel execution
baml-cli test --parallel 5

# Verbose output
baml-cli test --verbose
```

## Default Behavior

If `$ARGUMENTS` is empty, run all tests:
```bash
baml-cli test
```

If `$ARGUMENTS` contains a filter pattern:
```bash
baml-cli test --filter "$ARGUMENTS"
```

## Options Parsing

Parse `$ARGUMENTS` for:
- `-p N` or `--parallel N`: Run with N parallel workers
- `-v` or `--verbose`: Show detailed output
- `-f PATTERN` or `--filter PATTERN`: Filter test names
- Any other text: Use as filter pattern

## Example Commands

```
/baml-test                    → baml-cli test
/baml-test Receipt            → baml-cli test --filter "Receipt"
/baml-test -p 5               → baml-cli test --parallel 5
/baml-test Receipt -v         → baml-cli test --filter "Receipt" --verbose
/baml-test -p 3 -f Extract    → baml-cli test --parallel 3 --filter "Extract"
```

## Output Format

Report:
1. Command executed
2. Test results (pass/fail counts)
3. Failure details if any
4. Suggestions for failures

## On Failure

If tests fail:
1. Show which tests failed
2. Show assertion that failed
3. Show expected vs actual (if available)
4. Suggest using `/baml-diagnose` for deeper analysis

## Prerequisites

- `baml_src/` directory exists
- `baml-cli` is installed
- Environment variables are set
