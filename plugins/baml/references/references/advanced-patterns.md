# Advanced Extraction Patterns

Complex extraction scenarios including hierarchical structures, dynamic types, and tool calling.

## Hierarchical Extraction

### Nested Organizations

```baml
class Employee {
  name string
  title string
  email string
}

class Department {
  name string
  manager Employee
  employees Employee[]
}

class Company {
  name string
  departments Department[]
  ceo Employee
}

function ExtractOrgChart(doc: string) -> Company {
  client GPT4
  prompt #"
    Extract complete organizational structure:
    {{ doc }}
    {{ ctx.output_format }}
  "#
}
```

### Recursive Document Structure

```baml
class Section {
  heading string
  level int  // 1 = H1, 2 = H2, etc.
  content string
  subsections Section[]  // Recursive
}

class Document {
  title string
  sections Section[]
}
```

## Table Parsing with Calculations

### Invoice with Totals

```baml
class LineItem {
  description string
  quantity int @assert(this > 0)
  unit_price float @assert(this >= 0)
  subtotal float @description("quantity * unit_price")
}

class Invoice {
  invoice_number string
  line_items LineItem[] @assert(this|length > 0)
  subtotal float @description("Sum of line item subtotals")
  tax_rate float
  tax_amount float @description("subtotal * tax_rate")
  total float @description("subtotal + tax_amount")

  @@assert({{ this.total == this.subtotal + this.tax_amount }}, valid_total)
}

function ExtractInvoice(doc: image) -> Invoice {
  client GPT4
  prompt #"
    Extract invoice with ALL calculated fields.

    Calculate:
    - Line total = quantity × unit_price
    - Subtotal = sum of line items
    - Tax = subtotal × tax_rate
    - Total = subtotal + tax

    {{ doc }}
    {{ ctx.output_format }}
  "#
}
```

## Union Types for Tool Calling

### Multi-Tool Selection

```baml
class GetWeather {
  location string
  units "celsius" | "fahrenheit"
}

class SearchWeb {
  query string
  max_results int
}

class Calculator {
  expression string
}

// Single tool
function SelectTool(query: string) -> GetWeather | SearchWeb | Calculator {
  client GPT4
  prompt #"Select tool for: {{ query }} {{ ctx.output_format }}"#
}

// Multiple tools
function SelectTools(query: string) -> (GetWeather | SearchWeb | Calculator)[] {
  client GPT4
  prompt #"Select ALL tools for: {{ query }} {{ ctx.output_format }}"#
}
```

**Python usage:**
```python
from baml_client.types import GetWeather, SearchWeb, Calculator

result = b.SelectTool("weather in Seattle")

if isinstance(result, GetWeather):
    weather = fetch_weather(result.location)
elif isinstance(result, SearchWeb):
    results = search(result.query)
elif isinstance(result, Calculator):
    answer = evaluate(result.expression)
```

## Dynamic Types

### Runtime Schema Modification

```baml
enum Category @@dynamic {
  TECHNICAL
  BILLING
}

class DataRecord @@dynamic {
  id string
  timestamp string
}
```

**Python usage:**
```python
from baml_client.type_builder import TypeBuilder

tb = TypeBuilder()
tb.Category.add_value("REFUND")
tb.Category.add_value("SHIPPING")

result = b.Classify(text, {"tb": tb})
```

## Streaming Patterns

```python
stream = b.stream.ExtractData(large_doc)
for partial in stream:
    print(f"Extracted {len(partial.items)} items...")

final = stream.get_final_response()
```

### Semantic Streaming Control

```baml
class ImportantItem @stream.done {
  id string
  data string
  // Only streams when complete
}

class DataStream {
  title string @stream.not_null  // Must exist before streaming
  items ImportantItem[]
}
```

## Image and Multimodal

```baml
class ImageContent {
  description string
  main_objects string[]
  text_detected string?
}

function AnalyzeImage(img: image) -> ImageContent {
  client GPT4
  prompt #"
    {{ _.role("user") }}
    Analyze: {{ img }}
    {{ ctx.output_format }}
  "#
}
```

```python
from baml_py import Image
result = b.AnalyzeImage(img=Image.from_url("file://invoice.jpg"))
```

## Best Practices

### Keep Nesting Reasonable

**Good** (3 levels):
```baml
class Invoice {
  vendor Company
  line_items LineItem[]
}
```

**Too Deep** (5+ levels) - split into multiple passes.

### Progressive Extraction

For large complex documents:

```python
# Pass 1: Structure
structure = b.ExtractStructure(doc)

# Pass 2: Details per section
sections = [b.ExtractSection(doc, s) for s in structure.section_ids]

# Combine
complete = combine(structure, sections)
```

### Token-Efficient Schemas

```baml
// Verbose (high tokens)
class Person {
  fullNameIncludingMiddle string @description("Complete name with first, middle, last")
}

// Concise (low tokens)
class Person {
  name string  // Already clear
}
```

### Error Recovery

```python
try:
    result = b.ExtractComplex(doc)
except BamlValidationError:
    result = b.ExtractSimple(doc)  # Fallback
```
