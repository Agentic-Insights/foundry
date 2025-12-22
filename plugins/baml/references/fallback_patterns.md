# Fallback Patterns Module

**Version**: 1.0.0
**Purpose**: Embedded fallback patterns when MCP unavailable

## Generic Templates

```
GENERIC_EXTRACTION_TEMPLATE = """
class {EntityName} {{
  {field1} string
  {field2} string
}}

function Extract{EntityName}(input: string) -> {EntityName} {{
  client "openai/gpt-4o-mini"

  prompt #"
    Extract the following from the input:

    {{ input }}

    {{ ctx.output_format }}
  "#
}}
"""

GENERIC_CLASSIFICATION_TEMPLATE = """
enum {CategoryName} {{
  Option1
  Option2
  Option3
}}

function Classify{CategoryName}(input: string) -> {CategoryName} {{
  client "openai/gpt-4o-mini"

  prompt #"
    Classify the following:

    {{ input }}

    {{ ctx.output_format }}
  "#
}}
"""

GENERIC_RAG_TEMPLATE = """
class SearchResult {{
  content string
  source string
  relevance float
}}

function Search(query: string, context: string[]) -> SearchResult[] {{
  client "openai/gpt-4o"

  prompt #"
    Query: {{ query }}

    Context:
    {% for doc in context %}
    {{ doc }}
    {% endfor %}

    {{ ctx.output_format }}
  "#
}}
"""

GENERIC_AGENT_TEMPLATE = """
class Action {{
  action_type string
  parameters map<string, string>
}}

function PlanAction(state: string) -> Action {{
  client "openai/gpt-4o"

  prompt #"
    Current state:
    {{ state }}

    Decide the next action.

    {{ ctx.output_format }}
  "#
}}
"""
```

## Fallback Logic

```
FUNCTION get_fallback_pattern(category, requirement_spec):
  IF category == "extraction":
    RETURN customize_template(GENERIC_EXTRACTION_TEMPLATE, requirement_spec)
  ELSE IF category == "classification":
    RETURN customize_template(GENERIC_CLASSIFICATION_TEMPLATE, requirement_spec)
  ELSE IF category == "rag":
    RETURN GENERIC_RAG_TEMPLATE
  ELSE:
    RETURN GENERIC_AGENT_TEMPLATE

FUNCTION customize_template(template, spec):
  # Replace placeholders with actual values from spec
  customized = template.replace("{EntityName}", spec.entities.output_types[0])
  # ... more customization
  RETURN customized
```

## MCP Reconnection

```
FUNCTION attempt_mcp_reconnection(max_retries=3):
  FOR attempt IN range(max_retries):
    TRY:
      mcp_interface.validate_connection()
      log(INFO, "MCP reconnected successfully")
      RETURN True
    CATCH:
      delay = 2 ** attempt  # Exponential backoff
      log(WARNING, f"MCP reconnection attempt {attempt+1} failed, retrying in {delay}s")
      sleep(delay)

  log(ERROR, "MCP reconnection failed after {max_retries} attempts")
  RETURN False
```

---

**Status**: Fallback patterns for offline operation (80% functionality)
