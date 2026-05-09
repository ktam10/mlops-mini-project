# 🎙️ Whisper AI Translation API on AWS EKS

A production-style MLOps + DevOps project that performs:

- 🎤 Speech-to-Text using OpenAI Whisper
- 🌍 English → Spanish Translation
- ☁️ Containerized deployment using Docker
- 🚀 Kubernetes orchestration on AWS EKS
- 🔄 CI/CD using GitHub Actions
- 📈 Monitoring using Prometheus + Grafana

---

# 🏗️ Architecture Diagram

```text
                        ┌──────────────────────┐
                        │      GitHub Repo     │
                        │  FastAPI + Docker    │
                        └──────────┬───────────┘
                                   │
                                   │ git push
                                   ▼
                    ┌────────────────────────────┐
                    │     GitHub Actions CI/CD   │
                    │                            │
                    │ 1. Build Docker Image      │
                    │ 2. Push to AWS ECR         │
                    │ 3. Deploy to AWS EKS       │
                    └──────────┬─────────────────┘
                               │
                               ▼
                 ┌─────────────────────────┐
                 │     Amazon ECR          │
                 │  Docker Image Registry  │
                 └──────────┬──────────────┘
                            │
                            ▼
                ┌──────────────────────────┐
                │       AWS EKS Cluster    │
                │                          │
                │  ┌────────────────────┐  │
                │  │  Whisper API Pod   │  │
                │  │                    │  │
                │  │ FastAPI            │  │
                │  │ Whisper Model      │  │
                │  │ Translation Layer  │  │
                │  └─────────┬──────────┘  │
                └────────────┼─────────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │  Kubernetes Service    │
                 │    AWS LoadBalancer    │
                 └──────────┬─────────────┘
                            │
                            ▼
                      Public Endpoint


                 ┌────────────────────────┐
                 │     Prometheus         │
                 │  Metrics Scraping      │
                 └──────────┬─────────────┘
                            │
                            ▼
                 ┌────────────────────────┐
                 │       Grafana          │
                 │   Visualization UI     │
                 └────────────────────────┘
```

---

# 🚀 Features

## ✅ AI Features

- Speech-to-text transcription using Whisper
- English to Spanish translation
- Audio file upload support
- Automatic temporary file cleanup
- Model preloading at startup for performance

---

## ✅ DevOps / MLOps Features

- Dockerized FastAPI application
- AWS ECR image storage
- AWS EKS Kubernetes deployment
- GitHub Actions CI/CD pipeline
- Rolling Kubernetes deployments
- Prometheus metrics instrumentation
- Grafana dashboards
- Kubernetes ServiceMonitor integration

---

# 🧠 Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI |
| AI Model | OpenAI Whisper |
| Translation | deep_translator |
| Containerization | Docker |
| Cloud | AWS |
| Kubernetes | Amazon EKS |
| Image Registry | Amazon ECR |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus |
| Visualization | Grafana |

---

# 📂 Project Structure

```text
.
├── main.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
├── service.yaml
├── servicemonitor.yaml
├── .github/
│   └── workflows/
│       └── deploy.yml
└── README.md
```

---

# ⚙️ FastAPI Application

## API Endpoint

### POST `/transcribe`

Accepts an audio file and returns:

- English transcription
- Spanish translation

---

## Example Response

```json
{
  "filename": "sample.mp3",
  "english_text": "Hello everyone",
  "spanish_text": "Hola a todos"
}
```

---

# 🛠️ Local Development Setup

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Required Python Packages

```txt
fastapi
uvicorn
openai-whisper
python-multipart
deep-translator
prometheus-fastapi-instrumentator
```

---

# 🎵 Install FFmpeg

Whisper requires FFmpeg.

## Windows

1. Download FFmpeg
2. Extract ZIP
3. Add `ffmpeg/bin` to Windows PATH
4. Restart terminal

Verify:

```bash
ffmpeg -version
```

---

# ▶️ Run Application Locally

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 📈 Prometheus Metrics Endpoint

Metrics endpoint:

```text
http://127.0.0.1:8000/metrics
```

---

# 🐳 Docker Setup

## Dockerfile

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

# 🐳 Build Docker Image

```bash
docker build -t whisper-api .
```

---

# ▶️ Run Docker Container

```bash
docker run -p 8000:8000 whisper-api
```

---

# ☁️ AWS ECR Setup

## Create ECR Repository

```bash
aws ecr create-repository --repository-name whisper-api
```

---

## Login to ECR

```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-2.amazonaws.com
```

---

## Tag Docker Image

```bash
docker tag whisper-api:latest <account-id>.dkr.ecr.us-east-2.amazonaws.com/whisper-api:latest
```

---

## Push Docker Image

```bash
docker push <account-id>.dkr.ecr.us-east-2.amazonaws.com/whisper-api:latest
```

---

# ☸️ AWS EKS Setup

## Install Tools

### Install kubectl

Verify:

```bash
kubectl version --client
```

---

### Install eksctl

Verify:

```bash
eksctl version
```

---

### Install Helm

Verify:

```bash
helm version
```

---

# 🚀 Create EKS Cluster

```bash
eksctl create cluster \
--name whisper-cluster \
--region us-east-2 \
--nodegroup-name whisper-nodes \
--node-type t3.medium \
--nodes 2
```

---

# 🔍 Verify Cluster

```bash
kubectl get nodes
```

---

# 📄 Kubernetes Deployment

## deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: whisper-api

spec:
  replicas: 1

  selector:
    matchLabels:
      app: whisper-api

  template:
    metadata:
      labels:
        app: whisper-api

    spec:
      containers:
        - name: whisper-api
          image: <ecr-image-url>
          imagePullPolicy: Always

          ports:
            - containerPort: 8000
