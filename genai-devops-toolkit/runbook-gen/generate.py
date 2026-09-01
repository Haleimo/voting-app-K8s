#!/usr/bin/env python3
"""
runbook-gen: turn a Helm chart's values.yaml into a human-readable RUNBOOK.md.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python generate.py --values ../../voting-app/values.yaml --out ../../voting-app/RUNBOOK.md

Requires: pip install anthropic
"""
import argparse
import pathlib
import sys

try:
    import anthropic
except ImportError:
    sys.exit("Missing dependency. Run: pip install anthropic --break-system-packages")

MODEL = "claude-sonnet-4-6"
HERE = pathlib.Path(__file__).parent
SYSTEM_PROMPT = (HERE / "prompts" / "system_prompt.md").read_text()


def generate_runbook(values_yaml: str) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": values_yaml}],
    )
    return "".join(block.text for block in resp.content if block.type == "text").strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--values", required=True, help="Path to values.yaml")
    parser.add_argument("--out", default="RUNBOOK.md", help="Output markdown path")
    args = parser.parse_args()

    values_path = pathlib.Path(args.values)
    if not values_path.exists():
        sys.exit(f"values file not found: {values_path}")

    runbook = generate_runbook(values_path.read_text())

    out_path = pathlib.Path(args.out)
    out_path.write_text(runbook)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
