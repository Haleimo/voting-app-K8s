# GenAI-Augmented DevOps Toolkit

LLM-powered tooling applied to a real multi-service Kubernetes app (`voting-app`,
adapted from kodekloudhub/example-voting-app):

1. **workflow-gen** — turns a plain-English deployment description into a
   validated GitHub Actions workflow YAML.
2. **runbook-gen** — turns the app's Helm `values.yaml` into a human-readable
   `RUNBOOK.md`, regenerated automatically in CI whenever `values.yaml` changes.

## Structure

```
genai-devops-toolkit/
├── workflow-gen/
│   ├── generate.py
│   ├── prompts/system_prompt.md
│   └── examples/example-input.txt
├── runbook-gen/
│   ├── generate.py
│   └── prompts/system_prompt.md
├── .github/workflows/
│   ├── build-and-push.yaml     # builds & pushes vote/worker/result images
│   └── regen-runbook.yaml      # regenerates RUNBOOK.md on values.yaml changes
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt --break-system-packages
export ANTHROPIC_API_KEY=sk-...
```

## Usage

Generate a workflow from a plain-English description:

```bash
cd workflow-gen
python generate.py "build and push vote and result on push to main, deploy to staging, run a smoke test" \
    --out ../../.github/workflows/ci-cd.generated.yaml
```

Regenerate the runbook from the chart's values.yaml:

```bash
cd runbook-gen
python generate.py --values ../../voting-app/values.yaml --out ../../voting-app/RUNBOOK.md
```

## Why two separate tools, one toolkit

Both scripts share the same pattern (system prompt + Claude API call + output
validation), which is the actual "toolkit" — the voting-app is the demo subject,
not a hardcoded dependency. Point `runbook-gen` at any Helm chart's `values.yaml`
and it works the same way.

## Repo layout (this repo + the app repo)

```
Haleimo/
├── voting-app/                 # Helm chart (separate repo or submodule)
└── genai-devops-toolkit/       # this repo
```

Keeping them separate is intentional: it reads as a reusable tool applied to a
project, not app-specific glue code baked into the app repo.
