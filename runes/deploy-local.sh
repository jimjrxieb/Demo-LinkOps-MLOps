#!/bin/bash
set -e

echo "🔧 Creating 'linkops' namespace if not exists..."
kubectl get ns linkops || kubectl create namespace linkops

echo "🚀 Deploying all LinkOps services via Helmfile..."
helmfile apply

echo "✅ All services deployed to Kubernetes under 'linkops' namespace."
kubectl get pods -n linkops 