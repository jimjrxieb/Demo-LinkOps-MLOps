#!/usr/bin/env python3
"""
Test script for Audit Assess System.
Tests repository scanning, security analysis, and GitOps compliance.
"""

import asyncio
import os
import tempfile

from logic.analyzer import RepoAnalyzer
from logic.gitops_scanner import GitOpsScanner
from logic.security_scanner import SecurityScanner


async def test_audit_system():
    """Test the complete audit system functionality."""
    print("🧪 Testing Audit Assess System...")

    # Create a test repository structure
    with tempfile.TemporaryDirectory() as temp_dir:
        test_repo_path = os.path.join(temp_dir, "test-repo")
        os.makedirs(test_repo_path)

        # Create test files
        create_test_repository(test_repo_path)

        print(f"\n📁 Created test repository at: {test_repo_path}")

        # Test 1: Security Scanner
        print("\n1. Testing Security Scanner...")
        security_scanner = SecurityScanner(test_repo_path)
        security_results = await security_scanner.run_full_security_scan()

        print(f"   Secrets found: {security_results['summary']['secrets_found']}")
        print(
            f"   Vulnerabilities found: {security_results['summary']['vulnerabilities_found']}"
        )
        print(f"   Total issues: {security_results['summary']['total_issues']}")
        print(f"   Compliance score: {security_results['summary']['compliance_score']}")

        # Test 2: GitOps Scanner
        print("\n2. Testing GitOps Scanner...")
        gitops_scanner = GitOpsScanner(test_repo_path)
        gitops_results = await gitops_scanner.scan_gitops_compliance()

        print(
            f"   Overall score: {gitops_results['overall_score']}/{gitops_results['max_score']}"
        )
        print(f"   Grade: {gitops_results['grade']}")
        print(f"   Categories: {len(gitops_results['categories'])}")

        # Test 3: Full Repository Analysis
        print("\n3. Testing Full Repository Analysis...")
        analyzer = RepoAnalyzer()
        analyzer.repo_path = test_repo_path  # Use our test repo instead of cloning

        analysis = {
            "repo_name": "test-repo",
            "languages": analyzer._detect_languages(),
            "structure": analyzer._analyze_structure(),
            "ci_configs": analyzer._detect_ci_configs(),
            "helm_charts": analyzer._detect_helm_charts(),
            "dockerfiles": analyzer._detect_dockerfiles(),
            "gitops_tools": analyzer._detect_gitops_tools(),
            "architecture_patterns": analyzer._detect_architecture_patterns(),
            "security_issues": analyzer._detect_security_issues(),
            "recommendations": analyzer._generate_recommendations(),
            "security_scan": security_results,
            "gitops_compliance": gitops_results,
        }

        print(f"   Languages detected: {analysis['languages']}")
        print(f"   Total files: {analysis['structure']['total_files']}")
        print(f"   CI configs: {len(analysis['ci_configs'])}")
        print(f"   Dockerfiles: {len(analysis['dockerfiles'])}")
        print(f"   Helm charts: {len(analysis['helm_charts'])}")

        # Test 4: API Endpoint Simulation
        print("\n4. Testing API Endpoint Simulation...")
        audit_response = {
            "message": "Audit complete",
            "repo_url": "https://github.com/test/test-repo",
            "report": analysis,
            "summary": {
                "security_score": analysis.get("security_scan", {})
                .get("summary", {})
                .get("compliance_score", 0),
                "gitops_score": analysis.get("gitops_compliance", {}).get(
                    "overall_score", 0
                ),
                "total_issues": analysis.get("security_scan", {})
                .get("summary", {})
                .get("total_issues", 0),
                "grade": analysis.get("gitops_compliance", {}).get("grade", "F"),
            },
        }

        print(f"   Security Score: {audit_response['summary']['security_score']}")
        print(f"   GitOps Score: {audit_response['summary']['gitops_score']}")
        print(f"   Total Issues: {audit_response['summary']['total_issues']}")
        print(f"   Grade: {audit_response['summary']['grade']}")

        # Test 5: Generate Recommendations
        print("\n5. Testing Recommendations...")
        recommendations = analysis.get("gitops_compliance", {}).get(
            "recommendations", []
        )
        print(f"   Generated {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):  # Show first 3
            print(f"     {i}. {rec['title']} ({rec['priority']} priority)")

        print("\n✅ Audit system tests completed successfully!")


def create_test_repository(repo_path: str):
    """Create a test repository with various files for testing."""

    # Create Dockerfile
    dockerfile_content = """FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
"""
    with open(os.path.join(repo_path, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # Create docker-compose.yml
    compose_content = """version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
"""
    with open(os.path.join(repo_path, "docker-compose.yml"), "w") as f:
        f.write(compose_content)

    # Create Kubernetes manifests
    k8s_dir = os.path.join(repo_path, "k8s")
    os.makedirs(k8s_dir)

    deployment_content = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: test-app
  template:
    metadata:
      labels:
        app: test-app
    spec:
      containers:
      - name: app
        image: test-app:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
"""
    with open(os.path.join(k8s_dir, "deployment.yaml"), "w") as f:
        f.write(deployment_content)

    # Create Helm chart
    helm_dir = os.path.join(repo_path, "helm")
    os.makedirs(helm_dir)

    chart_yaml = """apiVersion: v2
name: test-app
description: Test application
version: 0.1.0
appVersion: "1.0.0"
"""
    with open(os.path.join(helm_dir, "Chart.yaml"), "w") as f:
        f.write(chart_yaml)

    # Create GitHub Actions workflow
    workflows_dir = os.path.join(repo_path, ".github", "workflows")
    os.makedirs(workflows_dir)

    workflow_content = """name: CI/CD Pipeline
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Run tests
      run: |
        echo "Running tests..."
"""
    with open(os.path.join(workflows_dir, "ci.yml"), "w") as f:
        f.write(workflow_content)

    # Create Python app
    app_content = """import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
"""
    with open(os.path.join(repo_path, "app.py"), "w") as f:
        f.write(app_content)

    # Create requirements.txt
    requirements_content = """flask==2.0.1
requests==2.25.1
"""
    with open(os.path.join(repo_path, "requirements.txt"), "w") as f:
        f.write(requirements_content)

    # Create README.md
    readme_content = """# Test Application

This is a test application for auditing.

## Usage

```bash
docker-compose up
```

## Deployment

```bash
helm install test-app ./helm
```
"""
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write(readme_content)

    # Create a file with a "secret" (for testing)
    config_content = """# Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/db
"""
    with open(os.path.join(repo_path, "config.env"), "w") as f:
        f.write(config_content)


def test_api_endpoints():
    """Test the API endpoints."""
    print("\n🌐 Testing API endpoints...")

    import requests

    base_url = "http://localhost:8003"  # audit_assess service port

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health endpoint error: {str(e)}")

    # Test scan endpoint
    try:
        scan_data = {"repo_url": "https://github.com/test/test-repo", "branch": "main"}
        response = requests.post(f"{base_url}/scan/repo/", json=scan_data, timeout=30)
        if response.status_code == 200:
            print("   ✅ Scan endpoint working")
            result = response.json()
            print(f"   📊 Scan result: {result.get('repo_name', 'Unknown')}")
        else:
            print(f"   ❌ Scan endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Scan endpoint error: {str(e)}")

    # Test audit endpoint
    try:
        audit_data = {"repo_url": "https://github.com/test/test-repo"}
        response = requests.post(f"{base_url}/scan/audit", json=audit_data, timeout=60)
        if response.status_code == 200:
            print("   ✅ Audit endpoint working")
            result = response.json()
            print(f"   📊 Audit summary: {result.get('summary', {})}")
        else:
            print(f"   ❌ Audit endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Audit endpoint error: {str(e)}")


if __name__ == "__main__":
    print("🚀 Starting Audit Assess Tests...")

    # Run async tests
    asyncio.run(test_audit_system())

    # Run API tests
    test_api_endpoints()

    print("\n🎉 All tests completed!")
