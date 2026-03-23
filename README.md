# AI Prediction System

A full-stack, end-to-end Machine Learning web application featuring a modern UI, a FastAPI backend, Docker containerization, Kubernetes configurations, and comprehensive CI/CD pipelines.

## Features
- **Machine Learning**: Scikit-learn Random Forest model predicting Iris species.
- **Backend API**: FastAPI backend with Pydantic validation, structured logging, and API Key authentication.
- **Frontend UI**: Modern, responsive dashboard with glassmorphism design and real-time Chart.js integration.
- **Deployment**: `Dockerfile`, GitHub Actions CI/CD workflows, and Kubernetes manifests (`deployment.yaml`, `service.yaml`).
- **Monitoring**: Built-in Prometheus `/metrics` endpoint.

## Project Structure
```text
ai_prediction_system/
├── backend/          # FastAPI application (routes, models, auth, logging)
├── frontend/         # HTML/CSS/JS frontend application
├── ml_model/         # ML training scripts and serialized model
├── k8s/              # Kubernetes deployment configurations
├── monitoring/       # Prometheus configurations
├── .github/workflows/# GitHub Actions CI/CD pipeline
├── Dockerfile        # Container build instructions
├── requirements.txt  # Python dependencies
└── postman_collection.json # API testing suite
```

## Running Locally

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Train the Model:**
   ```bash
   python ml_model/train.py
   ```
3. **Start the API Server:**
   Ensure your terminal is at the project root (`ai_prediction_system`):
   ```bash
   # Windows
   set PYTHONPATH=.
   # Linux/Mac
   export PYTHONPATH=.

   python -m uvicorn backend.main:app --reload
   ```
4. **Access the Application:**
   - **Frontend Dashboard**: [http://localhost:8000](http://localhost:8000)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Prometheus Metrics**: [http://localhost:8000/metrics](http://localhost:8000/metrics)

> **Note**: The default API Key for the prediction endpoint is `supersecretapikey123`.

## Docker Deployment

Build and run the container securely:
```bash
docker build -t ai-prediction-api .
docker run -p 8000:8000 ai-prediction-api
```

## Kubernetes Deployment

Deploy the pre-configured manifests:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## AWS EC2 Deployment Guide

1. **Launch an EC2 Instance**: Use Ubuntu Server 22.04 LTS.
2. **Configure Security Groups**: Allow inbound traffic on port 22 (SSH) and port 80 (HTTP).
3. **Install Docker on EC2**:
   ```bash
   sudo apt update
   sudo apt install docker.io
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ubuntu
   ```
4. **Setup GitHub Secrets**: For CI/CD, add `EC2_HOST`, `EC2_USERNAME` (ubuntu), `EC2_PRIVATE_KEY`, `DOCKERHUB_USERNAME`, and `DOCKERHUB_TOKEN` to your repository secrets.
5. **Trigger CI/CD**: Pushing to the `main` branch will automatically build the image, push it to Docker Hub, and deploy it onto your EC2 instance via SSH.
