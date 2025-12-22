# BAML Pattern Library

This document catalogs common BAML patterns organized by use case category. Each pattern includes type definitions, function signatures, and real-world examples.

## Pattern Categories

### 1. Extraction Patterns

**Use Case**: Parse unstructured text into structured data

**Common Scenarios**:
- Invoice/receipt extraction
- Resume parsing
- Form data extraction
- Document analysis
- Medical records
- Legal contracts

**Pattern Structure**:
```baml
class EntityType {
  field1 string @description("Clear field description")
  field2 int @description("Numeric data")
  optional_field string? @description("May be absent")
  list_field string[] @description("Multiple values")
}

function ExtractEntity(input: string) -> EntityType {
  client GPT5
  prompt #"
    Extract structured data from this text:

    {{ input }}

    {{ ctx.output_format }}
  "#
}
```

**Key Features**:
- Optional fields with `?`
- Array fields with `[]`
- Clear descriptions for each field
- Simple extraction prompt

**Example - Invoice Extraction**:
```baml
class Invoice {
  invoice_number string @description("Invoice ID")
  date string @description("Invoice date")
  total float @description("Total amount") @assert(this > 0)
  items InvoiceItem[] @description("Line items")
}

class InvoiceItem {
  description string
  quantity int @assert(this > 0)
  price float @assert(this > 0)
  total float @assert(this > 0)
}

function ExtractInvoice(invoice_text: string) -> Invoice {
  client GPT5
  prompt #"
    Extract invoice details from this text:

    {{ invoice_text }}

    {{ ctx.output_format }}
  "#
}
```

### 2. Classification Patterns

**Use Case**: Categorize inputs into predefined classes

**Common Scenarios**:
- Sentiment analysis
- Intent detection
- Content moderation
- Priority classification
- Topic categorization
- Language detection

**Pattern Structure**:
```baml
enum Category {
  CATEGORY_A @description("When X conditions")
  CATEGORY_B @description("When Y conditions")
  CATEGORY_C @description("Default case")
}

function ClassifyInput(text: string) -> Category {
  client GPT5Mini  // Fast model for classification
  prompt #"
    Classify this text into one of these categories:

    {{ text }}

    {{ ctx.output_format }}
  "#
}
```

**Key Features**:
- Enum types for fixed categories
- Fast models (GPT-5-mini, Claude Haiku)
- Optional confidence scores
- Descriptions on enum values

**Example - Sentiment Analysis**:
```baml
enum Sentiment {
  POSITIVE @description("Happy, satisfied, enthusiastic")
  NEGATIVE @description("Angry, disappointed, frustrated")
  NEUTRAL @description("Factual, balanced, no emotion")
}

class SentimentResult {
  sentiment Sentiment
  confidence float @description("0-1 confidence score")
  reasoning string @description("Why this classification")
}

function ClassifySentiment(text: string) -> SentimentResult {
  client GPT5Mini
  prompt #"
    Analyze the sentiment of this text:

    {{ text }}

    Provide your classification with reasoning.

    {{ ctx.output_format }}
  "#
}
```

### 3. RAG (Retrieval-Augmented Generation) Patterns

**Use Case**: Generate answers with citations and sources

**Common Scenarios**:
- Document Q&A
- Knowledge base search
- Research assistance
- Legal discovery
- Medical literature review
- Customer support

**Pattern Structure**:
```baml
class Citation {
  source string @description("Source identifier")
  quote string @description("Relevant excerpt")
  relevance float @description("0-1 relevance score")
}

class AnswerWithCitations {
  answer string @description("Main answer")
  citations Citation[] @description("Supporting sources")
  confidence float @description("Answer confidence")
}

function AnswerQuestion(
  question: string,
  context: string
) -> AnswerWithCitations {
  client GPT5
  prompt #"
    Answer this question using the provided context:

    Question: {{ question }}

    Context: {{ context }}

    Provide citations for all claims.

    {{ ctx.output_format }}
  "#
}
```

**Key Features**:
- Citation tracking
- Source attribution
- Confidence scoring
- Quote extraction

**Example - Document Q&A**:
```baml
class Source {
  doc_id string
  page_number int
  text string @description("Relevant passage")
}

class DocumentAnswer {
  answer string @description("Direct answer")
  sources Source[] @description("Supporting passages")
  confidence float @assert(this >= 0 && this <= 1)
  needs_clarification bool @description("Question ambiguous?")
}

function QueryDocuments(
  question: string,
  documents: string
) -> DocumentAnswer {
  client GPT5
  prompt #"
    Answer this question based on the documents:

    Question: {{ question }}

    Documents:
    {{ documents }}

    Cite specific passages with doc_id and page_number.

    {{ ctx.output_format }}
  "#
}
```

### 4. Agent Patterns

**Use Case**: Multi-step reasoning and tool usage

**Common Scenarios**:
- Task planning
- Tool selection
- Multi-step workflows
- Decision trees
- State machines
- Error recovery

