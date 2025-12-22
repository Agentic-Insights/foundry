# Other Languages Reference

BAML supports additional language targets beyond Python and TypeScript.

## Supported Languages

| Language | Generator Type | Status |
|----------|---------------|--------|
| Python/Pydantic | `python/pydantic` | Stable |
| Python/Pydantic v1 | `python/pydantic/v1` | Stable |
| TypeScript | `typescript` | Stable |
| TypeScript/React | `typescript/react` | Stable |
| Ruby/Sorbet | `ruby/sorbet` | Stable |
| Go | `go` | Stable |
| REST/OpenAPI | `rest/openapi` | Stable |

## Ruby Configuration

```baml
generator lang_ruby {
  output_type ruby/sorbet
  output_dir "../baml_client"
  version "0.211.2"
}
```

Ruby generates Sorbet-typed classes for static type checking.

## Go Configuration

```baml
generator lang_go {
  output_type go
  output_dir "../baml_client"
  version "0.211.2"
  client_package_name "example.com/my-project"
  on_generate "gofmt -w . && goimports -w . && go mod tidy"
}
```

**Go-specific options:**
- `client_package_name`: Go module path for imports
- `on_generate`: Post-generation commands (formatting, etc.)

## OpenAPI Generation

```baml
generator openapi {
  output_type rest/openapi
  output_dir "../openapi"
  version "0.211.2"
  on_generate "rm .gitignore"
}
```

Generates OpenAPI spec that can be used to create REST API clients in any language.

## Generator Options

### Common Options

| Option | Description |
|--------|-------------|
| `output_type` | Target language/format |
| `output_dir` | Directory for generated code |
| `version` | BAML version (must match CLI) |

### Advanced Options

| Option | Description |
|--------|-------------|
| `on_generate` | Shell command to run after generation |
| `module_format` | For TypeScript: `esm` or `commonjs` |
| `client_package_name` | For Go: module import path |

## Multiple Generators

You can have multiple generators in one project:

```baml
// Python backend
generator python {
  output_type python/pydantic
  output_dir "../backend/baml_client"
  version "0.211.2"
}

// TypeScript frontend
generator typescript {
  output_type typescript
  output_dir "../frontend/baml_client"
  version "0.211.2"
}

// API spec for other services
generator openapi {
  output_type rest/openapi
  output_dir "../api"
  version "0.211.2"
}
```

This allows the same BAML schemas to generate clients for different parts of your stack.

## Version Synchronization

**Critical:** The `version` field must match your installed BAML CLI version:

```bash
# Check CLI version
baml-cli --version

# Update generator to match
generator target {
  output_type python/pydantic
  output_dir "../baml_client"
  version "0.211.2"  // Must match!
}
```

If versions mismatch, you'll get errors during generation.

## Post-Generation Hooks

Use `on_generate` for automatic formatting:

```baml
// Python - run black and isort
generator python {
  output_type python/pydantic
  output_dir "../baml_client"
  version "0.211.2"
  on_generate "black . && isort ."
}

// Go - format and tidy
generator go {
  output_type go
  output_dir "../baml_client"
  version "0.211.2"
  on_generate "gofmt -w . && go mod tidy"
}
```
