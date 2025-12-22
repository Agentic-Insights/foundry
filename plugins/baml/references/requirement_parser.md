# Requirement Parser Module

**Version**: 1.0.0
**Purpose**: Parse natural language requirements into structured specifications
**Supports**: Extraction, classification, RAG, agents, multimodal

## Overview

The Requirement Parser analyzes user requirements in natural language and extracts structured information needed for code generation. It identifies pattern types, entities, constraints, and special features like multimodal support.

## Core Parsing Algorithm

```
FUNCTION parse_requirement(text):
  # Step 1: Normalize input
  normalized = normalize_text(text)

  # Step 2: Detect pattern category
  category = detect_pattern_category(normalized)

  # Step 3: Extract entities
  entities = extract_entities(normalized)

  # Step 4: Extract constraints
  constraints = extract_constraints(normalized)

  # Step 5: Detect special features
  features = detect_features(normalized)

  # Step 6: Estimate complexity
  complexity = estimate_complexity(normalized, entities, constraints)

  # Step 7: Build structured spec
  spec = {
    "original_text": text,
    "category": category,
    "entities": entities,
    "constraints": constraints,
    "features": features,
    "complexity": complexity
  }

  RETURN spec
```

## Pattern Category Detection

### Category Triggers
```
EXTRACTION_TRIGGERS = [
  "extract", "parse", "structure", "data", "document",
  "form", "ocr", "vision", "read", "capture"
]

CLASSIFICATION_TRIGGERS = [
  "classify", "categorize", "label", "identify", "detect",
  "sentiment", "intent", "category", "priority", "tag"
]

RAG_TRIGGERS = [
  "search", "retrieve", "context", "citation", "source",
  "reference", "query", "find", "lookup"
]

AGENT_TRIGGERS = [
  "agent", "plan", "execute", "tool", "workflow",
  "action", "decision", "task", "automate"
]
```

### Detection Algorithm
```
FUNCTION detect_pattern_category(text):
  words = tokenize(text.lower())
  scores = {
    "extraction": 0,
    "classification": 0,
    "rag": 0,
    "agents": 0
  }

  # Score each category
  FOR word IN words:
    IF word IN EXTRACTION_TRIGGERS:
      scores["extraction"] += 1
    IF word IN CLASSIFICATION_TRIGGERS:
      scores["classification"] += 1
    IF word IN RAG_TRIGGERS:
      scores["rag"] += 1
    IF word IN AGENT_TRIGGERS:
      scores["agents"] += 1

  # Position weighting (early words more important)
  FOR i, word IN enumerate(words):
    weight = 1.0 / (1.0 + i * 0.1)  # Decay by position
    IF word IN EXTRACTION_TRIGGERS:
      scores["extraction"] += weight
    # ... same for other categories

  # Get category with highest score
  max_score = max(scores.values())
  IF max_score == 0:
    RETURN "extraction"  # Default

  FOR category, score IN scores.items():
    IF score == max_score:
      RETURN category

  RETURN "extraction"  # Fallback
```

## Entity Extraction

### Entity Types
```
ENTITY_TYPES = {
  "data_objects": ["invoice", "resume", "receipt", "form", "document"],
  "data_fields": ["name", "date", "amount", "email", "address", "phone"],
  "categories": ["sentiment", "intent", "priority", "status"],
  "actions": ["extract", "classify", "search", "plan"],
  "sources": ["image", "text", "pdf", "document", "file"],
  "outputs": ["json", "structured", "class", "type"]
}
```

### Extraction Algorithm
```
FUNCTION extract_entities(text):
  entities = {
    "input_types": [],
    "output_types": [],
    "fields": [],
    "actions": []
  }

  words = tokenize(text)

  # Extract capitalized words (likely entity names)
  FOR word IN words:
    IF is_capitalized(word) AND word NOT IN COMMON_WORDS:
      entities["output_types"].append(word)

  # Extract known data objects
  FOR entity_type, keywords IN ENTITY_TYPES.items():
    FOR keyword IN keywords:
      IF keyword IN text.lower():
        IF entity_type == "data_objects":
          entities["output_types"].append(capitalize(keyword))
        ELSE IF entity_type == "sources":
          entities["input_types"].append(keyword)
        ELSE IF entity_type == "data_fields":
          entities["fields"].append(keyword)
        ELSE IF entity_type == "actions":
          entities["actions"].append(keyword)

  # Deduplicate
  FOR key IN entities.keys():
    entities[key] = list(set(entities[key]))

  RETURN entities
```

### Field Inference
```
FUNCTION infer_fields(text, entity_name):
  # Look for field mentions related to entity
  patterns = [
    f"{entity_name} (with|including|containing) (.+)",
    f"(\\w+) of (the )?{entity_name}",
    f"{entity_name}'s (\\w+)"
  ]

  fields = []
  FOR pattern IN patterns:
    matches = regex_findall(pattern, text, case_insensitive=True)
    fields.extend(matches)

  # Common field patterns
  IF "date" IN text.lower():
    fields.append("date")
  IF "total" IN text.lower() OR "amount" IN text.lower():
    fields.append("total")
  IF "name" IN text.lower():
    fields.append("name")

  RETURN list(set(fields))
```

