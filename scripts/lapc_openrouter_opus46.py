#!/usr/bin/env python3
"""Build a JACDD LAPC artifact using OpenRouter (Claude Opus 4.6 by default).

This script performs:
1) Compression draft from source docs
2) Blind validation loop:
   - QA interview battery (source-aware)
   - Oracle answers (source-aware)
   - Evaluator answers (compressed-only, source-blind)
   - Scorer (compares oracle vs evaluator, source-blind)
3) Targeted restoration rounds if needed
4) Writes final markdown with wc-based ratio in header
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-opus-4.6"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def word_count(text: str) -> int:
    return len(text.split())


def extract_message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "".join(parts)
    return str(content)


def call_openrouter(
    *,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int = 4000,
    temperature: float = 0.2,
    response_format: dict[str, Any] | None = None,
    retries: int = 3,
) -> str:
    body = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if response_format is not None:
        body["response_format"] = response_format
    payload = json.dumps(body).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://local.jacdd",
        "X-Title": "JACDD LAPC Opus 4.6 Runner",
    }

    for attempt in range(1, retries + 1):
        req = urllib.request.Request(OPENROUTER_URL, data=payload, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return extract_message_text(data["choices"][0]["message"]["content"]).strip()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if attempt == retries:
                raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
            time.sleep(attempt * 2)
        except Exception:
            if attempt == retries:
                raise
            time.sleep(attempt * 2)
    raise RuntimeError("Unreachable retry state")


def parse_json_block(raw: str) -> Any:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def call_openrouter_json(
    *,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int = 3000,
    temperature: float = 0.1,
) -> Any:
    raw = call_openrouter(
        api_key=api_key,
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    return parse_json_block(raw)


def ensure_header_and_ratio(doc: str, source_label: str, original_words: int) -> str:
    lines = doc.splitlines()
    compressed_words = max(1, word_count(doc))
    ratio = f"{original_words}/{compressed_words} (wc-w proxy; ~{original_words / compressed_words:.2f}:1)"
    header = f"[LAPC v1 | source: {source_label} | ratio: {ratio}]"
    if lines and lines[0].startswith("[LAPC v1"):
        lines[0] = header
    else:
        lines = [header, ""] + lines
    return "\n".join(lines).rstrip() + "\n"


def ensure_required_sections(doc: str) -> None:
    required = [
        "// Context frame",
        "// Tier 3 payload",
        "// Activation cues",
        "// Behavioral constraints",
    ]
    missing = [m for m in required if m not in doc]
    if missing:
        raise RuntimeError(f"Compressed output missing required sections: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build JACDD LAPC doc via OpenRouter.")
    parser.add_argument(
        "--source-a",
        default="docs/jacdd-reference.md",
        help="Primary source doc path",
    )
    parser.add_argument(
        "--source-b",
        default="docs/raw-braindump-extraction.md",
        help="Secondary source doc path",
    )
    parser.add_argument(
        "--output",
        default="docs/jacdd-claude-opus-4.6.md",
        help="Output markdown file path",
    )
    parser.add_argument(
        "--report",
        default="docs/jacdd-claude-opus-4.6-validation.json",
        help="Validation report output path",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="OpenRouter model id (default: env OPENROUTER_MODEL or anthropic/claude-opus-4.6)",
    )
    parser.add_argument("--max-rounds", type=int, default=2, help="Max restoration rounds")
    args = parser.parse_args()

    repo_root = Path.cwd()
    load_dotenv(repo_root / ".env")

    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. Set it in .env or environment.")

    model = args.model or os.environ.get("OPENROUTER_MODEL", DEFAULT_MODEL)
    source_a = repo_root / args.source_a
    source_b = repo_root / args.source_b
    output_path = repo_root / args.output
    report_path = repo_root / args.report

    src_a = read_text(source_a)
    src_b = read_text(source_b)
    source_label = f"{args.source_a} + {args.source_b}"
    source_text = (
        f"[SOURCE A: {args.source_a}]\n{src_a}\n\n"
        f"[SOURCE B: {args.source_b}]\n{src_b}\n"
    )
    original_words = word_count(src_a) + word_count(src_b)

    compression_system = (
        "You are Claude Opus 4.6 performing LAPC compression. "
        "Output only the final compressed document. No commentary."
    )
    compression_user = f"""
Apply LAPC with balanced compression (dense but disambiguate where behavior could drift).
Source scope: SOURCE A is canonical base; keep any unique Tier-3 payload from SOURCE B.
Exclude operational templates/spec from .claude agents.
Compression target: roughly 250-420 words total after the header.
Required output shape:
1) First line must be LAPC header with ratio placeholder:
[LAPC v1 | source: {source_label} | ratio: TBD]
2) Then these exact section headers in order:
// Context frame
// Tier 3 payload
// Activation cues
// Behavioral constraints
3) Use compact LAPC syntax where useful (! ? -> ; w/ w/o etc).
4) Add ? prefix for ambiguous/high-drift cues.
5) Keep concrete Tier-3 facts and behavior constraints faithful.

