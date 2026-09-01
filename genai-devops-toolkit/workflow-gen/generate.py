#!/usr/bin/env python3
"""
workflow-gen: turn a plain-English CI/CD description into a GitHub Actions
workflow YAML file for the voting-app project.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python generate.py "build and push vote and result on push to main, then deploy to staging and run a smoke test" \
        --out .github/workflows/ci-cd.yaml

Requires: pip install anthropic
"""
import argparse
import pathlib
import subprocess
import sys
import tempfile

try:
    import anthropic
except ImportError:
    sys.exit("Missing dependency. Run: pip install anthropic --break-system-packages")

MODEL = "claude-sonnet-4-6"
HERE = pathlib.Path(__file__).parent
SYSTEM_PROMPT = (HERE / "prompts" / "system_prompt.md").read_text()


def generate_workflow(description: str) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": description}],
    )
    text = "".join(block.text for block in resp.content if block.type == "text")
    # Strip accidental markdown fences if the model adds them anyway.
    text = text.strip()
    if text.startswith("```"):
        text = "\n".join(text.split("\n")[1:-1])
    return text


def validate_with_actionlint(yaml_text: str) -> tuple[bool, str]:
    """Returns (is_valid, error_output). Requires actionlint on PATH; skips if absent."""
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as f:
            f.write(yaml_text)
            tmp_path = f.name
        result = subprocess.run(
            ["actionlint", tmp_path], capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except FileNotFoundError:
        # actionlint not installed locally -- don't block, just warn.
        return True, "(actionlint not found on PATH; skipped validation)"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description", help="Plain-English description of the workflow")
    parser.add_argument("--out", default="workflow.generated.yaml", help="Output file path")
    parser.add_argument("--max-retries", type=int, default=2)
    args = parser.parse_args()

    description = args.description
    yaml_text = ""
    for attempt in range(args.max_retries + 1):
        yaml_text = generate_workflow(description)
        ok, msg = validate_with_actionlint(yaml_text)
        if ok:
            break
        print(f"[attempt {attempt + 1}] actionlint found issues:\n{msg}", file=sys.stderr)
        description += f"\n\nThe previous attempt failed actionlint with this output, fix it:\n{msg}"

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml_text)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
