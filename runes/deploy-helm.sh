#!/bin/bash

# LinkOps Demo Helm Deployment Script
# This script deploys the demo stack using Helm

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="linkops-demo"
RELEASE_NAME="linkops-demo"
CHART_PATH="./helm/demo-stack"

echo -e "${BLUE}🚀 LinkOps Demo Helm Deployment${NC}"
echo "=================================="

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}❌ Helm is not installed. Please install Helm first.${NC}"
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl is not installed. Please install kubectl first.${NC}"
    exit 1
fi

# Check if we have a valid kubeconfig
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Cannot connect to Kubernetes cluster. Please check your kubeconfig.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Create namespace if it doesn't exist
echo -e "${YELLOW}📦 Creating namespace: ${NAMESPACE}${NC}"
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# Check if values file exists
if [ ! -f "${CHART_PATH}/values.yaml" ]; then
    echo -e "${RED}❌ Values file not found at ${CHART_PATH}/values.yaml${NC}"
    exit 1
fi

# Update Helm dependencies
echo -e "${YELLOW}📥 Updating Helm dependencies...${NC}"
cd ${CHART_PATH}
helm dependency update
cd - > /dev/null

# Deploy the chart
echo -e "${YELLOW}🚀 Deploying LinkOps Demo Stack...${NC}"
helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} \
    --namespace ${NAMESPACE} \
    --create-namespace \
    --wait \
    --timeout 10m

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"

# Show deployment status
echo -e "${BLUE}📊 Deployment Status:${NC}"
kubectl get pods -n ${NAMESPACE}

echo -e "${BLUE}🌐 Services:${NC}"
kubectl get services -n ${NAMESPACE}

echo -e "${BLUE}🔗 Ingress:${NC}"
kubectl get ingress -n ${NAMESPACE}

echo ""
echo -e "${GREEN}🎉 LinkOps Demo is now deployed!${NC}"
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Add 'demo.linkops.local' to your /etc/hosts file pointing to your cluster IP"
echo "2. Access the frontend at: http://demo.linkops.local"
echo "3. Check logs with: kubectl logs -n ${NAMESPACE} -l app.kubernetes.io/name=frontend"
echo ""
echo -e "${YELLOW}🔧 Useful commands:${NC}"
echo "  View logs: kubectl logs -n ${NAMESPACE} -f deployment/${RELEASE_NAME}-frontend"
echo "  Port forward: kubectl port-forward -n ${NAMESPACE} svc/${RELEASE_NAME}-frontend 3000:3000"
echo "  Uninstall: helm uninstall ${RELEASE_NAME} -n ${NAMESPACE}" 