# Utilities Module

**Version**: 1.0.0
**Purpose**: Error handling, logging, and utility functions
**Scope**: Cross-cutting concerns for all skill modules

## Overview

This module provides error handling, logging, validation utilities, and helper functions used across all skill modules. It ensures consistent error messages, debugging capabilities, and robust operation.

## Error Handling

### Error Categories

#### 1. MCP Errors
```
MCPConnectionError:
  - cause: MCP server unavailable or timeout
  - recovery: Fall back to cached patterns
  - user_message: "Operating in offline mode with cached patterns"
  - log_level: WARNING

MCPQueryError:
  - cause: Query failed or returned unexpected format
  - recovery: Retry with exponential backoff (max 3 attempts)
  - user_message: "Unable to fetch latest patterns, using cache"
  - log_level: ERROR

MCPRateLimitError:
  - cause: Too many queries in short time
  - recovery: Queue queries, implement backoff
  - user_message: "Query rate limited, please wait..."
  - log_level: WARNING
```

#### 2. Pattern Errors
```
PatternNotFoundError:
  - cause: No matching pattern for requirement
  - recovery: Use generic template for category
  - user_message: "No exact match found, using generic template"
  - log_level: INFO

PatternValidationError:
  - cause: Pattern failed validation (syntax, types, etc.)
  - recovery: Skip pattern, try next best match
  - user_message: "Pattern validation failed, trying alternative"
  - log_level: WARNING

PatternAdaptationError:
  - cause: Cannot adapt pattern to requirement
  - recovery: Fall back to ground-up generation
  - user_message: "Cannot adapt pattern, generating from scratch"
  - log_level: INFO
```

#### 3. Generation Errors
```
CodeGenerationError:
  - cause: Code synthesis failed
  - recovery: Retry with different pattern or template
  - user_message: "Generation failed, retrying with different approach"
  - log_level: ERROR

SyntaxValidationError:
  - cause: Generated code has syntax errors
  - recovery: Attempt auto-fix or regenerate
  - user_message: "Syntax error detected, attempting correction"
  - log_level: ERROR

TypeResolutionError:
  - cause: Type references cannot be resolved
  - recovery: Generate missing types or simplify
  - user_message: "Type resolution issue, adding missing definitions"
  - log_level: WARNING
```

#### 4. Cache Errors
```
CacheWriteError:
  - cause: Cannot write to cache file
  - recovery: Use memory-only cache
  - user_message: "Cache write failed, using memory cache only"
  - log_level: WARNING

CacheCorruptionError:
  - cause: Cache file is corrupted
  - recovery: Rebuild cache from MCP
  - user_message: "Cache corrupted, rebuilding..."
  - log_level: WARNING

CacheMissError:
  - cause: Requested item not in cache
  - recovery: Query MCP
  - user_message: null  # Not user-facing
  - log_level: DEBUG
```

#### 5. Validation Errors
```
CompilationError:
  - cause: Generated BAML doesn't compile
  - recovery: Provide diagnostic, suggest fixes
  - user_message: "Code validation failed: {details}"
  - log_level: ERROR

TestGenerationError:
  - cause: Cannot generate tests for function
  - recovery: Provide basic test template
  - user_message: "Test generation incomplete, manual review needed"
  - log_level: WARNING
```

### Error Handling Strategy

```
FUNCTION handle_error(error, context):
  # Classify error
  error_type = classify_error(error)

  # Log error with context
  log(error_type.log_level, f"{error_type.name}: {error.message}", context)

  # Execute recovery strategy
  recovery_result = execute_recovery(error_type.recovery, context)

  # Notify user if needed
  IF error_type.user_message:
    notify_user(error_type.user_message)

  # Return recovery result or raise if unrecoverable
  IF recovery_result.success:
    RETURN recovery_result.value
  ELSE:
    RAISE UnrecoverableError(error)
```

### Retry Logic with Exponential Backoff

```
FUNCTION retry_with_backoff(operation, max_retries=3, base_delay=1.0):
  attempt = 0

  WHILE attempt < max_retries:
    TRY:
      result = operation()
      RETURN result

    CATCH error:
      attempt += 1

      IF attempt >= max_retries:
        log(ERROR, f"Operation failed after {max_retries} attempts")
        RAISE error

      # Calculate delay with exponential backoff + jitter
      delay = base_delay * (2 ** attempt) + random(0, 1)
      log(WARNING, f"Attempt {attempt} failed, retrying in {delay}s...")
      sleep(delay)

  RAISE MaxRetriesExceeded
```

## Logging Framework

### Log Levels
```
DEBUG: Detailed diagnostic information
INFO: General informational messages
WARNING: Warning messages (recoverable issues)
ERROR: Error messages (failures with recovery)
CRITICAL: Critical errors (unrecoverable)
```

### Logging Interface

