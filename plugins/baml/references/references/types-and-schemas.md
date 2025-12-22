# BAML Type System Reference

Complete reference for BAML's type system, which compiles to native Pydantic (Python) and TypeScript interfaces.

## Primitive Types

```baml
bool      // true, false
int       // 42, -10, 0
float     // 3.14, -0.5, 2.0
string    // "text", 'text'
null      // null value
```

## Optional Types

```baml
class User {
  name string              // Required
  nickname string?         // Optional (shorthand)
  bio Optional<string>     // Optional (explicit)
}
```

## Collection Types

### Lists

```baml
class Data {
  tags string[]           // Shorthand
  items List<string>      // Explicit
  matrix int[][]          // Nested arrays
}
```

### Maps

```baml
class Config {
  settings map<string, string>
  counts map<string, int>
  metadata map<string, string | int | bool>
}
```

Map keys must be strings or enums.

## Multimodal Types

```baml
class Analysis {
  document image | pdf | audio | video
  photo image
  recording audio
}

function AnalyzeImage(img: image) -> Description {
  client GPT4
  prompt #"Describe: {{ img }} {{ ctx.output_format }}"#
}
```

**Python usage:**
```python
from baml_py import Image
result = b.AnalyzeImage(img=Image.from_url("file://path/to/image.jpg"))
```

## Classes (Structured Types)

```baml
class Address {
  street string
  city string
  state string
  zip_code string
}

class Company {
  name string
  founded_year int
  headquarters Address  // Nested
}
```

### Field Attributes

**@alias** - Different name for LLM:
```baml
class Person {
  fullName string @alias("full_name")
}
```

**@description** - Context for LLM (critical for guiding extraction):
```baml
class Task {
  priority int @description("1-5 where 5 is highest")
  dueDate string @description("Format: yyyy-mm-dd")
}
```

**@skip** - Exclude from LLM schema:
```baml
class User {
  name string
  internal_id string @skip
}
```

### Dynamic Classes

```baml
class Resume @@dynamic {
  name string
  email string
}
```

**Python usage:**
```python
from baml_client.type_builder import TypeBuilder

tb = TypeBuilder()
tb.Resume.add_property("linkedin", "string")
result = b.ExtractResume(text, {"tb": tb})
```

## Enums

```baml
enum Status {
  PENDING
  IN_PROGRESS
  COMPLETED
}

enum Priority {
  Low
  Medium
  High
}
```

### Dynamic Enums

```baml
enum Category @@dynamic {
  TECHNICAL
  BILLING
}
```

```python
tb = TypeBuilder()
tb.Category.add_value("REFUND")
result = b.Classify(text, {"tb": tb})
```

## Literal Types

```baml
function Classify() -> "positive" | "negative" | "neutral" {
  client GPT4
  prompt #"Classify sentiment {{ ctx.output_format }}"#
}

class Config {
  mode "development" | "staging" | "production"
  level 1 | 2 | 3 | 4 | 5
}
```

## Union Types

```baml
function Parse() -> int | string {
  // Tries int first, then string
}

class Response {
  data string | int | bool
}
```

### Union for Tool Calling

```baml
class GetWeather {
  location string
}

class SearchWeb {
  query string
}

function SelectTool(query: string) -> GetWeather | SearchWeb {
  client GPT4
  prompt #"Select tool for: {{ query }} {{ ctx.output_format }}"#
}
```

**Python usage:**
```python
result = b.SelectTool("weather in Seattle")
if isinstance(result, GetWeather):
    # Handle weather
elif isinstance(result, SearchWeb):
    # Handle search
```

## Type Aliases

```baml
type Graph = map<string, string[]>
type Result = int | string | bool

// Recursive
type JsonValue = int | float | bool | string | null | JsonValue[] | map<string, JsonValue>

class Data {
  graph Graph
  result Result
}
```

## Recursive Types

```baml
class TreeNode {
  value string
  children TreeNode[]
}

class Section {
  heading string
  content string
  subsections Section[]  // Recursive
}
```

## Calculated Fields

Use @description to hint at calculations:

```baml
class LineItem {
  quantity int
  unit_price float
  total float @description("quantity * unit_price")
}

class Invoice {
  items LineItem[]
  subtotal float @description("Sum of all line item totals")
  tax_amount float @description("subtotal * tax_rate")
  total float @description("subtotal + tax_amount")
}
```

## Best Practices

**For extraction accuracy:**
- Set temperature to 0.0
- Use @description to clarify ambiguous fields
- Prefer enums over strings when values are known
- Use @assert for critical validations

**For type design:**
- Keep nesting to 3-4 levels maximum
- Use Optional<T> for truly optional fields
- Prefer unions over generic types when possible

**For token efficiency:**
- Rely on `{{ ctx.output_format }}` for schema injection
- Use @alias sparingly (adds tokens)
- @skip fields that don't need LLM extraction

**For maintainability:**
- One class per concept
- Descriptive field names
- Group related types in same .baml file