## Constraint Extraction

### Constraint Types
```
CONSTRAINT_TYPES = {
  "validation": ["validate", "check", "ensure", "verify", "confirm"],
  "format": ["format", "YYYY-MM-DD", "ISO", "UTC"],
  "range": ["between", "min", "max", "at least", "up to"],
  "required": ["required", "mandatory", "must have", "necessary"],
  "optional": ["optional", "if available", "if present"]
}
```

### Extraction Algorithm
```
FUNCTION extract_constraints(text):
  constraints = []

  # Validation constraints
  validation_patterns = [
    "validate (that )?(.+)",
    "ensure (that )?(.+)",
    "check (that )?(.+)"
  ]

  FOR pattern IN validation_patterns:
    matches = regex_findall(pattern, text, case_insensitive=True)
    FOR match IN matches:
      constraints.append({
        "type": "validation",
        "rule": match
      })

  # Format constraints
  IF re.search(r"YYYY-MM-DD|ISO.?8601|UTC", text):
    constraints.append({
      "type": "format",
      "rule": "Use standard date/time formats"
    })

  # Range constraints
  range_patterns = [
    "between (\\d+) and (\\d+)",
    "at least (\\d+)",
    "maximum (\\d+)"
  ]

  FOR pattern IN range_patterns:
    matches = regex_findall(pattern, text)
    FOR match IN matches:
      constraints.append({
        "type": "range",
        "rule": f"Range constraint: {match}"
      })

  RETURN constraints
```

## Multimodal Detection

### Multimodal Keywords
```
MULTIMODAL_KEYWORDS = {
  "image": ["image", "picture", "photo", "screenshot", "visual", "scan"],
  "audio": ["audio", "sound", "speech", "voice", "recording"],
  "video": ["video", "clip", "recording"],
  "document": ["pdf", "document", "file"],
  "vision": ["ocr", "vision", "read", "see", "view", "analyze image"]
}
```

### Detection Algorithm
```
FUNCTION detect_multimodal(text):
  multimodal = {
    "has_multimodal": False,
    "input_types": [],
    "requires_vision_model": False
  }

  text_lower = text.lower()

  # Check for multimodal keywords
  FOR media_type, keywords IN MULTIMODAL_KEYWORDS.items():
    FOR keyword IN keywords:
      IF keyword IN text_lower:
        multimodal["has_multimodal"] = True
        multimodal["input_types"].append(media_type)

  # Deduplicate
  multimodal["input_types"] = list(set(multimodal["input_types"]))

  # Determine if vision model needed
  vision_types = ["image", "document", "vision"]
  FOR vtype IN vision_types:
    IF vtype IN multimodal["input_types"]:
      multimodal["requires_vision_model"] = True
      break

  RETURN multimodal
```

### Vision Model Selection
```
FUNCTION select_vision_model(multimodal_spec):
  IF not multimodal_spec["requires_vision_model"]:
    RETURN null

  # Default to GPT-4o for vision tasks
  RETURN {
    "provider": "openai",
    "model": "gpt-4o",
    "reason": "Best multimodal performance for image understanding"
  }

  # Alternative models:
  # - "anthropic/claude-3.5-sonnet" for complex reasoning + vision
  # - "google-ai/gemini-1.5-pro" for long-context vision
```

## Feature Detection

### Special Features
```
FEATURES = {
  "streaming": ["stream", "streaming", "real-time", "live"],
  "batch": ["batch", "bulk", "multiple", "many"],
  "validation": ["validate", "check", "verify"],
  "confidence": ["confidence", "score", "probability", "certainty"],
  "reasoning": ["reasoning", "explain", "rationale", "why"],
  "multimodal": [],  # Detected separately
  "async": ["async", "asynchronous", "background"]
}
```

### Detection Algorithm
```
FUNCTION detect_features(text):
  detected = []

  text_lower = text.lower()

  FOR feature, keywords IN FEATURES.items():
    FOR keyword IN keywords:
      IF keyword IN text_lower:
        detected.append(feature)
        break

  # Add multimodal if detected
  multimodal = detect_multimodal(text)
  IF multimodal["has_multimodal"]:
    detected.append("multimodal")

  RETURN list(set(detected))
```

## Complexity Estimation

### Complexity Factors
```
COMPLEXITY_FACTORS = {
  "simple": {
    "max_entities": 3,
    "max_fields_per_entity": 5,
    "max_constraints": 2,
    "no_nesting": True
  },
  "moderate": {
    "max_entities": 7,
    "max_fields_per_entity": 10,
    "max_constraints": 5,
    "nesting_depth": 2
  },
  "complex": {
    "max_entities": 15,
    "max_fields_per_entity": 20,
    "max_constraints": 10,
    "nesting_depth": 3
  }
}
```

