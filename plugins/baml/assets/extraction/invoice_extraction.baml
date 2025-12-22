// Example: Invoice Extraction Pattern
// This template extracts structured invoice data from images

class LineItem {
  description string @description("Item description")
  quantity int @description("Number of units")
  unit_price float @description("Price per unit")
  total float @description("Line item total")
}

class Invoice {
  invoice_number string @description("Invoice ID")
  date string @description("Invoice date (YYYY-MM-DD)")
  vendor_name string
  items LineItem[] @description("List of line items")
  subtotal float
  tax float
  total float @description("Grand total")
}

client VisionModel {
  provider "openai"
  options {
    model "gpt-4o"
    temperature 0.0
  }
}

function ExtractInvoice(invoice_image: image) -> Invoice {
  client VisionModel

  prompt #"
    Extract all information from this invoice image.

    {{ invoice_image }}

    IMPORTANT:
    - Validate that subtotal + tax = total
    - Extract all line items accurately
    - Use YYYY-MM-DD format for dates

    {{ ctx.output_format }}
  "#
}