```

---

# 🌐 Kubernetes Service

## service.yaml

```yaml
apiVersion: v1
kind: Service

metadata:
  name: whisper-service
  namespace: default

  labels:
    app: whisper-api

spec:
  selector:
    app: whisper-api

  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 8000

  type: LoadBalancer
```

---

# 🚀 Deploy Application

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

---

# 🔍 Verify Deployment

```bash
kubectl get deployments
kubectl get pods
kubectl get svc
```

---

# 🌍 Access API

After LoadBalancer creation:

```text
http://<load-balancer-url>/docs
```

---

# 🔄 GitHub Actions CI/CD

## GitHub Secrets

Add:

| Secret | Description |
|---|---|
| AWS_ACCESS_KEY_ID | IAM Access Key |
| AWS_SECRET_ACCESS_KEY | IAM Secret Key |
| AWS_REGION | AWS Region |
| ECR_REPOSITORY | ECR Repository Name |
| EKS_CLUSTER_NAME | EKS Cluster Name |

---

# 📄 GitHub Actions Workflow

## `.github/workflows/deploy.yml`

```yaml
name: Deploy

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and Push Docker Image
        run: |
          docker build -t whisper-api .
          docker tag whisper-api:latest <ecr-url>/whisper-api:latest
          docker push <ecr-url>/whisper-api:latest

      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --region us-east-2 --name whisper-cluster

      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f deployment.yaml
          kubectl apply -f service.yaml
          kubectl rollout restart deployment whisper-api
```

---

# 🔐 EKS Authentication Troubleshooting

## Common Error

```text
You must be logged in to the server
```

---

## Fix

Add IAM user to EKS Access Entries:

AWS Console → EKS → Cluster → Access → Create Access Entry

Grant:

```text
AmazonEKSClusterAdminPolicy
```

---

# 📈 Monitoring Stack

## Install kube-prometheus-stack

### Add Helm Repo

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

---

## Create Monitoring Namespace

```bash
kubectl create namespace monitoring
```

---

## Install Monitoring Stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
--namespace monitoring
```

---

# 📊 FastAPI Metrics Instrumentation

## Add Dependency

```txt
prometheus-fastapi-instrumentator
```

---

## Add Instrumentation

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

# 📄 ServiceMonitor

## servicemonitor.yaml

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor

metadata:
  name: whisper-api-monitor
  namespace: monitoring

  labels:
    release: monitoring

spec:
  selector:
    matchLabels:
      app: whisper-api

  namespaceSelector:
    matchNames:
      - default

  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

---

# 🚀 Apply ServiceMonitor

```bash
kubectl apply -f servicemonitor.yaml
```

---

# 🔍 Access Prometheus

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090 -n monitoring
```

Open:

```text
http://localhost:9090
```

---

# 📊 Access Grafana

```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```

Open:

```text
http://localhost:3000
```

---

# 🔑 Grafana Credentials

## Username

```text
admin
```

## Password

```bash
kubectl get secret monitoring-grafana -n monitoring -o jsonpath="{.data.admin-password}" | base64 --decode
```

---

# 📈 Example Prometheus Queries

## Request Rate

```text
rate(http_requests_total[1m])
```

---

## Request Count

```text
http_requests_total
```

---

## Request Latency

```text
rate(http_request_duration_seconds_sum[1m])
/
rate(http_request_duration_seconds_count[1m])
```

---

# 🧪 Testing the API

## Swagger UI

```text
http://<load-balancer-url>/docs
```

Upload audio file and execute request.

---

# 🎨 Swagger UI Customization

Custom dark Swagger UI theme used:

```python
swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-themes@3.0.1/themes/3.x/theme-dark.css"
```

---

# ⚠️ Common Issues & Fixes

---

## ❌ FFmpeg Not Found

### Error

```text
[WinError 2] The system cannot find the file specified
```

### Fix

Install FFmpeg and add it to PATH.

---

## ❌ kubectl Exec Format Error

### Error

```text
kubectl: cannot execute binary file
```

### Fix

Wrong kubectl binary architecture.

Download correct Windows AMD64 version.

---

## ❌ Kubernetes Deployment Not Found

### Error

```text
deployment not found
```

### Fix

Check actual deployment name:

```bash
kubectl get deployments
```

---

## ❌ Prometheus Returns No Data

### Root Cause

Service labels or port name mismatch.

### Fix

Ensure:

```yaml
labels:
  app: whisper-api
```

AND:

```yaml
ports:
  - name: http
```

exist in service.yaml.

---

## ❌ GitHub Actions EKS Permission Error

### Error

```text
User cannot get resource deployments
```

### Fix

Add GitHub IAM user to:

```text
AmazonEKSClusterAdminPolicy
```

through EKS Access Entries.

---

# 📌 Future Improvements

- Horizontal Pod Autoscaling
- Loki Log Aggregation
- JWT Authentication
- HTTPS + Ingress
- ArgoCD GitOps
- Multi-language Translation
- GPU-based Whisper Inference
- React Frontend

---

# 🎯 Learning Outcomes

This project demonstrates:

✅ AI model deployment

✅ Kubernetes orchestration

✅ Docker containerization

✅ AWS cloud infrastructure

✅ CI/CD automation

✅ Monitoring & observability

✅ Prometheus metrics scraping

✅ Grafana dashboarding

✅ Infrastructure troubleshooting

---

# 🙌 Acknowledgements

- OpenAI Whisper
- FastAPI
- Kubernetes
- AWS
- Prometheus Community
- Grafana

---

# ⭐ Final Result

A fully production-style AI inference platform deployed on Kubernetes with:

- automated CI/CD
- observability
- monitoring
- scalable infrastructure
- cloud-native deployment

built end-to-end from scratch.
