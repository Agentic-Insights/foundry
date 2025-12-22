# Code Generator Module

**Version**: 1.0.0
**Purpose**: Synthesize complete BAML code from patterns and specifications
**Supports**: Types, functions, clients, multimodal, optimization

## Overview

The Code Generator is the core synthesis engine that transforms requirement specifications and matched patterns into production-ready BAML code. It generates types, functions, clients, and applies optimizations.

## Generation Pipeline

```
FUNCTION generate(requirement_spec, patterns):
  # Step 1: Select best pattern
  template = pattern_matcher.select_template(requirement_spec, patterns)

  # Step 2: Generate types
  types = generate_types(requirement_spec, template)

  # Step 3: Generate functions
  functions = generate_functions(requirement_spec, template, types)

  # Step 4: Generate clients
  clients = generate_clients(requirement_spec, template)

  # Step 5: Assemble code
  baml_code = assemble_baml_code(types, functions, clients)

  # Step 6: Optimize
  optimized = optimize_code(baml_code, requirement_spec)

  # Step 7: Validate
  validation = validator.validate(optimized)

  IF not validation.valid:
    RETURN handle_validation_errors(optimized, validation)

  RETURN {
    "baml_code": optimized,
    "metadata": {
      "pattern_used": template.pattern.name,
      "token_count": count_tokens(optimized),
      "generation_time_ms": elapsed_time
    }
  }
```

## Type Generation

```
FUNCTION generate_types(requirement_spec, template):
  types = []
  entities = requirement_spec.entities.output_types

  FOR entity IN entities:
    # Infer fields
    fields = infer_fields_for_entity(entity, requirement_spec)

    # Generate class definition
    class_def = generate_class(entity, fields, requirement_spec)
    types.append(class_def)

  RETURN types

FUNCTION generate_class(name, fields, spec):
  code = f"class {name} {{\n"

  FOR field IN fields:
    field_type = infer_field_type(field, spec)
    optional = "?" if field.is_optional else ""
    desc = f' @description("{field.description}")' if field.description else ""

    code += f"  {field.name} {field_type}{optional}{desc}\n"

  code += "}"
  RETURN code
```

## Function Generation

```
FUNCTION generate_functions(requirement_spec, template, types):
  functions = []

  # Determine function name and signature
  func_name = generate_function_name(requirement_spec)
  input_params = generate_input_params(requirement_spec)
  return_type = types[0].name if len(types) > 0 else "string"

  # Generate prompt
  prompt = generate_prompt(requirement_spec, template)

  # Select client
  client = select_client_for_function(requirement_spec)

  # Assemble function
  function = f"""function {func_name}({input_params}) -> {return_type} {{
  client "{client}"

  prompt #"
{prompt}
  "#
}}"""

  functions.append(function)
  RETURN functions
```

## Vision Model Configuration

```
FUNCTION generate_vision_client(requirement_spec):
  IF not requirement_spec.multimodal.requires_vision_model:
    RETURN None

  recommended = requirement_spec.multimodal.recommended_model

  client_code = f"""client VisionModel {{
  provider "{recommended.provider}"
  options {{
    model "{recommended.model}"
    temperature 0.0
    max_tokens 2000
  }}
}}"""

  RETURN client_code
```

## Multimodal Type Generation

```
FUNCTION generate_multimodal_types(requirement_spec):
  types = []

  IF "image" IN requirement_spec.multimodal.input_types:
    # Image parameter already supported natively in BAML
    # Just ensure function signature includes: param_name: image
    pass

  IF "audio" IN requirement_spec.multimodal.input_types:
    # Audio support (future)
    types.append("// Audio type: use image type for now")

  RETURN types
```

## Prompt Synthesis

```
FUNCTION generate_prompt(requirement_spec, template):
  prompt = ""

  # Task description
  category = requirement_spec.category
  task_verb = {
    "extraction": "Extract",
    "classification": "Classify",
    "rag": "Search and retrieve",
    "agents": "Plan and execute"
  }[category]

  prompt += f"{task_verb} the following information.\n\n"

  # Input injection
  FOR param IN requirement_spec.entities.input_types:
    prompt += f"{{{{ {param} }}}}\n\n"

  # Constraints
  IF len(requirement_spec.constraints) > 0:
    prompt += "IMPORTANT:\n"
    FOR constraint IN requirement_spec.constraints:
      prompt += f"- {constraint.rule}\n"
    prompt += "\n"

  # Output format
  prompt += "{{ ctx.output_format }}"

  RETURN prompt
```

## Client Generation

```
FUNCTION generate_clients(requirement_spec, template):
  clients = []

  # Vision client if needed
  IF requirement_spec.multimodal.requires_vision_model:
    clients.append(generate_vision_client(requirement_spec))

  # Fast client for classification
  IF requirement_spec.category == "classification":
    clients.append(generate_fast_client())

  # Default client
  IF len(clients) == 0:
    clients.append(generate_default_client())

  RETURN clients

FUNCTION generate_default_client():
  RETURN """client DefaultGPT4 {
  provider "openai"
  options {
    model "gpt-4o-mini"
    temperature 0.1
  }
}"""
```

## Code Assembly

```
FUNCTION assemble_baml_code(types, functions, clients):
  code = "// Generated by BAML Code Generation Skill\n"
  code += f"// Generated: {now().isoformat()}\n\n"

  # Types first
  IF len(types) > 0:
    code += "// Types\n"
    FOR type_def IN types:
      code += type_def + "\n\n"

  # Clients
  IF len(clients) > 0:
    code += "// Clients\n"
    FOR client IN clients:
      code += client + "\n\n"

  # Functions
  IF len(functions) > 0:
    code += "// Functions\n"
    FOR function IN functions:
      code += function + "\n\n"

  RETURN code
```

## Optimization

```
FUNCTION optimize_code(baml_code, requirement_spec):
  optimization_level = requirement_spec.get("optimization_level", "standard")

  IF optimization_level == "standard":
    # Basic optimizations
    optimized = remove_redundant_descriptions(baml_code)
    optimized = compress_prompts(optimized)

  ELSE IF optimization_level == "aggressive":
    # Aggressive optimizations
    optimized = remove_redundant_descriptions(baml_code)
    optimized = compress_prompts(optimized)
    optimized = consolidate_types(optimized)
    optimized = apply_aliases(optimized)

  ELSE:
    optimized = baml_code

  RETURN optimized
```

## Metadata Tracking

```
FUNCTION generate_metadata(baml_code, requirement_spec, generation_time_ms):
  RETURN {
    "pattern_used": requirement_spec.category,
    "token_count": count_tokens(baml_code),
    "optimization_savings": calculate_savings(baml_code),
    "generation_time_ms": generation_time_ms,
    "generation_cost": estimate_cost(baml_code),
    "compilation_success": True,
    "features_used": requirement_spec.features
  }
```

## Fallback Code Generation

```
FUNCTION generate_from_generic_template(requirement_spec):
  # When no pattern matches, use generic template
  category = requirement_spec.category

  IF category == "extraction":
    RETURN generate_generic_extraction(requirement_spec)
  ELSE IF category == "classification":
    RETURN generate_generic_classification(requirement_spec)
  ELSE IF category == "rag":
    RETURN generate_generic_rag(requirement_spec)
  ELSE:
    RETURN generate_generic_agent(requirement_spec)
```

---

**Status**: Core code generation with multimodal and optimization
**Next**: output_formatter.md
