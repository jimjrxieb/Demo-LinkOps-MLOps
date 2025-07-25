#!/bin/bash
"""
Kubernetes Deployment Script for DEMO-LinkOps

This script deploys the complete DEMO-LinkOps platform to Kubernetes
in the correct order to handle dependencies.
"""

set -e

echo "🚀 Deploying DEMO-LinkOps to Kubernetes..."

# Function to wait for deployment to be ready
wait_for_deployment() {
    local deployment=$1
    echo "⏳ Waiting for $deployment to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/$deployment -n demo-linkops
}

# Function to wait for pod to be ready
wait_for_pods() {
    local label=$1
    echo "⏳ Waiting for pods with label $label to be ready..."
    kubectl wait --for=condition=ready --timeout=300s pod -l $label -n demo-linkops
}

echo "📋 Applying Kubernetes manifests in dependency order..."

# 1. Create namespace and configuration
echo "1️⃣ Creating namespace and configuration..."
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml

# 2. Deploy database services first (they have no dependencies)
echo "2️⃣ Deploying database services..."
kubectl apply -f postgres.yaml
kubectl apply -f redis.yaml

# Wait for databases to be ready
wait_for_deployment demo-postgres
wait_for_deployment demo-redis

echo "✅ Database services are ready"

# 3. Deploy backend microservices (they depend on databases)
echo "3️⃣ Deploying backend microservices..."
kubectl apply -f rag-service.yaml
kubectl apply -f rag-deployment.yaml
kubectl apply -f ml-models.yaml
kubectl apply -f pipeline.yaml 
kubectl apply -f sync-engine.yaml

# Wait for backend services to be ready
wait_for_deployment demo-rag
wait_for_deployment demo-ml-models
wait_for_deployment demo-pipeline
wait_for_deployment demo-sync-engine

echo "✅ Backend microservices are ready"

# 4. Deploy unified API (depends on backend services)
echo "4️⃣ Deploying unified API..."
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml

wait_for_deployment demo-unified-api

echo "✅ Unified API is ready"

# 5. Deploy frontend (depends on unified API)
echo "5️⃣ Deploying frontend..."
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

wait_for_deployment demo-frontend

echo "✅ Frontend is ready"

# 6. Deploy ingress (depends on all services)
echo "6️⃣ Deploying ingress..."
kubectl apply -f ingress.yaml

echo "🎉 DEMO-LinkOps deployment completed successfully!"

# Display deployment status
echo ""
echo "📊 Deployment Status:"
echo "===================="
kubectl get pods -n demo-linkops -o wide

echo ""
echo "🌐 Services:"
echo "============"
kubectl get svc -n demo-linkops

echo ""
echo "🚪 Ingress:"
echo "==========="
kubectl get ingress -n demo-linkops

echo ""
echo "💾 Persistent Volumes:"
echo "======================"
kubectl get pvc -n demo-linkops

echo ""
echo "🔗 Access URLs:"
echo "==============="
echo "Frontend:    http://demo.local"
echo "API:         http://demo.local/api"
echo "RAG:         http://demo.local/rag"
echo "ML Models:   http://demo.local/ml-models"
echo "Pipeline:    http://demo.local/pipeline"
echo "Sync Engine: http://demo.local/sync"
echo ""
echo "📝 Note: Add 'demo.local' to your /etc/hosts file pointing to your ingress IP"
echo "💡 To get ingress IP: kubectl get ingress -n demo-linkops"
echo ""
echo "✅ Deployment complete! Your DEMO-LinkOps platform is ready to use."