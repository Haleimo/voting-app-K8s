# voting-app (Helm chart)

Helm chart for the multi-service example voting app: **vote** (frontend) →
**redis** (queue) → **worker** (consumer) → **postgres** (db) → **result** (frontend).

Forked/adapted from kodekloudhub/example-voting-app and example-voting-app-kubernetes,
converted to Helm and parameterized for multi-environment deploys.

## Install

```bash
# local / minikube
helm install voting-app . -f values-dev.yaml

# cloud (EKS/AKS/GKE)
helm install voting-app . -f values-prod.yaml
```

## Structure

```
voting-app/
├── Chart.yaml
├── values.yaml            # defaults
├── values-dev.yaml        # NodePort, no persistence
├── values-prod.yaml       # LoadBalancer, replicas, persistence, ingress
├── templates/
│   ├── _helpers.tpl
│   ├── NOTES.txt
│   ├── vote-deployment.yaml / vote-service.yaml
│   ├── worker-deployment.yaml      (no service — no inbound listener)
│   ├── result-deployment.yaml / result-service.yaml
│   ├── redis-deployment.yaml / redis-service.yaml
│   ├── db-deployment.yaml / db-service.yaml / db-secret.yaml
│   └── ingress.yaml
└── RUNBOOK.md              # auto-generated — see genai-devops-toolkit/runbook-gen
```

## Notes

- `db-secret.yaml` uses plaintext values from `values.yaml` for demo purposes.
  Replace with Sealed Secrets or External Secrets before using this for anything real.
- `vote.service.type` / `result.service.type` control whether you get a NodePort
  (local) or a LoadBalancer (cloud). See the generated `RUNBOOK.md` for the full
  breakdown of what each value affects.
- Set real image repositories in `values.yaml` before installing — the defaults
  (`yourdockerhubuser/...`) are placeholders.
