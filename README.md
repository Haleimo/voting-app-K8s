# 🗳️ Lightweight Voting Application & DevOps Toolkit

A fast, lightweight, and modern Voting Web Application built with **Python (Flask)**, **SQLite**, and **HTML5/CSS3**, accompanied by an optimized **Kubernetes Helm Chart** (`voting-app`) and **GenAI DevOps Tooling** (`genai-devops-toolkit`).

---

## ⚡ Quickstart — Running Locally

### Option 1: Direct Python (Fastest)

Run the included shell script:

```bash
chmod +x run.sh
./run.sh
```

Or execute directly:

```bash
pip install -r requirements.txt
python3 app/app.py
```

The application will start on **`http://localhost:5000`**.

---

### Option 2: Docker / Docker Compose

Build and run using Docker Compose:

```bash
docker compose up --build
```

Access the app at `http://localhost:5000`.

---

### Option 3: Kubernetes (Helm Chart)

Deploy to a local Kubernetes cluster (Minikube / k3s / Kind):

```bash
helm install voting-app ./voting-app -f voting-app/values-dev.yaml
```

---

## 📂 Project Structure

```
.
├── app/                        # Lightweight Voting Web Application
│   ├── app.py                  # Flask backend & SQLite API endpoints
│   └── templates/
│       └── index.html          # Modern dark-mode UI with live charts
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt            # Minimal Python dependencies
├── run.sh                      # Quick launcher script
├── voting-app/                 # Streamlined Helm Chart
│   ├── Chart.yaml
│   ├── values.yaml             # Optimized low-resource defaults
│   ├── values-dev.yaml         # Local dev overrides
│   ├── values-prod.yaml        # Production deployment settings
│   └── templates/              # K8s Deployment, Service, Secret manifests
├── genai-devops-toolkit/       # LLM DevOps Tooling
│   ├── runbook-gen/            # Helm values to RUNBOOK.md generator
│   └── workflow-gen/           # Prompt to GitHub Actions YAML generator
├── .gitignore                  # Git exclusions (pycache, db, temp files)
└── README.md                   # Project documentation
```