```
FUNCTION log(level, message, context=null):
  timestamp = now()
  log_entry = {
    "timestamp": timestamp.isoformat(),
    "level": level,
    "message": message,
    "context": context,
    "session_id": get_session_id()
  }

  # Format log message
  formatted = format_log_entry(log_entry)

  # Output based on environment
  IF debug_mode:
    print(formatted)  # Console output

  # Store in log buffer (last 100 entries)
  log_buffer.append(log_entry)
  IF len(log_buffer) > 100:
    log_buffer.pop(0)

  # Persist critical errors
  IF level IN [ERROR, CRITICAL]:
    persist_log_entry(log_entry)
```

### Structured Logging

```
FUNCTION log_operation(operation_name, params, result, duration_ms):
  log(INFO, f"Operation completed", {
    "operation": operation_name,
    "params": params,
    "result_type": type(result).__name__,
    "duration_ms": duration_ms,
    "success": result.success if hasattr(result, 'success') else True
  })
```

### Performance Logging

```
FUNCTION log_performance(component, metric_name, value, unit="ms"):
  log(DEBUG, f"Performance metric", {
    "component": component,
    "metric": metric_name,
    "value": value,
    "unit": unit,
    "timestamp": now()
  })

  # Update performance stats
  performance_stats[component][metric_name].append(value)
```

## Validation Utilities

### BAML Syntax Validation

```
FUNCTION validate_baml_syntax(code):
  # Check basic structure
  IF not has_valid_structure(code):
    RETURN False, "Invalid BAML structure"

  # Check type definitions
  types = extract_types(code)
  FOR type_def IN types:
    IF not is_valid_type_definition(type_def):
      RETURN False, f"Invalid type: {type_def.name}"

  # Check function definitions
  functions = extract_functions(code)
  FOR function IN functions:
    IF not is_valid_function_definition(function):
      RETURN False, f"Invalid function: {function.name}"

  # Check client definitions
  clients = extract_clients(code)
  FOR client IN clients:
    IF not is_valid_client_definition(client):
      RETURN False, f"Invalid client: {client.name}"

  RETURN True, "Valid BAML syntax"
```

### Type Checking

```
FUNCTION validate_type_references(code):
  defined_types = extract_defined_types(code)
  referenced_types = extract_referenced_types(code)

  undefined = []
  FOR ref_type IN referenced_types:
    IF ref_type NOT IN defined_types AND ref_type NOT IN BUILTIN_TYPES:
      undefined.append(ref_type)

  IF undefined:
    RETURN False, f"Undefined types: {', '.join(undefined)}"

  RETURN True, "All types defined"
```

### Circular Dependency Detection

```
FUNCTION check_circular_dependencies(types):
  dependency_graph = build_dependency_graph(types)

  # DFS cycle detection
  visited = set()
  recursion_stack = set()

  FOR type_name IN dependency_graph.keys():
    IF detect_cycle_dfs(type_name, dependency_graph, visited, recursion_stack):
      RETURN False, f"Circular dependency involving: {type_name}"

  RETURN True, "No circular dependencies"

FUNCTION detect_cycle_dfs(node, graph, visited, rec_stack):
  visited.add(node)
  rec_stack.add(node)

  FOR neighbor IN graph.get(node, []):
    IF neighbor NOT IN visited:
      IF detect_cycle_dfs(neighbor, graph, visited, rec_stack):
        RETURN True
    ELSE IF neighbor IN rec_stack:
      RETURN True  # Cycle found

  rec_stack.remove(node)
  RETURN False
```

## Helper Functions

### Token Counting

```
FUNCTION count_tokens(text):
  # Approximate token count (GPT tokenizer approximation)
  # ~4 characters per token on average
  char_count = len(text)
  token_estimate = char_count / 4

  # More accurate for code: count words, punctuation, newlines
  words = text.split()
  punctuation = count_punctuation(text)
  newlines = text.count('\n')

  token_count = len(words) + punctuation + newlines * 0.5

  RETURN int(token_count)
```

### Hash Generation

```
FUNCTION generate_hash(data):
  # Create deterministic hash for caching
  import hashlib

  IF isinstance(data, dict):
    data_str = json.dumps(data, sort_keys=True)
  ELSE:
    data_str = str(data)

  hash_obj = hashlib.sha256(data_str.encode('utf-8'))
  RETURN hash_obj.hexdigest()[:16]  # First 16 chars
```

### Text Extraction

```
FUNCTION extract_entities(text):
  # Simple entity extraction (nouns, proper nouns)
  # For production, could use NLP library

  words = text.split()
  entities = []

  FOR word IN words:
    IF is_capitalized(word) AND word NOT IN COMMON_WORDS:
      entities.append(word)
    ELSE IF word.lower() IN ENTITY_KEYWORDS:
      entities.append(word)

  RETURN list(set(entities))  # Unique entities

FUNCTION extract_verbs(text):
  # Extract action verbs (extract, parse, classify, etc.)
  words = text.lower().split()
  verbs = []

  FOR word IN words:
    IF word IN ACTION_VERBS:
      verbs.append(word)

  RETURN verbs
```

### String Formatting

