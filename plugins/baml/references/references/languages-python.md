# Python + BAML Reference

Python-specific patterns for BAML with Pydantic generated types.

## Project Setup

### With uv (Recommended)

```bash
# Create project
uv init my-baml-project
cd my-baml-project

# Add BAML
uv add baml-py

# Initialize BAML structure
mkdir baml_src
```

### generators.baml for Python

```baml
generator target {
  output_type python/pydantic
  output_dir "../baml_client"
  version "0.211.2"  // Must match installed baml-py version
}

// For Pydantic v1 compatibility
generator target_v1 {
  output_type python/pydantic/v1
  output_dir "../baml_client_v1"
  version "0.211.2"
}
```

### Project Structure

```
my-project/
├── baml_src/
│   ├── generators.baml
│   ├── clients.baml
│   └── *.baml
├── baml_client/           # Generated - don't edit
│   ├── __init__.py
│   ├── types.py           # Pydantic models
│   ├── sync_client.py
│   └── async_client.py
├── pyproject.toml
└── .env
```

## Generated Code Usage

### Import Pattern

```python
from baml_client import b
from baml_client.types import Person, Invoice, LineItem
```

### Sync Usage

```python
# Simple extraction
person = b.ExtractPerson(text)
print(person.name)  # Type-safe access

# With validation error handling
from baml_client.errors import BamlValidationError

try:
    invoice = b.ExtractInvoice(doc)
except BamlValidationError as e:
    print(f"Validation failed: {e}")
```

### Async Usage

```python
import asyncio

async def extract_async():
    person = await b.ExtractPerson(text)
    return person

result = asyncio.run(extract_async())
```

### Streaming

```python
# Sync streaming
stream = b.stream.ExtractData(large_doc)
for partial in stream:
    print(f"Progress: {len(partial.items)} items")

final = stream.get_final_response()

# Async streaming
async for partial in b.stream.ExtractData(doc):
    update_ui(partial)
```

## Type Safety

### Generated Pydantic Models

BAML classes become Pydantic models:

```python
# From baml_client/types.py (generated)
class Person(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

# Full type hints in IDE
person = b.ExtractPerson(text)
person.name    # str - autocomplete works
person.age     # Optional[int]
```

### Union Type Handling

```python
from baml_client.types import GetWeather, SearchWeb, Calculator

result = b.SelectTool(query)

# Pattern matching (Python 3.10+)
match result:
    case GetWeather(location=loc, units=u):
        return fetch_weather(loc, u)
    case SearchWeb(query=q):
        return search(q)
    case Calculator(expression=expr):
        return eval_safe(expr)

# isinstance (all Python versions)
if isinstance(result, GetWeather):
    return fetch_weather(result.location, result.units)
```

## Validation Access

### Check Results

```python
result = b.ExtractData(text)

# Access individual checks
if result.__baml_checks__.has_source.passed:
    process(result.source)
else:
    log_warning("Missing source")

# Check all validations
all_passed = all(
    check.passed
    for check in result.__baml_checks__.__dict__.values()
)
```

### Error Handling

```python
from baml_client.errors import BamlValidationError

try:
    result = b.ExtractInvoice(doc)
except BamlValidationError as e:
    logger.error(f"Validation failed: {e}")
    result = fallback_extraction(doc)
```

## Image Handling

```python
from baml_py import Image

# From file
result = b.AnalyzeImage(
    img=Image.from_url("file:///path/to/image.jpg")
)

# From URL
result = b.AnalyzeImage(
    img=Image.from_url("https://example.com/image.png")
)

# From base64
result = b.AnalyzeImage(
    img=Image.from_base64("image/png", base64_string)
)
```

## Dynamic Types

```python
from baml_client.type_builder import TypeBuilder

# Add enum values
tb = TypeBuilder()
tb.Category.add_value("REFUND")
tb.Category.add_value("SHIPPING")

result = b.Classify(text, {"tb": tb})

# Add class properties
tb = TypeBuilder()
tb.DataRecord.add_property("user_id", "string")
tb.DataRecord.add_property("metadata", "map<string, string>")

record = b.ExtractRecord(log, {"tb": tb})
```

## Environment Variables

```python
# .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# For python-dotenv users
from dotenv import load_dotenv
load_dotenv()  # Load before importing baml_client

from baml_client import b
```

## Testing

### Run BAML Tests

```bash
baml-cli test
baml-cli test --filter "TestName"
baml-cli test --parallel 5
```

### Python Unit Tests

```python
import pytest
from baml_client import b

def test_person_extraction():
    text = "John Smith, john@example.com, age 30"
    result = b.ExtractPerson(text)

    assert result.name == "John Smith"
    assert result.email == "john@example.com"
    assert result.age == 30

@pytest.mark.asyncio
async def test_async_extraction():
    result = await b.ExtractPerson(text)
    assert result.name is not None
```

## Best Practices

1. **Use uv for dependency management** - Faster, more reliable than pip
2. **Type hints everywhere** - Generated code has full type hints
3. **Handle validation errors** - Wrap in try/except for production
4. **Stream for large documents** - Better UX, memory efficiency
5. **Use async for high throughput** - Better concurrency
