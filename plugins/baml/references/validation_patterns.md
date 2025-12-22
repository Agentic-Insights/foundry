# Validation Patterns Reference

Practical guide to using @assert and @check for data quality enforcement in generated BAML code.

## Overview

- **@assert**: Strict validation - raises exception on failure
- **@check**: Non-blocking validation - tracks pass/fail for monitoring

Both use Jinja2 expressions.

## @assert - Strict Validation

### Basic Assertions

```baml
class Payment {
  amount float @assert(this > 0)
  currency string @assert(this in ["USD", "EUR", "GBP"])
  status string @assert(this in ["pending", "completed", "failed"])
}
```

### Numeric Constraints

```baml
class Product {
  price float @assert(this >= 0)
  quantity int @assert(this > 0)
  discount_percent float @assert(this >= 0 and this <= 100)
  rating float @assert(this >= 1 and this <= 5)
}
```

### String Validations

```baml
class User {
  username string @assert(this|length >= 3 and this|length <= 20)
  email string @assert("@" in this and "." in this)
  phone string @assert(this|length == 10)
}
```

### Regex Validation

```baml
class Contact {
  email string @assert(this|regex_match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"))
  phone string @assert(this|regex_match("^\\d{3}-\\d{3}-\\d{4}$"))
}
```

### Collection Validations

```baml
class Data {
  tags string[] @assert(this|length > 0)
  scores int[] @assert(this|min >= 0 and this|max <= 100)
}

class Team {
  members string[] @assert(this|unique|length == this|length)  // No duplicates
}
```

## @check - Monitoring Validation

Non-blocking - data passes through but status is tracked.

```baml
class Citation {
  line_number int @assert(this > 0)           // Strict
  quote string @check(this|length > 0, exact_citation_found)  // Monitored
  website_link string @check("https://" in this, valid_link)
}
```

### Accessing Check Results

```python
result = b.GetCitation(text)

if result.__baml_checks__.exact_citation_found.passed:
    print("Citation found!")
else:
    log_warning("Citation might be missing", result.quote)

# Check all
all_passed = all(
    check.passed
    for check in result.__baml_checks__.__dict__.values()
)
```

## Block-Level Validation (@@assert)

Validate relationships between fields:

```baml
class Invoice {
  subtotal float
  tax_amount float
  total float
  @@assert({{ this.total == this.subtotal + this.tax_amount }}, invalid_total)
}

class DateRange {
  start_date string
  end_date string
  @@assert({{ this.start_date <= this.end_date }}, invalid_range)
}
```

## Validation Expressions

### Operators

```baml
this > 0              // Comparison
this >= 10 and this < 100  // Logical
this in ["a", "b"]    // Membership
"@" in this           // Contains
```

### Filters

```baml
this|length > 5       // String/collection length
this|lower == "test"  // String transform
this|regex_match("pattern")  // Regex
this|min >= 0         // Collection min
this|max <= 100       // Collection max
this|sum == 1000      // Collection sum
this|unique|length == this|length  // No duplicates
```

## Production Patterns

### Layered Validation

```baml
class Transaction {
  amount float
    @assert(this > 0)                         // Critical
    @check(this <= 10000, reasonable_amount)  // Warning
}
```

### Calculated Field Verification

```baml
class LineItem {
  quantity int @assert(this > 0)
  unit_price float @assert(this >= 0)
  subtotal float @check(this == quantity * unit_price, correct_calc)
}
```

If calculation is wrong, data returns but check fails - fix in app:

```python
for item in items:
    if not item.__baml_checks__.correct_calc.passed:
        item.subtotal = item.quantity * item.unit_price
```

### Confidence Scoring

```baml
class Extraction {
  value string @check(this|length > 5, high_confidence)
  source string @check(this|length > 0, has_source)
}
```

```python
result = b.Extract(doc)
confidence = sum(
    1 for check in result.__baml_checks__.__dict__.values()
    if check.passed
) / len(result.__baml_checks__.__dict__)

if confidence < 0.7:
    queue_for_manual_review(result)
```

## Best Practices

### Use @assert For
- Critical business rules
- Data integrity requirements
- Type constraints
- Security validations

### Use @check For
- Quality monitoring
- Optional validations
- Calculated field verification
- Confidence tracking

### Error Handling

```python
from baml_client.errors import BamlValidationError

try:
    result = b.ExtractData(text)
except BamlValidationError as e:
    # Fallback or manual review
    result = b_fallback.ExtractData(text)
```

### Testing Validations

```baml
test ValidPayment {
  functions [ExtractPayment]
  args { text "Payment of $100 USD" }
  @@assert({{ this.amount > 0 }})
  @@assert({{ this.currency in ["USD", "EUR"] }})
}
```

---

**Purpose**: Practical @assert/@check patterns for code generation
**Related**: `validator.md` (validation pipeline)
