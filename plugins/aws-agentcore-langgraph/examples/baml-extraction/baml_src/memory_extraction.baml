// Memory Event Extraction for AWS Bedrock AgentCore
// Type-safe extraction of conversation messages from memory events

// ============================================
// Schema: AgentCore Memory Event Structure
// ============================================

// Role enum with strict validation
enum MessageRole {
  USER
  ASSISTANT
  SYSTEM
}

// Extracted conversation message (output format)
class ConversationMessage {
  role MessageRole @description("The role of the message sender")
  content string @description("The text content of the message")
}

// Agent response with optional structured metadata
class AgentResponse {
  main_response string @description("The primary response content from the agent")
  tools_used string[]? @description("List of tools that were invoked during this turn")
  confidence float? @description("Confidence score from 0.0 to 1.0")
  requires_followup bool @description("Whether the agent suggests a follow-up question")
}

// Complete conversation with metadata
class Conversation {
  messages ConversationMessage[] @description("Ordered list of messages in the conversation")
  turn_count int @description("Number of conversation turns (non-negative)")
  has_tool_calls bool @description("Whether any tools were called in this conversation")
}

// ============================================
// Extraction Functions
// ============================================

// Extract conversation messages from raw AgentCore memory events
// This replaces the error-prone manual parsing in agent.py lines 88-112
function ExtractConversation(raw_events: string) -> Conversation {
  client Extractor
  prompt #"
    You are a precise JSON parser. Extract conversation messages from AWS Bedrock AgentCore memory events.

    The input is raw memory event data with nested structure:
    - events is a list of event objects
    - each event has a payload list
    - each payload item may have a "conversational" field
    - conversational contains role (USER/ASSISTANT) and content.text

    Extract ALL messages in chronological order.

    Raw events data:
    {{ raw_events }}

    {{ ctx.output_format }}
  "#
}

// Extract and enhance an agent response with metadata
function ExtractAgentResponse(raw_response: string, tool_names: string) -> AgentResponse {
  client Extractor
  prompt #"
    Analyze this agent response and extract structured information.

    Agent response:
    {{ raw_response }}

    Available tools that may have been used: {{ tool_names }}

    Determine:
    1. The main response content
    2. Which tools (if any) were used (based on response content patterns)
    3. Estimate confidence (high confidence = definitive answers, low = uncertain/hedged language)
    4. Whether a follow-up question is warranted

    {{ ctx.output_format }}
  "#
}

// Validate and normalize a single message
function ValidateMessage(role: string, content: string) -> ConversationMessage {
  client Extractor
  prompt #"
    Normalize this message into the correct format.

    Input role (may be lowercase or uppercase): {{ role }}
    Input content: {{ content }}

    Rules:
    - Role must be exactly USER, ASSISTANT, or SYSTEM
    - Content should be trimmed of leading/trailing whitespace
    - If role is unrecognized, default to USER

    {{ ctx.output_format }}
  "#
}

// Quick sentiment check on agent response (useful for monitoring)
function AnalyzeResponseTone(response: string) -> ResponseAnalysis {
  client Extractor
  prompt #"
    Briefly analyze the tone and helpfulness of this agent response.

    Response: {{ response }}

    {{ ctx.output_format }}
  "#
}

class ResponseAnalysis {
  tone string @description("Brief description: helpful, confused, apologetic, etc.")
  is_error_message bool @description("Whether this appears to be an error or failure message")
  suggested_improvement string? @description("Optional suggestion for improving the response")
}