Now compress this source:
{source_text}
""".strip()

    compressed = call_openrouter(
        api_key=api_key,
        model=model,
        messages=[
            {"role": "system", "content": compression_system},
            {"role": "user", "content": compression_user},
        ],
        max_tokens=5000,
    )
    compressed = ensure_header_and_ratio(compressed, source_label, original_words)
    ensure_required_sections(compressed)

    qa_system = "Generate a rigorous test battery for compression equivalence."
    qa_user = f"""
Create exactly 10 high-signal questions to verify semantic/behavioral equivalence for JACDD.
Mix coverage + edge-case questions. JSON only:
{{"questions":[{{"id":"q1","question":"..."}}, ...]}}

Source:
{source_text}
""".strip()
    qa_data = call_openrouter_json(
        api_key=api_key,
        model=model,
        messages=[
            {"role": "system", "content": qa_system},
            {"role": "user", "content": qa_user},
        ],
        max_tokens=2500,
        temperature=0.1,
    )
    questions = qa_data.get("questions", [])
    if len(questions) != 10:
        raise RuntimeError(f"Expected 10 questions, got {len(questions)}")

    report: dict[str, Any] = {
        "model": model,
        "source": [args.source_a, args.source_b],
        "output": args.output,
        "rounds": [],
    }

    for round_idx in range(1, args.max_rounds + 1):
        oracle_user = f"""
Answer these questions using ONLY the original source.
Return JSON only: {{"answers":{{"q1":"...", ...}}}}
Keep each answer <= 45 words and factual.

Questions:
{json.dumps(questions, ensure_ascii=False, indent=2)}

Source:
{source_text}
""".strip()
        oracle = call_openrouter_json(
            api_key=api_key,
            model=model,
            messages=[
                {"role": "system", "content": "You are the oracle pass. Use source only."},
                {"role": "user", "content": oracle_user},
            ],
            max_tokens=3000,
            temperature=0.1,
        )

        evaluator_user = f"""
You are the blind evaluator pass.
You MUST answer using only compressed content below. You are forbidden from using any unseen source.
Return JSON only: {{"answers":{{"q1":"...", ...}}}}
Keep each answer <= 45 words. If uncertain, say uncertain.

Questions:
{json.dumps(questions, ensure_ascii=False, indent=2)}

Compressed:
{compressed}
""".strip()
        evaluator = call_openrouter_json(
            api_key=api_key,
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Source-blind evaluation only. If uncertain, state uncertainty; do not invent.",
                },
                {"role": "user", "content": evaluator_user},
            ],
            max_tokens=3000,
            temperature=0.1,
        )

        scorer_user = f"""
Score equivalence by comparing Oracle vs Evaluator answers.
You are source-blind: DO NOT use original source text.
Output JSON only with schema:
{{
  "pass": true|false,
  "score_0_100": int,
  "failures": [{{"id":"qX","severity":"high|medium|low","reason":"...","minimal_fix":"..."}}],
  "summary":"..."
}}
Passing guidance: >=95 and no high-severity failure.

Questions:
{json.dumps(questions, ensure_ascii=False, indent=2)}

Oracle answers:
{json.dumps(oracle, ensure_ascii=False, indent=2)}

Evaluator answers:
{json.dumps(evaluator, ensure_ascii=False, indent=2)}
""".strip()
        score = call_openrouter_json(
            api_key=api_key,
            model=model,
            messages=[
                {"role": "system", "content": "Strict equivalence scorer."},
                {"role": "user", "content": scorer_user},
            ],
            max_tokens=2000,
            temperature=0.1,
        )

        round_data = {
            "round": round_idx,
            "oracle": oracle,
            "evaluator": evaluator,
            "score": score,
        }
        report["rounds"].append(round_data)

        passed = bool(score.get("pass", False))
        if passed:
            break

        failures = score.get("failures", [])
        restoration_user = f"""
Revise the compressed doc with MINIMAL token additions to fix failures.
Keep required section headers and preserve dense LAPC style.
Do not add explanatory prose.
Output only revised compressed document.

Failures:
{json.dumps(failures, ensure_ascii=False, indent=2)}

Current compressed:
{compressed}

Original source for targeted restoration:
{source_text}
""".strip()
        compressed = call_openrouter(
            api_key=api_key,
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Targeted restoration pass. Minimal edits only.",
                },
                {"role": "user", "content": restoration_user},
            ],
            max_tokens=5000,
            temperature=0.2,
        )
        compressed = ensure_header_and_ratio(compressed, source_label, original_words)
        ensure_required_sections(compressed)

    compressed = ensure_header_and_ratio(compressed, source_label, original_words)
    ensure_required_sections(compressed)
    write_text(output_path, compressed)
    write_text(report_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")

    final_score = report["rounds"][-1]["score"] if report["rounds"] else {}
    print(
        json.dumps(
            {
                "output": str(output_path),
                "report": str(report_path),
                "model": model,
                "score": final_score,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
