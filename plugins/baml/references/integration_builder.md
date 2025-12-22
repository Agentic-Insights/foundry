# Integration Builder Module

**Version**: 1.0.0
**Purpose**: Generate framework-specific integration code

## Overview

Generates API endpoints, client code, and integration patterns for Python (FastAPI, Flask, Django), TypeScript (Next.js, Express), Ruby (Rails, Sinatra), Java (Spring Boot), Go (Gin), and C# (ASP.NET Core).

## Integration Generation

```
FUNCTION generate_integration(baml_code, framework, language):
  IF language == "python":
    RETURN generate_python_integration(baml_code, framework)
  ELSE IF language == "typescript":
    RETURN generate_typescript_integration(baml_code, framework)
  ELSE IF language == "ruby":
    RETURN generate_ruby_integration(baml_code, framework)
  ELSE IF language == "java":
    RETURN generate_java_integration(baml_code, framework)
  ELSE IF language == "golang":
    RETURN generate_go_integration(baml_code, framework)
  ELSE IF language == "csharp":
    RETURN generate_csharp_integration(baml_code, framework)
```

## Python Integration

### FastAPI
```
FUNCTION generate_python_integration(baml_code, framework):
  IF framework == "fastapi":
    RETURN """
from fastapi import FastAPI, HTTPException
from baml_client import b
from baml_client.types import {types}
from pydantic import BaseModel

app = FastAPI()

class Request(BaseModel):
    {request_fields}

@app.post("/api/{endpoint}")
async def {endpoint}(request: Request):
    try:
        result = await b.{FunctionName}(request.{param})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
```

## TypeScript Integration

### Next.js
```
FUNCTION generate_typescript_integration(baml_code, framework):
  IF framework == "nextjs":
    RETURN """
import {{ {FunctionName} }} from '@/baml_client';
import {{ NextRequest, NextResponse }} from 'next/server';

export async function POST(request: NextRequest) {{
  try {{
    const body = await request.json();
    const result = await {FunctionName}(body.input);
    return NextResponse.json(result);
  }} catch (error) {{
    return NextResponse.json(
      {{ error: error.message }},
      {{ status: 500 }}
    );
  }}
}}
"""
```

## Ruby Integration

### Rails
```
FUNCTION generate_ruby_integration(baml_code, framework):
  IF framework == "rails":
    RETURN """
# app/controllers/baml_controller.rb
class BamlController < ApplicationController
  def {action}
    result = Baml::Client.{function_name}(params[:input])
    render json: result
  rescue StandardError => e
    render json: { error: e.message }, status: :internal_server_error
  end
end
"""
```

## Java Integration

### Spring Boot
```
FUNCTION generate_java_integration(baml_code, framework):
  RETURN """
@RestController
@RequestMapping("/api")
public class BamlController {{

    @PostMapping("/{endpoint}")
    public ResponseEntity<{ReturnType}> {methodName}(@RequestBody {RequestType} request) {{
        try {{
            {ReturnType} result = BamlClient.{functionName}(request.getInput());
            return ResponseEntity.ok(result);
        }} catch (Exception e) {{
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(null);
        }}
    }}
}}
"""
```

## Go Integration

### Gin
```
FUNCTION generate_go_integration(baml_code, framework):
  RETURN """
package main

import (
    "github.com/gin-gonic/gin"
    "baml/client"
)

func {HandlerName}(c *gin.Context) {{
    var req {RequestType}
    if err := c.BindJSON(&req); err != nil {{
        c.JSON(400, gin.H{{"error": err.Error()}})
        return
    }}

    result, err := client.{FunctionName}(req.Input)
    if err != nil {{
        c.JSON(500, gin.H{{"error": err.Error()}})
        return
    }}

    c.JSON(200, result)
}}
"""
```

## C# Integration

### ASP.NET Core
```
FUNCTION generate_csharp_integration(baml_code, framework):
  RETURN """
[ApiController]
[Route("api/[controller]")]
public class BamlController : ControllerBase
{{
    [HttpPost]
    public async Task<ActionResult<{ReturnType}>> {MethodName}([FromBody] {RequestType} request)
    {{
        try
        {{
            var result = await BamlClient.{FunctionName}(request.Input);
            return Ok(result);
        }}
        catch (Exception ex)
        {{
            return StatusCode(500, new {{ error = ex.Message }});
        }}
    }}
}}
"""
```

## Monitoring Integration

```
FUNCTION generate_monitoring_hooks(language):
  # Telemetry, logging, error tracking
  RETURN """
# Monitoring setup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_baml_call(function_name, duration_ms, success):
    logger.info(f"BAML call: {{function_name}} - {{duration_ms}}ms - {{success}}")
"""
```

## Retry Logic

```
FUNCTION generate_retry_logic(language):
  RETURN """
# Retry with exponential backoff
async def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
"""
```

## Fallback Patterns

```
FUNCTION generate_fallback_patterns(language):
  RETURN """
# Graceful degradation
async def call_with_fallback(primary_func, fallback_func):
    try:
        return await primary_func()
    except Exception:
        logger.warning("Primary call failed, using fallback")
        return await fallback_func()
"""
```

---

**Status**: Integration generation for 6+ languages and frameworks
