#!/bin/bash
"""
Kubernetes Cleanup Script for DEMO-LinkOps

This script removes the DEMO-LinkOps deployment from Kubernetes.
"""

set -e

echo "🧹 Cleaning up DEMO-LinkOps from Kubernetes..."

# Function to safely delete resources
safe_delete() {
    local resource=$1
    echo "🗑️  Deleting $resource..."
    kubectl delete -f $resource --ignore-not-found=true
}

# Delete in reverse order
echo "1️⃣ Removing ingress..."
safe_delete ingress.yaml

echo "2️⃣ Removing frontend..."
safe_delete frontend-service.yaml
safe_delete frontend-deployment.yaml

echo "3️⃣ Removing unified API..."
safe_delete backend-service.yaml
safe_delete backend-deployment.yaml

echo "4️⃣ Removing backend microservices..."
safe_delete sync-engine.yaml
safe_delete pipeline.yaml
safe_delete ml-models.yaml
safe_delete rag-deployment.yaml
safe_delete rag-service.yaml

echo "5️⃣ Removing database services..."
safe_delete redis.yaml
safe_delete postgres.yaml

echo "6️⃣ Removing configuration..."
safe_delete secrets.yaml
safe_delete configmap.yaml

echo "7️⃣ Removing namespace..."
safe_delete namespace.yaml

echo "🎉 DEMO-LinkOps cleanup completed!"

# Show remaining resources (should be empty)
echo ""
echo "📊 Remaining resources in demo-linkops namespace:"
kubectl get all -n demo-linkops 2>/dev/null || echo "✅ Namespace successfully removed"