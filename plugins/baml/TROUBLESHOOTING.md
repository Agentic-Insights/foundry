# BAML Code Generation Skill - Troubleshooting Guide

**Version**: 1.0.0
**Last Updated**: 2025-01-25

## Common Issues

### 1. MCP Server Unavailable

**Error**: `MCP server unavailable`

**Causes**:
- MCP server not installed
- Network connectivity issues
- Server configuration problems

**Solutions**:
1. Verify MCP server installation:
   ```bash
   claude mcp add "baml_Docs" --scope user -- npx -y mcp-remote https://gitmcp.io/BoundaryML/baml
   ```

2. Check MCP server status in Claude Code settings

3. If unavailable, skill will use cached patterns (offline mode)
   - Functionality: ~80% (cached patterns only)
   - Warning: "Operating in offline mode with cached patterns"

**Workaround**: Continue using cached patterns, manually refresh when connection restored

---

### 2. Pattern Not Found

**Error**: `No matching pattern found for requirement`

**Causes**:
- Requirement too vague or novel
- No similar examples in repository
- Cache miss with MCP unavailable

**Solutions**:
1. **Provide more specific requirements**:
   - Bad: "Process documents"
   - Good: "Extract invoice data from images including line items and totals"

2. **Specify pattern category**:
   - "Generate BAML extraction function for..."
   - "Create BAML classification function for..."

3. **Use generic template**: Skill will automatically use generic template for category

---

### 3. Generated Code Validation Failed

**Error**: `Syntax error in generated code` or `Type resolution failed`

**Causes**:
- Complex nested types
- Circular type dependencies
- Invalid BAML syntax in generated code

**Solutions**:
1. **Check validation errors**: Skill provides detailed diagnostics

2. **Simplify requirements**: Break complex requirements into smaller parts

3. **Regenerate with different approach**: Retry generation

4. **Manual fix**: Apply suggested corrections from validation output

---

### 4. Compilation Errors

**Error**: `Generated code doesn't compile`

**Causes**:
- Missing type definitions
- Invalid function signatures
- Client configuration errors

**Solutions**:
1. **Run BAML compiler**:
   ```bash
   baml-cli generate
   ```

2. **Check error messages**: BAML compiler provides specific line numbers

3. **Verify all types are defined**: Check that referenced types exist

4. **Check client configuration**: Ensure provider/model names are correct

---

### 5. Multimodal Functions Not Working

**Error**: `Model reports "I don't see the image"`

