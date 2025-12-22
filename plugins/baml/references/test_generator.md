# Test Generator Module

**Version**: 1.0.0
**Purpose**: Generate comprehensive test suites for BAML functions

## Overview

Generates happy path, edge case, and error handling tests for generated BAML code.

## Test Generation

```
FUNCTION generate_tests(baml_code, requirement_spec):
  functions = extract_functions(baml_code)
  tests = []

  FOR function IN functions:
    # Happy path test
    tests.append(generate_happy_path_test(function, requirement_spec))

    # Edge case tests
    tests.extend(generate_edge_case_tests(function, requirement_spec))

    # Error handling tests
    tests.append(generate_error_test(function))

  RETURN tests

FUNCTION generate_happy_path_test(function, spec):
  language = spec.get("target_language", "python")

  IF language == "python":
    RETURN f"""
import pytest
from baml_client import b
from baml_client.types import {function.return_type}

@pytest.mark.asyncio
async def test_{function.name}_happy_path():
    # TODO: Provide test input
    result = await b.{function.name}(test_input)

    assert isinstance(result, {function.return_type})
    # TODO: Add specific assertions
"""

  # Similar for TypeScript, Ruby, etc.
```

## Test Templates by Framework

```
PYTHON_TEST_TEMPLATE = """
import pytest
from baml_client import b
from baml_client.types import {return_type}

@pytest.mark.asyncio
async def test_{function_name}():
    result = await b.{function_name}({params})
    assert isinstance(result, {return_type})
"""

TYPESCRIPT_TEST_TEMPLATE = """
import {{ {function_name} }} from './baml_client';
import {{ {return_type} }} from './baml_client/types';

test('{function_name}', async () => {{
  const result = await {function_name}({params});
  expect(result).toBeInstanceOf({return_type});
}});
"""
```

## Fallback Test Generation

```
FUNCTION generate_basic_tests(baml_code):
  # When detailed spec unavailable, generate basic template
  RETURN """
# Basic test template
# TODO: Customize for your use case

import pytest
from baml_client import b

@pytest.mark.asyncio
async def test_generated_function():
    # Provide test inputs
    result = await b.GeneratedFunction(test_input)

    # Add assertions
    assert result is not None
"""
```

---

**Status**: Test generation for Python/TypeScript/Ruby
