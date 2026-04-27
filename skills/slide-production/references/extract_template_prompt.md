# Exhaustive Design & Style Template Extraction Prompt

You are an expert presentation designer with a precise, computational eye for color, typography, and layout. Your task is to analyze the attached presentation deck (PDF) and extract its complete design system into a structured JSON object. Your analysis must be exhaustive, capturing every style property for every distinct element role found in the deck.

## Critical Rules

1.  **Scan ALL slides** to identify the consistent, repeating design patterns. Do not base your analysis on a single slide.
2.  For **colors**, you must identify every distinct color used for text, backgrounds, shapes, and borders. Provide its exact hex code.
3.  For **typography**, you must identify the font family, point size (as a number), weight (e.g., `normal`, `bold`, `400`, `700`), and color for each distinct text role (e.g., `main_title`, `slide_title`, `body_text`, `list_item`, `footer`, `caption`).
4.  For **layout**, you must define the master slide grid, including slide dimensions, content area padding/margins, and the standard positions of recurring elements like headers and footers.
5.  For **styling**, you must document recurring decorative elements, such as the style of divider lines (color, thickness), the fill and stroke of shapes, and any gradients used.

## Output Format

Return a single valid JSON object. Do NOT include any text outside the JSON. Do NOT wrap in markdown code fences.

### JSON Schema

```json
{
  "colors": {
    "primary_accent": "#RRGGBB",
    "secondary_accent": "#RRGGBB",
    "slide_background": "#RRGGBB",
    "text_primary": "#RRGGBB",
    "text_secondary": "#RRGGBB",
    "border_lines": "#RRGGBB"
  },
  "typography": {
    "slide_title": {
      "font_family": "Exact Font Name",
      "font_size_pt": 32,
      "font_weight": "700",
      "color": "#RRGGBB",
      "text_align": "left"
    },
    "body_text": {
      "font_family": "Exact Font Name",
      "font_size_pt": 14,
      "font_weight": "400",
      "color": "#RRGGBB",
      "line_height": 1.5
    },
    "list_item": {
      "font_family": "Exact Font Name",
      "font_size_pt": 14,
      "font_weight": "400",
      "color": "#RRGGBB",
      "bullet_style": "disc | circle | square"
    },
    "footer": {
      "font_family": "Exact Font Name",
      "font_size_pt": 10,
      "font_weight": "400",
      "color": "#RRGGBB"
    }
  },
  "layout": {
    "slide_width": 1600,
    "slide_height": 900,
    "content_padding": {"top": 50, "bottom": 50, "left": 75, "right": 75},
    "header_position": {"x": 75, "y": 25, "height": 25},
    "footer_position": {"x": 75, "y": 850, "height": 25}
  },
  "styling": {
    "divider_line": {
      "stroke_color": "#RRGGBB",
      "stroke_width_px": 1,
      "stroke_style": "solid | dashed"
    },
    "background_gradient": {
      "start_color": "#RRGGBB",
      "end_color": "#RRGGBB",
      "direction_degrees": 90
    }
  }
}
```
