#!/bin/bash
"""
Kubernetes Manifest Validation Script for DEMO-LinkOps

This script validates all Kubernetes manifests before deployment.
"""

set -e

echo "🔍 Validating DEMO-LinkOps Kubernetes manifests..."

# Array of manifest files in deployment order
MANIFESTS=(
    "namespace.yaml"
    "configmap.yaml" 
    "secrets.yaml"
    "postgres.yaml"
    "redis.yaml"
    "rag-service.yaml"
    "rag-deployment.yaml"
    "ml-models.yaml"
    "pipeline.yaml"
    "sync-engine.yaml"
    "backend-deployment.yaml"
    "backend-service.yaml"
    "frontend-deployment.yaml"
    "frontend-service.yaml" 
    "ingress.yaml"
)

# Function to validate a single manifest
validate_manifest() {
    local manifest=$1
    echo "📋 Validating $manifest..."
    
    if [[ ! -f "$manifest" ]]; then
        echo "❌ ERROR: Manifest file '$manifest' not found!"
        return 1
    fi
    
    # Validate YAML syntax
    if ! kubectl apply --dry-run=client -f "$manifest" >/dev/null 2>&1; then
        echo "❌ ERROR: Invalid YAML syntax in '$manifest'"
        kubectl apply --dry-run=client -f "$manifest"
        return 1
    fi
    
    # Validate Kubernetes schema
    if ! kubectl apply --dry-run=server -f "$manifest" >/dev/null 2>&1; then
        echo "⚠️  WARNING: Schema validation issues in '$manifest'"
        kubectl apply --dry-run=server -f "$manifest"
    fi
    
    echo "✅ $manifest is valid"
    return 0
}

# Validate all manifests
ERRORS=0
for manifest in "${MANIFESTS[@]}"; do
    if ! validate_manifest "$manifest"; then
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
echo "📊 Validation Summary:"
echo "======================"
echo "Total manifests: ${#MANIFESTS[@]}"
echo "Errors found: $ERRORS"

if [[ $ERRORS -eq 0 ]]; then
    echo "🎉 All manifests are valid!"
    echo ""
    echo "🚀 Ready for deployment! Run:"
    echo "   ./deploy.sh"
    exit 0
else
    echo "❌ Found $ERRORS errors. Please fix them before deployment."
    exit 1
fi