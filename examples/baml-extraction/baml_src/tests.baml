// BAML Tests for Memory Extraction Functions
// Run with: baml-cli test

// Test extracting a simple conversation from memory events
test ExtractSimpleConversation {
  functions [ExtractConversation]
  args {
    raw_events #"
      [
        {
          "event_id": "evt-001",
          "payload": [
            {
              "conversational": {
                "role": "USER",
                "content": {"text": "What is the weather in Seattle?"}
              }
            }
          ]
        },
        {
          "event_id": "evt-002",
          "payload": [
            {
              "conversational": {
                "role": "ASSISTANT",
                "content": {"text": "I searched for weather information. Seattle is currently 55F and cloudy."}
              }
            }
          ]
        }
      ]
    "#
  }
  @@assert({{ this.messages | length == 2 }})
  @@assert({{ this.messages[0].role == "USER" }})
  @@assert({{ this.messages[1].role == "ASSISTANT" }})
  @@assert({{ this.turn_count >= 1 }})
}

// Test with multiple turns
test ExtractMultiTurnConversation {
  functions [ExtractConversation]
  args {
    raw_events #"
      [
        {"event_id": "1", "payload": [{"conversational": {"role": "USER", "content": {"text": "Hello"}}}]},
        {"event_id": "2", "payload": [{"conversational": {"role": "ASSISTANT", "content": {"text": "Hi there! How can I help?"}}}]},
        {"event_id": "3", "payload": [{"conversational": {"role": "USER", "content": {"text": "Search for Python tutorials"}}}]},
        {"event_id": "4", "payload": [{"conversational": {"role": "ASSISTANT", "content": {"text": "I found several Python tutorials on the web."}}}]}
      ]
    "#
  }
  @@assert({{ this.messages | length == 4 }})
  @@assert({{ this.turn_count >= 2 }})
}

// Test extracting agent response with tool usage
test ExtractResponseWithTools {
  functions [ExtractAgentResponse]
  args {
    raw_response "Based on my search using DuckDuckGo, I found that Python 3.12 was released in October 2023. The search returned several results from python.org and various programming blogs."
    tool_names "DuckDuckGo, Calculator"
  }
  @@assert({{ "DuckDuckGo" in this.tools_used }})
  @@assert({{ this.requires_followup == false }})
}

// Test response without tools
test ExtractSimpleResponse {
  functions [ExtractAgentResponse]
  args {
    raw_response "I'm not sure about that. Could you provide more context about what you're looking for?"
    tool_names "DuckDuckGo, Calculator"
  }
  @@assert({{ not this.tools_used or this.tools_used | length == 0 }})
  @@assert({{ this.requires_followup == true }})
}

// Test message validation and normalization
test ValidateLowercaseRole {
  functions [ValidateMessage]
  args {
    role "user"
    content "  Hello world  "
  }
  @@assert({{ this.role == "USER" }})
}

// Test response tone analysis
test AnalyzeHelpfulResponse {
  functions [AnalyzeResponseTone]
  args {
    response "I found the information you were looking for! Here are the top 5 results with detailed explanations."
  }
  @@assert({{ this.is_error_message == false }})
}

test AnalyzeErrorResponse {
  functions [AnalyzeResponseTone]
  args {
    response "I encountered an error while processing your request. The service is temporarily unavailable."
  }
  @@assert({{ this.is_error_message == true }})
}

// Test edge case: empty events
test ExtractEmptyConversation {
  functions [ExtractConversation]
  args {
    raw_events "[]"
  }
  @@assert({{ this.messages | length == 0 }})
  @@assert({{ this.turn_count == 0 }})
}
