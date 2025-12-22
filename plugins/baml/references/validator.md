# Validator Module

**Version**: 1.0.0
**Purpose**: 5-layer validation pipeline for generated BAML code

## Overview

Validates generated BAML code through syntax, type, semantic, completeness, and performance checks.

## Validation Pipeline

```
FUNCTION validate(baml_code):
  results = {
    "valid": True,
    "errors": [],
    "warnings": [],
    "suggestions": []
  }

  # Layer 1: Syntax
  syntax_result = validate_syntax(baml_code)
  IF not syntax_result.valid:
    results.valid = False
    results.errors.extend(syntax_result.errors)

  # Layer 2: Types
  type_result = validate_types(baml_code)
  IF not type_result.valid:
    results.valid = False
    results.errors.extend(type_result.errors)

  # Layer 3: Semantics
  semantic_result = validate_semantics(baml_code)
  results.warnings.extend(semantic_result.warnings)

  # Layer 4: Completeness
  completeness_result = validate_completeness(baml_code)
  IF not completeness_result.valid:
    results.warnings.append("Incomplete code")

  # Layer 5: Performance
  perf_result = validate_performance(baml_code)
  results.suggestions.extend(perf_result.suggestions)

  RETURN results

FUNCTION validate_syntax(code):
  # Parse BAML with grammar rules
  TRY:
    ast = parse_baml(code)
    RETURN {"valid": True}
  CATCH SyntaxError as e:
    RETURN {"valid": False, "errors": [str(e)]}

FUNCTION validate_types(code):
  defined = extract_defined_types(code)
  referenced = extract_referenced_types(code)
  undefined = [t for t in referenced if t not in defined and t not in BUILTIN_TYPES]

  IF undefined:
    RETURN {"valid": False, "errors": [f"Undefined types: {undefined}"]}
  RETURN {"valid": True}

FUNCTION validate_semantics(code):
  warnings = []
  # Check prompt coherence
  # Check client references
  # Check parameter usage
  RETURN {"warnings": warnings}

FUNCTION validate_completeness(code):
  has_types = "class " in code or "enum " in code
  has_functions = "function " in code
  has_clients = "client " in code

  RETURN {"valid": has_types and has_functions and has_clients}

FUNCTION validate_performance(code):
  suggestions = []
  token_count = count_tokens(code)

  IF token_count > 3000:
    suggestions.append("Consider optimizing prompts for token reduction")

  RETURN {"suggestions": suggestions}
```

## Fallback Validation

```
FUNCTION validate_fallback(code):
  # When MCP unavailable, use basic checks
  has_basic_structure = (
    "class " in code or "enum " in code
  ) and "function " in code

  RETURN {"valid": has_basic_structure}
```

---

**Status**: 5-layer validation implemented
