// Example: Sentiment Classification Pattern

enum Sentiment {
  Positive @description("Positive sentiment")
  Negative @description("Negative sentiment")
  Neutral @description("Neutral sentiment")
}

class SentimentResult {
  sentiment Sentiment
  confidence float @description("Confidence score 0-1")
  reasoning string @description("Explanation for classification")
}

client FastModel {
  provider "openai"
  options {
    model "gpt-4o-mini"
    temperature 0.1
  }
}

function ClassifySentiment(text: string) -> SentimentResult {
  client FastModel

  prompt #"
    Classify the sentiment of the following text:

    {{ text }}

    Provide confidence score and reasoning.

    {{ ctx.output_format }}
  "#
}
