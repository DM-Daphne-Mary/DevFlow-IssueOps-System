# 🚀 DevFlow IssueOps System — Cloud-Native Complaint Management

[![CI/CD Pipeline](https://github.com/DM-Daphne-Mary/DevFlow-IssueOps-System/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/DM-Daphne-Mary/DevFlow-IssueOps-System/actions)

A production-ready, cloud-native complaint management system with end-to-end DevOps automation. This project demonstrates modern DevOps practices including CI/CD pipelines, containerization, container orchestration, and Infrastructure as Code (IaC).

---

## 🏗️ Architecture Overview

| Layer               | Technology                        |
|---------------------|-----------------------------------|
| **Backend**         | Flask (Python 3.11) REST API      |
| **Database**        | PostgreSQL 15 (Alpine)            |
| **Containerization**| Docker + Docker Compose           |
| **CI/CD**           | GitHub Actions                    |
| **Orchestration**   | Kubernetes (Minikube)             |
| **IaC**             | Terraform (Docker Provider)       |
| **Config Mgmt**     | Ansible                          |
| **Production WSGI** | Gunicorn (2 workers)             |

---

## 📁 Project Structure

```
DevFlow-IssueOps-System/
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions CI/CD pipeline
├── app/
│   ├── app.py                      # Flask application (main entry point)
│   ├── requirements.txt            # Python dependencies
│   ├── templates/
│   │   └── index.html              # Web UI template
│   └── tests/
│       └── test_app.py             # Unit tests (pytest)
├── k8s/
│   ├── namespace.yml               # Kubernetes namespace
│   ├── postgres-secret.yml         # Database credentials (base64)
│   ├── postgres-pvc.yml            # Persistent Volume Claim
│   ├── postgres-deployment.yml     # PostgreSQL deployment
│   ├── postgres-service.yml        # PostgreSQL ClusterIP service
│   ├── app-deployment.yml          # Flask app deployment (2 replicas)
│   └── app-service.yml             # Flask app NodePort service
├── terraform/
│   ├── main.tf                     # Docker provider infrastructure
│   ├── variables.tf                # Configurable variables
│   ├── outputs.tf                  # Output values (URLs, IDs)
│   └── .terraform.lock.hcl         # Provider lock file
├── ansible/
│   ├── playbook.yml                # Server setup & app deployment
│   └── inventory.ini               # Host inventory
├── Dockerfile                      # Multi-stage container image
├── docker-compose.yml              # Multi-container orchestration
├── .gitignore                      # Git ignore rules
└── README.md                       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

| Tool              | Version  | Purpose                    |
|-------------------|----------|----------------------------|
| Docker            | 20.10+   | Containerization           |
| Docker Compose    | 2.x      | Multi-container management |
| Python            | 3.11+    | Local development          |
| Minikube          | 1.30+    | Local Kubernetes cluster   |
| kubectl           | 1.27+    | Kubernetes CLI             |
| Terraform         | 1.0+     | Infrastructure as Code     |
| Ansible           | 2.14+    | Configuration management   |

---

### Option 1: Docker Compose (Recommended)

The fastest way to run the full stack locally:

```bash
# Clone the repository
git clone https://github.com/DM-Daphne-Mary/DevFlow-IssueOps-System.git
cd DevFlow-IssueOps-System

# Start all services
docker-compose up --build -d

# Verify the app is running
curl http://localhost:5000/health
```

🌐 Access the app at **http://localhost:5000**

```bash
# Stop the services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

### Option 2: Kubernetes (Minikube)

Deploy the application on a local Kubernetes cluster:

```bash
# Start Minikube
minikube start

# Build the Docker image inside Minikube
eval $(minikube docker-env)
docker build -t complaint-management-system:latest .

# Deploy all Kubernetes resources
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/postgres-secret.yml
kubectl apply -f k8s/postgres-pvc.yml
kubectl apply -f k8s/postgres-deployment.yml
kubectl apply -f k8s/postgres-service.yml
kubectl apply -f k8s/app-deployment.yml
kubectl apply -f k8s/app-service.yml

# Verify pods are running
kubectl get pods -n complaint-app

# Get the application URL
minikube service flask-app-service -n complaint-app --url
```

#### Kubernetes Resources

| Resource             | Type         | Details                          |
|----------------------|--------------|----------------------------------|
| `complaint-app`      | Namespace    | Isolated namespace for the app   |
| `postgres-secret`    | Secret       | DB credentials (base64 encoded)  |
| `postgres-pvc`       | PVC          | 1Gi persistent storage           |
| `postgres`           | Deployment   | PostgreSQL 15 (1 replica)        |
| `postgres-service`   | ClusterIP    | Internal DB access (port 5432)   |
| `flask-app`          | Deployment   | Flask app (2 replicas)           |
| `flask-app-service`  | NodePort     | External access (port 30500)     |

---

### Option 3: Terraform

Provision Docker containers using Terraform's Docker provider:

```bash
cd terraform

# Initialize Terraform
terraform init

# Preview the changes
terraform plan

# Apply the infrastructure
terraform apply -auto-approve
```

🌐 Access the app at **http://localhost:5001**

#### Terraform Variables

| Variable       | Default        | Description                  |
|----------------|----------------|------------------------------|
| `db_name`      | `complaintsdb` | PostgreSQL database name     |
| `db_user`      | `admin`        | PostgreSQL username          |
| `db_password`  | `admin123`     | PostgreSQL password          |
| `db_port`      | `5433`         | External PostgreSQL port     |
| `app_port`     | `5001`         | External Flask app port      |
| `environment`  | `development`  | Deployment environment tag   |

```bash
# Destroy the infrastructure
terraform destroy -auto-approve
```

---

### Option 4: Ansible

Automate server setup and deployment on remote machines:

```bash
# Update the inventory file with your server IP
nano ansible/inventory.ini

# Run the playbook
ansible-playbook -i ansible/inventory.ini ansible/playbook.yml
```

The Ansible playbook will:
1. Install system packages and Docker
2. Copy application files to the server
3. Start the app with Docker Compose
4. Verify health check at `/health`

---

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline triggers on every push or pull request to `main` and `dev` branches.

### Pipeline Stages

```
┌──────────────┐     ┌────────────────────┐     ┌──────────────────────┐
│  Run Tests   │────▶│ Build Docker Image  │────▶│ Deploy to Production │
│  (pytest)    │     │ (docker build)      │     │ (Docker Hub push)    │
└──────────────┘     └────────────────────┘     └──────────────────────┘
     Job 1                  Job 2                  Job 3 (main only)
```

| Stage      | Trigger                  | Description                                      |
|------------|--------------------------|--------------------------------------------------|
| **Test**   | All pushes & PRs         | Install deps, run `pytest` with verbose output   |
| **Build**  | After tests pass         | Build Docker image, tag with commit SHA & latest |
| **Deploy** | Push to `main` only      | Push image to Docker Hub with SHA, latest, & v3 tags |

### Required GitHub Secrets

| Secret             | Description                |
|--------------------|----------------------------|
| `DOCKER_USERNAME`  | Docker Hub username        |
| `DOCKER_PASSWORD`  | Docker Hub password/token  |

---

## 📊 API Reference

### Endpoints

| Method | Endpoint           | Description                    | Response   |
|--------|--------------------|--------------------------------|------------|
| `GET`  | `/`                | Web UI (HTML)                  | `200 HTML` |
| `GET`  | `/health`          | Health check                   | `200 JSON` |
| `GET`  | `/complaints`      | List all complaints            | `200 JSON` |
| `GET`  | `/complaints/open` | List only open complaints      | `200 JSON` |
| `POST` | `/complaints`      | Submit a new complaint         | `201 JSON` |

### Example: Submit a Complaint

```bash
curl -X POST http://localhost:5000/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daphne Mary",
    "email": "daphne@example.com",
    "complaint": "Service downtime on production server",
    "category": "Infrastructure",
    "priority": "High"
  }'
```

**Response:**
```json
{
  "message": "Complaint submitted successfully!"
}
```

### Example: List All Complaints

```bash
curl http://localhost:5000/complaints
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Daphne Mary",
    "email": "daphne@example.com",
    "complaint": "Service downtime on production server",
    "status": "Open",
    "category": "Infrastructure",
    "priority": "High",
    "created_at": "2026-04-11 00:00:00"
  }
]
```

---

## 🐳 Docker Details

### Dockerfile Highlights

- **Base image**: `python:3.11-slim` for minimal footprint
- **Multi-stage**: Optimized layer caching with requirements installed first
- **Health check**: Built-in health check hitting `/health` every 30s
- **Production server**: Uses Gunicorn with 2 workers (not Flask dev server)

### Build & Run Manually

```bash
# Build the image
docker build -t complaint-management-system:latest .

# Run standalone (without database)
docker run -d -p 5000:5000 \
  -e DB_HOST=localhost \
  -e DB_NAME=complaintsdb \
  -e DB_USER=admin \
  -e DB_PASSWORD=admin123 \
  complaint-management-system:latest
```

---

## 🧪 Running Tests

```bash
# Install dependencies
cd app
pip install -r requirements.txt

# Run tests with verbose output
python -m pytest tests/ -v --tb=short
```

---

## 📝 Environment Variables

| Variable      | Default        | Description                  |
|---------------|----------------|------------------------------|
| `DB_HOST`     | `db`           | PostgreSQL hostname          |
| `DB_NAME`     | `complaintsdb` | Database name                |
| `DB_USER`     | `admin`        | Database username            |
| `DB_PASSWORD` | `admin123`     | Database password            |

---

## 🌿 Branch Strategy

| Branch       | Purpose                           |
|--------------|-----------------------------------|
| `main`       | Production-ready code             |
| `dev`        | Development & integration branch  |
| `feature/*`  | Feature branches for new work     |

---

## 👤 Author

**Daphne Mary** — [DM-Daphne-Mary](https://github.com/DM-Daphne-Mary)

DevFlow IssueOps System — Cloud-Native Complaint Management with Full DevOps Automation