### Estimation Algorithm
```
FUNCTION estimate_complexity(text, entities, constraints):
  score = 0

  # Entity count factor
  entity_count = len(entities.get("output_types", []))
  score += entity_count

  # Field count factor
  field_count = len(entities.get("fields", []))
  score += field_count * 0.5

  # Constraint factor
  constraint_count = len(constraints)
  score += constraint_count

  # Nesting factor (look for keywords)
  IF "nested" IN text.lower() OR "hierarchical" IN text.lower():
    score += 5

  # Special feature factor
  features = detect_features(text)
  score += len(features) * 2

  # Classify
  IF score <= 10:
    RETURN "simple"
  ELSE IF score <= 25:
    RETURN "moderate"
  ELSE:
    RETURN "complex"
```

## Output Structure

### RequirementSpec Schema
```json
{
  "original_text": "User's requirement text",
  "category": "extraction | classification | rag | agents",
  "entities": {
    "input_types": ["image", "text"],
    "output_types": ["Invoice", "LineItem"],
    "fields": ["invoice_number", "date", "total"],
    "actions": ["extract", "parse"]
  },
  "constraints": [
    {
      "type": "validation",
      "rule": "subtotal + tax = total"
    },
    {
      "type": "format",
      "rule": "Use YYYY-MM-DD for dates"
    }
  ],
  "features": ["multimodal", "validation", "confidence"],
  "multimodal": {
    "has_multimodal": true,
    "input_types": ["image"],
    "requires_vision_model": true,
    "recommended_model": {
      "provider": "openai",
      "model": "gpt-4o"
    }
  },
  "complexity": "moderate",
  "metadata": {
    "word_count": 25,
    "estimated_output_size": "medium",
    "generation_time_estimate_ms": 5000
  }
}
```

## Usage Examples

### Example 1: Simple Extraction
```
Input: "Extract invoice number and total from an image"

Process:
  1. Category: "extraction" (extract keyword)
  2. Entities: {
       output_types: ["Invoice"],
       fields: ["invoice_number", "total"],
       input_types: ["image"]
     }
  3. Multimodal: Yes (image keyword)
  4. Complexity: "simple" (2 fields, no nesting)

Output:
{
  "category": "extraction",
  "multimodal": {
    "has_multimodal": true,
    "requires_vision_model": true
  },
  "complexity": "simple"
}
```

### Example 2: Complex Classification
```
Input: "Classify customer support tickets by intent (billing, technical, general) with confidence scores and reasoning"

Process:
  1. Category: "classification" (classify, intent keywords)
  2. Entities: {
       output_types": ["Intent"],
       fields: ["category", "confidence", "reasoning"]
     }
  3. Features: ["confidence", "reasoning"]
  4. Complexity: "moderate" (3 categories + confidence + reasoning)

Output:
{
  "category": "classification",
  "features": ["confidence", "reasoning"],
  "entities": {
    "output_types": ["Intent"],
    "categories": ["billing", "technical", "general"]
  },
  "complexity": "moderate"
}
```

### Example 3: Multimodal Extraction
```
Input: "Extract structured data from invoice images including line items with description, quantity, and price. Validate that subtotal + tax = total."

Process:
  1. Category: "extraction"
  2. Entities: {
       input_types: ["image"],
       output_types: ["Invoice", "LineItem"],
       fields: ["description", "quantity", "price", "subtotal", "tax", "total"]
     }
  3. Constraints: ["subtotal + tax = total"]
  4. Multimodal: Yes (image keyword)
  5. Nesting: Yes (line items nested in invoice)
  6. Complexity: "complex"

Output:
{
  "category": "extraction",
  "multimodal": {
    "has_multimodal": true,
    "requires_vision_model": true,
    "recommended_model": {"provider": "openai", "model": "gpt-4o"}
  },
  "entities": {
    "output_types": ["Invoice", "LineItem"],
    "fields": ["description", "quantity", "price", "subtotal", "tax", "total"]
  },
  "constraints": [{
    "type": "validation",
    "rule": "subtotal + tax = total"
  }],
  "complexity": "complex"
}
```

## Integration Points

### With Pattern Matcher
```
# Requirement parser output feeds pattern matcher
spec = requirement_parser.parse(user_text)
patterns = pattern_matcher.find_patterns(spec.category, spec.entities)
```

### With Code Generator
```
# Spec guides code generation
spec = requirement_parser.parse(user_text)
code = code_generator.generate(spec)
```

### With MCP Interface
```
# Multimodal detection affects model selection
spec = requirement_parser.parse(user_text)
IF spec.multimodal.requires_vision_model:
  client = spec.multimodal.recommended_model
```

## Edge Cases

### Ambiguous Requirements
```
Input: "Process documents"

Handling:
  - Too vague, default to "extraction"
  - Prompt user for clarification:
    * "What type of documents?"
    * "What data should be extracted?"
    * "What format is the output?"
```

### Multiple Categories
```
Input: "Extract invoice data and classify it by priority"

Handling:
  - Primary: "extraction" (first action)
  - Secondary: "classification"
  - Generate both extraction and classification functions
```

### Novel Patterns
```
Input: "Build a system that..."

Handling:
  - If no clear pattern match, default to "agents"
  - Use generic template
  - Request more specific requirements
```

---

**Status**: Core parsing + multimodal support implemented
**Next**: pattern_matcher.md for pattern selection
**Capabilities**: Extracts structure from natural language, detects multimodal needs
