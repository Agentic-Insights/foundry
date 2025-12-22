---
description: Diagnose BAML configuration and identify problems
argument-hint: [schema|clients|tests|env]
---

# Diagnose BAML Issues

Analyze BAML configuration and identify problems.

## Diagnostic Checks

### 1. Project Structure
- [ ] `baml_src/` directory exists
- [ ] `generators.baml` exists and is valid
- [ ] `clients.baml` exists with at least one client
- [ ] Generated `baml_client/` exists

### 2. Generator Configuration
```bash
# Check generator version matches CLI
baml-cli --version
```

Compare with `generators.baml` version field.

### 3. Client Configuration
Verify clients have:
- Valid provider (openai, anthropic, ollama, etc.)
- API key reference (`env.OPENAI_API_KEY`)
- Valid model name

### 4. Environment Variables
Check required env vars are set:
```bash
echo $OPENAI_API_KEY | head -c 10
echo $ANTHROPIC_API_KEY | head -c 10
```

### 5. Schema Validation
Look for common schema issues:
- Missing `{{ ctx.output_format }}` in prompts
- Deeply nested types (3+ levels)
- Ambiguous field names without @description
- @assert expressions that may fail unexpectedly

### 6. Test Health
```bash
baml-cli test --parallel 1
```

Check for:
- Parse failures
- Validation failures
- Timeouts

## Arguments

`$ARGUMENTS` can specify focus area:
- `schema` - Check schema files only
- `clients` - Check client configuration
- `tests` - Run and analyze tests
- `env` - Check environment variables
- (empty) - Run all checks

## Output

Provide:
1. **Status** - Overall health (✓ OK, ⚠ Warnings, ✗ Issues)
2. **Findings** - List of issues found
3. **Recommendations** - How to fix each issue
4. **Next Steps** - Suggested actions

## Example Output

```
BAML Project Diagnosis
======================

✓ Project Structure
  - baml_src/ found
  - generators.baml valid
  - clients.baml valid

⚠ Client Configuration
  - GPT4 client uses deprecated model name
  - Recommendation: Change "gpt-4" to "gpt-4-turbo"

✗ Environment
  - ANTHROPIC_API_KEY not set
  - Recommendation: Set in .env or environment

⚠ Schema Issues
  - ExtractData function missing ctx.output_format
  - Location: baml_src/extract.baml:15

Tests: 8 passed, 2 failed
  - TestComplexExtraction: Parse error
  - TestImageReceipt: Timeout

Next Steps:
1. Fix ANTHROPIC_API_KEY if using Anthropic
2. Add {{ ctx.output_format }} to ExtractData prompt
3. Run /baml-test TestComplexExtraction to debug
```

## Deep Diagnosis

If `$ARGUMENTS` includes a specific function or test name, do deep analysis:
1. Read the schema
2. Check the prompt
3. Run the test
4. Analyze output
5. Provide specific fix