**Pattern Structure**:
```baml
enum ToolType {
  SEARCH @description("Search knowledge base")
  CALCULATE @description("Perform calculation")
  QUERY @description("Database query")
}

class ToolCall {
  tool ToolType @description("Which tool to use")
  params string @description("Tool parameters as JSON")
  reasoning string @description("Why this tool")
}

class AgentPlan {
  steps ToolCall[] @description("Ordered steps")
  expected_outcome string @description("What we'll achieve")
}

function PlanTask(task: string) -> AgentPlan {
  client GPT5
  prompt #"
    Create a plan to accomplish this task:

    {{ task }}

    Break it into tool calls with clear reasoning.

    {{ ctx.output_format }}
  "#
}
```

**Key Features**:
- Union types for tool selection
- Step-by-step planning
- Reasoning traces
- State management

**Example - Research Agent**:
```baml
enum ResearchAction {
  SEARCH_WEB @description("Search internet")
  SEARCH_PAPERS @description("Search academic papers")
  READ_DOCUMENT @description("Read specific document")
  SYNTHESIZE @description("Combine findings")
  DONE @description("Task complete")
}

class ResearchStep {
  action ResearchAction
  query string @description("Search query or doc URL")
  reasoning string @description("Why this step")
}

class ResearchPlan {
  objective string @description("Research goal")
  steps ResearchStep[] @description("Ordered actions")
  success_criteria string @description("How to know we're done")
}

function PlanResearch(topic: string) -> ResearchPlan {
  client GPT5
  prompt #"
    Create a research plan for this topic:

    {{ topic }}

    Plan a sequence of search and synthesis steps.

    {{ ctx.output_format }}
  "#
}
```

## Multimodal Patterns

### Vision + Extraction

**Use Case**: Extract data from images

```baml
class ImageContent {
  description string @description("What's in the image")
  text string @description("Any visible text")
  objects string[] @description("Detected objects")
}

function AnalyzeImage(image: image) -> ImageContent {
  client GPT5Vision
  prompt #"
    Analyze this image and extract all relevant information:

    {{ image }}

    {{ ctx.output_format }}
  "#
}
```

### Audio + Transcription

**Use Case**: Process audio inputs

```baml
class Transcript {
  text string @description("Transcribed speech")
  speaker_count int @description("Number of speakers")
  sentiment Sentiment @description("Overall tone")
}

function TranscribeAudio(audio: audio) -> Transcript {
  client GPT5Audio
  prompt #"
    Transcribe and analyze this audio:

    {{ audio }}

    {{ ctx.output_format }}
  "#
}
```

## Advanced Patterns

### Hierarchical Extraction

**Use Case**: Nested document structures

```baml
class Section {
  title string
  content string
  subsections Section[] @description("Nested sections")
}

class Document {
  title string
  author string
  sections Section[]
}

function ParseDocument(doc: string) -> Document {
  client GPT5
  prompt #"
    Parse this document into a hierarchical structure:

    {{ doc }}

    {{ ctx.output_format }}
  "#
}
```

### Validation + Correction

**Use Case**: Extract and validate data

```baml
class ValidatedData {
  data ExtractedType
  valid bool @description("Passes validation?")
  errors string[] @description("Validation errors")
  corrected ExtractedType? @description("Auto-corrected version")
}

function ExtractAndValidate(input: string) -> ValidatedData {
  client GPT5
  prompt #"
    Extract data and validate it:

    {{ input }}

    If invalid, suggest corrections.

    {{ ctx.output_format }}
  "#
}
```

### Multi-step Reasoning

**Use Case**: Chain of thought processing

```baml
class ReasoningStep {
  thought string @description("Current thinking")
  conclusion string @description("What we learned")
}

class ReasonedAnswer {
  steps ReasoningStep[] @description("Reasoning chain")
  final_answer string @description("Final conclusion")
  confidence float
}

function ReasonAbout(question: string) -> ReasonedAnswer {
  client GPT5
  prompt #"
    Reason step-by-step about this question:

    {{ question }}

    Show your thinking process.

    {{ ctx.output_format }}
  "#
}
```

## Pattern Selection Guide

| Use Case | Pattern | Model Choice | Typical Latency |
|----------|---------|--------------|-----------------|
| Simple extraction | Extraction | GPT-5-mini | <2s |
| Complex extraction | Extraction | GPT-5 | 3-5s |
| Classification | Classification | GPT-5-mini | <1s |
| Q&A with sources | RAG | GPT-5 | 3-5s |
| Multi-step planning | Agent | GPT-5 | 5-10s |
| Image analysis | Vision | GPT-5-Vision | 4-6s |
| Nested structures | Hierarchical | GPT-5 | 5-8s |

## Optimization Tips

1. **Use Fast Models for Simple Tasks**: GPT-5-mini for classification, GPT-5 for complex reasoning
2. **Minimize Optional Fields**: Fewer `?` fields = more predictable output
3. **Clear Descriptions**: Better descriptions = better extraction
4. **Assertions for Validation**: Use `@assert` to catch invalid data
5. **Break Complex Tasks**: Multiple simple functions > one complex function

---

**References**:
- [BAML Examples Repository](https://github.com/BoundaryML/baml-examples)
- [Pattern Best Practices](https://docs.boundaryml.com/guides/patterns)
