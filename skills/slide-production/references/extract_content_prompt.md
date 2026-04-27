# Exhaustive Content & Placement Extraction Prompt

You are an expert document deconstruction engine. Your task is to process the attached presentation deck (PDF) and produce a structured JSON object that documents **every single element on every single slide**. This includes all text boxes, images, shapes, lines, charts, and tables. Your output must be exhaustive and precise, capturing both content and placement.

## Critical Rules

1.  **Process every slide in order**, from first to last.
2.  For each slide, create a JSON object containing a list of all elements on that slide.
3.  For each element, you MUST provide its exact **bounding box** (`x`, `y`, `width`, `height`) in pixels, assuming a 1600x900 slide dimension. The top-left corner is (0, 0).
4.  Extract ALL text **exactly as it appears** — do not paraphrase, summarize, or reword anything. Preserve all original line breaks within a text element.
5.  Identify the role of each text element (e.g., `title`, `body`, `footer`, `caption`).
6.  For images, use the filename from the "Available Images" list below if one matches. If not, use a descriptive placeholder like `image_slideN_position.png`.
7.  For charts and diagrams, describe them in detail, including type, data labels, and any visible trends.
8.  For tables, reproduce their full structure and content within the JSON.

## Output Format

Return a single valid JSON object. Do NOT include any text outside the JSON. Do NOT wrap in markdown code fences. The root of the JSON should be a list of slide objects.

### JSON Schema

```json
[
  {
    "slide_number": 1,
    "elements": [
      {
        "type": "text",
        "role": "title",
        "content": "Company Overview",
        "bounding_box": {"x": 100, "y": 80, "width": 1400, "height": 60}
      },
      {
        "type": "image",
        "filename": "image1.png",
        "alt_text": "Company logo",
        "bounding_box": {"x": 700, "y": 200, "width": 200, "height": 200}
      },
      {
        "type": "text",
        "role": "body",
        "content": "- Founded in 2015\n- 500+ employees globally\n- Offices in 12 countries",
        "bounding_box": {"x": 100, "y": 450, "width": 600, "height": 150}
      },
      {
        "type": "text",
        "role": "footer",
        "content": "Confidential — Page 1",
        "bounding_box": {"x": 1350, "y": 850, "width": 200, "height": 20}
      }
    ]
  }
]
```