**Cause**: Missing image parameter in prompt (THE #1 BAML GOTCHA!)

**Solution**:
**CRITICAL**: Ensure image parameter is included in prompt body:

```baml
// WRONG - Image not visible to model
function ExtractFromImage(page_image: image) -> Result {
  client VisionModel
  prompt #"
    Extract data from this image.
    {{ ctx.output_format }}
  "#
}

// CORRECT - Image visible to model
function ExtractFromImage(page_image: image) -> Result {
  client VisionModel
  prompt #"
    Extract data from this image.

    {{ page_image }}  // ← MUST INCLUDE THIS!

    {{ ctx.output_format }}
  "#
}
```

**Reference**: See CLAUDE.md BAML Development section for detailed multimodal guidance

---

### 6. Cache Issues

**Error**: `Cache write failed` or `Cache corrupted`

**Causes**:
- File system permissions
- Corrupted cache file
- Disk space issues

**Solutions**:
1. **Check permissions**: Ensure write access to `baml-claude-skill/cache/`

2. **Clear cache**:
   ```bash
   rm baml-claude-skill/cache/*.json
   ```
   Skill will rebuild cache automatically

3. **Check disk space**: Ensure sufficient space available

---

### 7. Performance Issues

**Error**: `Generation taking too long`

**Causes**:
- Complex requirements
- MCP query delays
- Large pattern library

**Solutions**:
1. **Simplify requirements**: Break into smaller tasks

2. **Use cached patterns**: Subsequent generations are faster

3. **Check MCP connectivity**: Slow network affects performance

**Expected Times**:
- Simple function: <5s
- Complex system: <30s

---

### 8. Test Generation Incomplete

**Error**: `Tests not covering all functions`

**Causes**:
- Complex function signatures
- Unknown input/output types
- Framework not supported

**Solutions**:
1. **Review generated tests**: Add missing test cases manually

2. **Specify test requirements explicitly**:
   - "Include edge cases for empty input"
   - "Add tests for error handling"

3. **Supported frameworks**:
   - Python: pytest
   - TypeScript: Jest
   - Ruby: RSpec

---

### 9. Integration Code Not Working

**Error**: `Framework integration has errors`

**Causes**:
- Framework version mismatch
- Missing dependencies
- Incorrect configuration

**Solutions**:
1. **Check framework version**: Ensure compatible version installed

2. **Install dependencies**:
   ```bash
   # Python
   pip install baml-py fastapi uvicorn

   # TypeScript
   npm install @boundaryml/baml
   ```

3. **Review generated code**: May need minor adjustments for your setup

4. **Supported frameworks**:
   - Python: FastAPI, Flask, Django
   - TypeScript: Next.js, Express, NestJS
   - Ruby: Rails, Sinatra
   - Java: Spring Boot
   - Go: Gin, Echo
   - C#: ASP.NET Core

---

### 10. Cost Exceeds Target

**Error**: `Generation cost above $0.02 target`

**Causes**:
- Large prompt sizes
- Multiple MCP queries
- Complex nested types

**Solutions**:
1. **Apply aggressive optimization**:
   - Request optimization level: "aggressive"

2. **Simplify types**: Reduce nested structures

3. **Use caching**: Cached generations are cheaper

4. **Monitor metrics**: Check token counts in metadata

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| MCP-001 | MCP server unavailable | Check installation, use cached patterns |
| MCP-002 | MCP query timeout | Retry, check network |
| MCP-003 | MCP rate limited | Wait, implement backoff |
| PAT-001 | Pattern not found | Provide more specific requirements |
| PAT-002 | Pattern validation failed | Use alternative pattern |
| GEN-001 | Code generation failed | Retry with different approach |
| GEN-002 | Syntax validation failed | Check error details, manual fix |
| GEN-003 | Type resolution failed | Define missing types |
| CACHE-001 | Cache write error | Check permissions |
| CACHE-002 | Cache corrupted | Clear and rebuild cache |
| TEST-001 | Test generation incomplete | Review and complete manually |
| INT-001 | Integration code error | Check framework compatibility |

---

## Debug Mode

Enable detailed logging:

```
Request: "Enable debug mode for BAML generation"

Claude will output:
- Detailed MCP queries
- Pattern matching scores
- Code generation steps
- Validation details
- Performance metrics
```

---

## Getting Help

1. **Check this guide** for common issues

2. **Review generated metadata** for clues:
   - Token counts
   - Pattern used
   - Validation errors

3. **Enable debug mode** for detailed logs

4. **Check BAML documentation**:
   - Skill queries MCP automatically
   - Or visit: https://docs.boundaryml.com

5. **Report issues**:
   - Provide: requirement text, error message, generated code
   - Include: metadata and debug logs if available

---

## Tips for Success

### Writing Good Requirements

**Do**:
- Be specific about data to extract/classify
- Mention input types (image, text, pdf)
- Specify validation rules if needed
- Include multimodal keywords ("image", "vision") when relevant

**Don't**:
- Be too vague ("process documents")
- Omit input/output types
- Assume default behavior

### Optimizing Performance

1. **Use caching**: Repeated similar requests are faster
2. **Batch related requests**: Generate multiple related functions at once
3. **Simplify first**: Start simple, add complexity iteratively
4. **Cache warmup**: First request slower (cold start)

### Ensuring Quality

1. **Review generated code**: Always validate output
2. **Run tests**: Execute generated tests to verify
3. **Check compilation**: Run `baml-cli generate`
4. **Iterate**: Refine requirements based on output

---

**Need More Help?**

Check the [quickstart guide](../specs/001-baml-codegen-skill/quickstart.md) for usage examples.
