#!/usr/bin/env python3
"""
brandinsights/scripts/dedupe_aggregator.py

Splits the raw research.md into 3 logical chunks for ChatGPT 5.4 Thinking
deduplication passes, and merges the de-duped outputs into insights.md.

Usage:
  python3 dedupe_aggregator.py split --input research.md --output-dir chunks/
  python3 dedupe_aggregator.py merge --input-dir chunks/ --output insights.md

The split command divides research.md into 3 files:
  chunk_1_consumer_insights.md
  chunk_2_competitive_benchmarks.md
  chunk_3_social_trends.md

Each chunk is designed to be pasted into ChatGPT 5.4 Thinking for deduplication.
"""

import argparse
import os
import re
import sys
from pathlib import Path


CHUNK_KEYWORDS = {
    "chunk_1_consumer_insights.md": [
        "consumer", "segment", "audience", "buyer", "shopper", "motivation",
        "purchase", "need", "psychographic", "demographic", "persona",
        "lifestyle", "value", "attitude", "behavior", "habit", "loyalty",
        "retention", "satisfaction", "nps", "csat", "survey", "focus group",
    ],
    "chunk_2_competitive_benchmarks.md": [
        "competitor", "benchmark", "market share", "tam", "sam", "som",
        "revenue", "growth", "cac", "ltv", "cpm", "cpa", "roas", "roi",
        "shelf", "velocity", "distribution", "retail", "pricing", "promotion",
        "brand equity", "awareness", "consideration", "conversion", "funnel",
        "performance", "kpi", "metric", "spend", "budget", "investment",
    ],
    "chunk_3_social_trends.md": [
        "trend", "social", "twitter", "reddit", "instagram", "tiktok",
        "youtube", "linkedin", "influencer", "creator", "viral", "hashtag",
        "sentiment", "community", "forum", "review", "comment", "post",
        "engagement", "reach", "impression", "share", "like", "follow",
        "cultural", "zeitgeist", "moment", "meme", "conversation",
    ],
}

DEDUPE_PROMPT_TEMPLATE = """You are a senior brand strategist performing a rigorous deduplication and synthesis pass.

Below is a chunk of raw research from multiple AI models (Gemini, ChatGPT, Claude) and social media mining. There is significant overlap and redundancy.

Your task:
1. Extract ALL unique, non-overlapping insights from this chunk.
2. Discard any claim that is a near-duplicate of another claim already in the output.
3. Preserve ALL citations in the format [Source Name](URL).
4. Structure the output as clean, hierarchical Markdown with ## section headers.
5. Flag any conflicting data points with a ⚠️ CONFLICT note.
6. Be quantitative wherever possible — preserve all numbers, percentages, and dates.
7. Do NOT summarize away detail. Depth, breadth, and specificity must be preserved.

RAW RESEARCH CHUNK:
---
{chunk_content}
---

Output the de-duplicated insights in clean Markdown format."""


def split_research(input_path: str, output_dir: str) -> None:
    """Split research.md into 3 thematic chunks."""
    text = Path(input_path).read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Initialize chunk buckets
    chunks = {name: [] for name in CHUNK_KEYWORDS}
    unassigned = []

    current_section = []
    current_header = ""

    for line in lines:
        if re.match(r'^#{1,3} ', line):
            # Flush current section to the most relevant chunk
            if current_section:
                _assign_section(current_header, current_section, chunks, unassigned)
            current_header = line.strip()
            current_section = [line]
        else:
            current_section.append(line)

    # Flush last section
    if current_section:
        _assign_section(current_header, current_section, chunks, unassigned)

    # Distribute unassigned content evenly
    chunk_names = list(CHUNK_KEYWORDS.keys())
    for i, section in enumerate(unassigned):
        chunks[chunk_names[i % 3]].extend(section)

    os.makedirs(output_dir, exist_ok=True)
    for chunk_name, content in chunks.items():
        out_path = os.path.join(output_dir, chunk_name)
        chunk_text = "".join(content)
        prompt = DEDUPE_PROMPT_TEMPLATE.format(chunk_content=chunk_text)
        Path(out_path).write_text(prompt, encoding="utf-8")
        word_count = len(chunk_text.split())
        print(f"  Chunk '{chunk_name}': {word_count} words → {out_path}")

    print(f"\n✅ Split complete. Paste each chunk file into ChatGPT 5.4 Thinking for deduplication.")
    print("   After deduplication, save each output as chunk_1_deduped.md, chunk_2_deduped.md, chunk_3_deduped.md")
    print("   Then run: python3 dedupe_aggregator.py merge --input-dir chunks/ --output insights.md")


def _assign_section(header: str, section: list, chunks: dict, unassigned: list) -> None:
    """Assign a section to the most relevant chunk based on keyword matching."""
    header_lower = header.lower()
    section_text = "".join(section).lower()
    scores = {}
    for chunk_name, keywords in CHUNK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in header_lower) * 3
        score += sum(1 for kw in keywords if kw in section_text)
        scores[chunk_name] = score

    best_chunk = max(scores, key=scores.get)
    if scores[best_chunk] > 0:
        chunks[best_chunk].extend(section)
    else:
        unassigned.append(section)


def merge_chunks(input_dir: str, output_path: str) -> None:
    """Merge the 3 de-duped chunk outputs into insights.md."""
    deduped_files = sorted(Path(input_dir).glob("*_deduped.md"))
    if not deduped_files:
        print(f"ERROR: No *_deduped.md files found in {input_dir}")
        print("Expected: chunk_1_deduped.md, chunk_2_deduped.md, chunk_3_deduped.md")
        sys.exit(1)

    merged = ["# Brand Insights — Synthesized & De-Duplicated\n\n"]
    merged.append(f"> Generated by brandinsights skill. Sources: {len(deduped_files)} de-duped chunks.\n\n")

    section_headers = [
        "## Consumer Insights & Segments",
        "## Competitive Benchmarks & Market Performance",
        "## Social Trends & Cultural Context",
    ]

    for i, deduped_file in enumerate(deduped_files):
        content = deduped_file.read_text(encoding="utf-8")
        header = section_headers[i] if i < len(section_headers) else f"## Section {i+1}"
        merged.append(f"{header}\n\n")
        merged.append(content.strip())
        merged.append("\n\n---\n\n")

    Path(output_path).write_text("".join(merged), encoding="utf-8")
    word_count = len("".join(merged).split())
    print(f"✅ insights.md written to {output_path} ({word_count} words)")


def main() -> None:
    parser = argparse.ArgumentParser(description="De-duplicate and aggregate research data")
    subparsers = parser.add_subparsers(dest="command")

    split_parser = subparsers.add_parser("split", help="Split research.md into 3 chunks")
    split_parser.add_argument("--input", required=True)
    split_parser.add_argument("--output-dir", required=True)

    merge_parser = subparsers.add_parser("merge", help="Merge de-duped chunks into insights.md")
    merge_parser.add_argument("--input-dir", required=True)
    merge_parser.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.command == "split":
        split_research(args.input, args.output_dir)
    elif args.command == "merge":
        merge_chunks(args.input_dir, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