```
FUNCTION format_code_block(code, language="baml"):
  # Format code for display
  RETURN f"```{language}\n{code}\n```"

FUNCTION truncate_string(text, max_length=100):
  # Truncate with ellipsis
  IF len(text) <= max_length:
    RETURN text
  RETURN text[:max_length-3] + "..."

FUNCTION indent_code(code, spaces=2):
  # Indent code block
  lines = code.split('\n')
  indent = ' ' * spaces
  RETURN '\n'.join(indent + line for line in lines)
```

### Time Utilities

```
FUNCTION now():
  # Current timestamp
  import datetime
  RETURN datetime.datetime.utcnow()

FUNCTION format_duration(start_time, end_time):
  # Human-readable duration
  delta = end_time - start_time
  ms = delta.total_seconds() * 1000

  IF ms < 1000:
    RETURN f"{int(ms)}ms"
  ELSE IF ms < 60000:
    RETURN f"{ms/1000:.2f}s"
  ELSE:
    RETURN f"{ms/60000:.2f}min"
```

### File Operations

```
FUNCTION safe_read_file(file_path):
  TRY:
    with open(file_path, 'r', encoding='utf-8') as f:
      RETURN f.read()
  CATCH FileNotFoundError:
    log(WARNING, f"File not found: {file_path}")
    RETURN null
  CATCH PermissionError:
    log(ERROR, f"Permission denied: {file_path}")
    RETURN null

FUNCTION safe_write_file(file_path, content):
  TRY:
    # Ensure directory exists
    create_directory_if_not_exists(path.dirname(file_path))

    with open(file_path, 'w', encoding='utf-8') as f:
      f.write(content)
    RETURN True
  CATCH PermissionError:
    log(ERROR, f"Cannot write to: {file_path}")
    RETURN False
```

## Constants

### Common Keywords
```
PATTERN_KEYWORDS = {
  "extraction": ["extract", "parse", "structure", "data", "form", "ocr", "document"],
  "classification": ["classify", "categorize", "label", "identify", "sentiment", "intent"],
  "rag": ["search", "retrieve", "context", "citation", "source", "reference"],
  "agents": ["agent", "plan", "execute", "tool", "workflow", "action", "decision"]
}

ACTION_VERBS = [
  "extract", "parse", "classify", "categorize", "search", "retrieve",
  "generate", "create", "build", "analyze", "detect", "identify"
]

BUILTIN_TYPES = [
  "string", "int", "float", "bool", "null",
  "image", "audio", "video"  # Multimodal types
]
```

### Error Messages
```
ERROR_MESSAGES = {
  "mcp_unavailable": "MCP server unavailable. Operating in offline mode with cached patterns.",
  "pattern_not_found": "No matching pattern found. Using generic template.",
  "validation_failed": "Generated code validation failed. Please review.",
  "syntax_error": "Syntax error in generated code: {details}",
  "type_error": "Type resolution failed: {details}",
  "cache_error": "Cache operation failed. Using memory cache only."
}
```

## Debug Mode

### Enable Debug Logging
```
debug_mode = False

FUNCTION set_debug_mode(enabled):
  global debug_mode
  debug_mode = enabled

  IF enabled:
    log(INFO, "Debug mode enabled")
    log(DEBUG, "Detailed logging active")
```

### Debug Output
```
FUNCTION debug_print(message, data=null):
  IF debug_mode:
    formatted_data = json.dumps(data, indent=2) if data else ""
    print(f"[DEBUG] {message}")
    IF formatted_data:
      print(formatted_data)
```

### Trace Execution
```
FUNCTION trace_function(func):
  # Decorator to trace function execution

  FUNCTION wrapper(*args, **kwargs):
    IF debug_mode:
      log(DEBUG, f"Entering: {func.__name__}")
      log(DEBUG, f"Args: {args}, Kwargs: {kwargs}")

    start_time = now()

    TRY:
      result = func(*args, **kwargs)
      duration = (now() - start_time).total_seconds() * 1000

      IF debug_mode:
        log(DEBUG, f"Exiting: {func.__name__}")
        log(DEBUG, f"Duration: {duration}ms")
        log(DEBUG, f"Result type: {type(result).__name__}")

      RETURN result

    CATCH error:
      duration = (now() - start_time).total_seconds() * 1000
      log(ERROR, f"Error in {func.__name__}: {error}")
      log(DEBUG, f"Duration before error: {duration}ms")
      RAISE

  RETURN wrapper
```

## Integration Points

### With All Modules
- All modules import utils for error handling
- All modules use logging functions
- All modules use validation utilities

### Error Propagation
```
# Modules raise specific errors
RAISE PatternNotFoundError("No extraction pattern for: {requirement}")

# Utils catches, logs, and handles recovery
TRY:
  pattern = pattern_matcher.find_pattern(requirement)
CATCH PatternNotFoundError as e:
  handle_error(e, {"requirement": requirement, "module": "pattern_matcher"})
  pattern = get_generic_template(category)
```

---

**Status**: Error handling framework complete
**Usage**: Import by all skill modules
**Coverage**: MCP, patterns, generation, cache, validation errors
**Next**: Begin Phase 3 - User Story 1 implementation
