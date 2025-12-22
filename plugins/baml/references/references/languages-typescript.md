# TypeScript + BAML Reference

TypeScript-specific patterns for BAML with generated interfaces.

## Project Setup

```bash
# Create project
mkdir my-baml-project && cd my-baml-project
npm init -y

# Add BAML
npm install @boundaryml/baml

# Initialize
mkdir baml_src
```

### generators.baml for TypeScript

```baml
// Standard CommonJS
generator target {
  output_type typescript
  output_dir "../baml_client"
  version "0.211.2"
}

// ESM module format
generator target_esm {
  output_type typescript
  output_dir "../baml_client"
  version "0.211.2"
  module_format esm
}

// React integration
generator target_react {
  output_type typescript/react
  output_dir "../baml_client"
  version "0.211.2"
}
```

### Project Structure

```
my-project/
├── baml_src/
│   ├── generators.baml
│   ├── clients.baml
│   └── *.baml
├── baml_client/           # Generated - don't edit
│   ├── index.ts
│   ├── types.ts           # TypeScript interfaces
│   └── client.ts
├── package.json
├── tsconfig.json
└── .env
```

## Generated Code Usage

### Import Pattern

```typescript
import { b } from './baml_client'
import type { Person, Invoice, LineItem } from './baml_client/types'
```

### Basic Usage (Async by default)

```typescript
// Simple extraction
const person: Person = await b.ExtractPerson(text)
console.log(person.name)  // Type-safe

// With error handling
try {
  const invoice = await b.ExtractInvoice(doc)
} catch (e) {
  if (e instanceof BamlValidationError) {
    console.error('Validation failed:', e.message)
  }
}
```

### Streaming

```typescript
// Async iteration
const stream = b.stream.ExtractData(largeDoc)
for await (const partial of stream) {
  console.log(`Progress: ${partial.items?.length ?? 0} items`)
  updateUI(partial)
}

const final = await stream.getFinalResponse()
```

## Type Safety

### Generated Interfaces

```typescript
// From baml_client/types.ts (generated)
interface Person {
  name: string
  email: string
  age?: number  // Optional
}

// Full IntelliSense in IDE
const person = await b.ExtractPerson(text)
person.name    // string
person.age     // number | undefined
```

### Union Type Handling

```typescript
import type { GetWeather, SearchWeb, Calculator } from './baml_client/types'

const result = await b.SelectTool(query)

// Type guards
function isGetWeather(r: typeof result): r is GetWeather {
  return 'location' in r && 'units' in r
}

if (isGetWeather(result)) {
  return fetchWeather(result.location, result.units)
}
```

## Image Handling

```typescript
import { Image } from '@boundaryml/baml'

// From URL
const result = await b.AnalyzeImage({
  img: Image.fromUrl('https://example.com/image.png')
})

// From file (Node.js)
import { readFileSync } from 'fs'
const buffer = readFileSync('image.jpg')
const result = await b.AnalyzeImage({
  img: Image.fromBase64('image/jpeg', buffer.toString('base64'))
})
```

## Environment Variables

```typescript
// .env file
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

// Use dotenv for Node.js
import 'dotenv/config'
import { b } from './baml_client'
```

## Next.js / React Integration

### Server Component

```typescript
// app/api/extract/route.ts
import { b } from '@/baml_client'

export async function POST(req: Request) {
  const { text } = await req.json()
  const result = await b.ExtractPerson(text)
  return Response.json(result)
}
```

### React Hook (with typescript/react generator)

```typescript
import { useExtractPerson } from './baml_client/react'

function MyComponent() {
  const { data, isLoading, error, mutate } = useExtractPerson()

  const handleExtract = () => {
    mutate({ text: inputText })
  }

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  if (data) return <div>Name: {data.name}</div>

  return <button onClick={handleExtract}>Extract</button>
}
```

## Testing

### Jest

```typescript
import { b } from './baml_client'

describe('Person Extraction', () => {
  it('extracts name and email', async () => {
    const text = 'John Smith, john@example.com'
    const result = await b.ExtractPerson(text)

    expect(result.name).toBe('John Smith')
    expect(result.email).toBe('john@example.com')
  })
})
```

### Vitest

```typescript
import { describe, it, expect } from 'vitest'
import { b } from './baml_client'

describe('extraction', () => {
  it('works', async () => {
    const result = await b.ExtractPerson(text)
    expect(result.name).toBeDefined()
  })
})
```

## Best Practices

1. **Use strict TypeScript** - `"strict": true` in tsconfig
2. **Import types separately** - `import type { ... }` for interfaces
3. **Handle async properly** - Always await or handle promises
4. **Stream for UX** - Better perceived performance
5. **Server-side only** - Don't expose API keys in browser
