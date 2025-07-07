#!/bin/bash

# LinkOps MLOps Platform - Deployment Validation Script
# This script validates that all components are properly deployed and healthy

set -e

NAMESPACE=${1:-linkops}
TIMEOUT=${2:-300}
INTERVAL=${3:-10}

echo "🔍 Validating LinkOps MLOps Platform deployment in namespace: $NAMESPACE"
echo "⏱️  Timeout: ${TIMEOUT}s, Check interval: ${INTERVAL}s"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "OK")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
    esac
}

# Function to check if namespace exists
check_namespace() {
    if kubectl get namespace $NAMESPACE >/dev/null 2>&1; then
        print_status "OK" "Namespace '$NAMESPACE' exists"
        return 0
    else
        print_status "ERROR" "Namespace '$NAMESPACE' does not exist"
        return 1
    fi
}

# Function to check if all pods are running
check_pods() {
    local failed_pods=$(kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running,status.phase!=Succeeded --no-headers 2>/dev/null | wc -l)
    local total_pods=$(kubectl get pods -n $NAMESPACE --no-headers 2>/dev/null | wc -l)
    
    if [ "$failed_pods" -eq 0 ] && [ "$total_pods" -gt 0 ]; then
        print_status "OK" "All $total_pods pods are running"
        return 0
    else
        print_status "ERROR" "$failed_pods/$total_pods pods are not running"
        kubectl get pods -n $NAMESPACE
        return 1
    fi
}

# Function to check if all services are available
check_services() {
    local services=$(kubectl get svc -n $NAMESPACE --no-headers 2>/dev/null | wc -l)
    if [ "$services" -gt 0 ]; then
        print_status "OK" "$services services are available"
        return 0
    else
        print_status "ERROR" "No services found"
        return 1
    fi
}

# Function to check if ingress is configured
check_ingress() {
    local ingress_count=$(kubectl get ingress -n $NAMESPACE --no-headers 2>/dev/null | wc -l)
    if [ "$ingress_count" -gt 0 ]; then
        print_status "OK" "$ingress_count ingress resources configured"
        return 0
    else
        print_status "WARNING" "No ingress resources found"
        return 0
    fi
}

# Function to check if persistent volumes are bound
check_persistent_volumes() {
    local unbound_pvcs=$(kubectl get pvc -n $NAMESPACE --no-headers 2>/dev/null | grep -v "Bound" | wc -l)
    local total_pvcs=$(kubectl get pvc -n $NAMESPACE --no-headers 2>/dev/null | wc -l)
    
    if [ "$unbound_pvcs" -eq 0 ] && [ "$total_pvcs" -gt 0 ]; then
        print_status "OK" "All $total_pvcs persistent volume claims are bound"
        return 0
    elif [ "$total_pvcs" -eq 0 ]; then
        print_status "INFO" "No persistent volume claims found"
        return 0
    else
        print_status "ERROR" "$unbound_pvcs/$total_pvcs persistent volume claims are not bound"
        kubectl get pvc -n $NAMESPACE
        return 1
    fi
}

# Function to check if secrets exist
check_secrets() {
    local required_secrets=("whis-secrets" "audit-secrets" "postgres-secrets" "grafana-secrets")
    local missing_secrets=0
    
    for secret in "${required_secrets[@]}"; do
        if kubectl get secret $secret -n $NAMESPACE >/dev/null 2>&1; then
            print_status "OK" "Secret '$secret' exists"
        else
            print_status "WARNING" "Secret '$secret' not found"
            ((missing_secrets++))
        fi
    done
    
    if [ "$missing_secrets" -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

# Function to check service health endpoints
check_health_endpoints() {
    print_status "INFO" "Checking service health endpoints..."
    
    # Check MLOps Platform health
    if kubectl get svc mlops-platform -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/mlops-platform -- curl -f http://localhost:8000/health >/dev/null 2>&1; then
            print_status "OK" "MLOps Platform health check passed"
        else
            print_status "ERROR" "MLOps Platform health check failed"
        fi
    fi
    
    # Check Frontend health
    if kubectl get svc frontend -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/frontend -- curl -f http://localhost:80/ >/dev/null 2>&1; then
            print_status "OK" "Frontend health check passed"
        else
            print_status "ERROR" "Frontend health check failed"
        fi
    fi
    
    # Check Audit Assess health
    if kubectl get svc audit-assess -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/audit-assess -- curl -f http://localhost:8003/health >/dev/null 2>&1; then
            print_status "OK" "Audit Assess health check passed"
        else
            print_status "ERROR" "Audit Assess health check failed"
        fi
    fi
}

# Function to check database connectivity
check_database() {
    if kubectl get svc postgres -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/postgres -- pg_isready -U mlops >/dev/null 2>&1; then
            print_status "OK" "PostgreSQL database is ready"
            return 0
        else
            print_status "ERROR" "PostgreSQL database is not ready"
            return 1
        fi
    else
        print_status "WARNING" "PostgreSQL service not found"
        return 0
    fi
}

# Function to check Redis connectivity
check_redis() {
    if kubectl get svc redis -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/redis -- redis-cli ping >/dev/null 2>&1; then
            print_status "OK" "Redis is ready"
            return 0
        else
            print_status "ERROR" "Redis is not ready"
            return 1
        fi
    else
        print_status "WARNING" "Redis service not found"
        return 0
    fi
}

# Function to check monitoring stack
check_monitoring() {
    # Check Prometheus
    if kubectl get svc prometheus -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/prometheus -- wget -qO- http://localhost:9090/-/healthy >/dev/null 2>&1; then
            print_status "OK" "Prometheus is healthy"
        else
            print_status "ERROR" "Prometheus is not healthy"
        fi
    fi
    
    # Check Grafana
    if kubectl get svc grafana -n $NAMESPACE >/dev/null 2>&1; then
        if kubectl exec -n $NAMESPACE deployment/grafana -- curl -f http://localhost:3000/api/health >/dev/null 2>&1; then
            print_status "OK" "Grafana is healthy"
        else
            print_status "ERROR" "Grafana is not healthy"
        fi
    fi
}

# Function to wait for deployment to be ready
wait_for_deployment() {
    local start_time=$(date +%s)
    local end_time=$((start_time + TIMEOUT))
    
    print_status "INFO" "Waiting for deployment to be ready..."
    
    while [ $(date +%s) -lt $end_time ]; do
        if check_pods && check_services; then
            print_status "OK" "Deployment is ready!"
            return 0
        fi
        
        print_status "INFO" "Waiting for deployment to be ready... ($(($(date +%s) - start_time))s elapsed)"
        sleep $INTERVAL
    done
    
    print_status "ERROR" "Deployment did not become ready within ${TIMEOUT}s"
    return 1
}

# Main validation function
main() {
    local exit_code=0
    
    echo "🚀 Starting LinkOps MLOps Platform validation..."
    echo ""
    
    # Check namespace
    if ! check_namespace; then
        exit_code=1
    fi
    
    # Wait for deployment to be ready
    if ! wait_for_deployment; then
        exit_code=1
    fi
    
    echo ""
    print_status "INFO" "Running comprehensive health checks..."
    echo ""
    
    # Run all checks
    if ! check_pods; then exit_code=1; fi
    if ! check_services; then exit_code=1; fi
    if ! check_ingress; then exit_code=1; fi
    if ! check_persistent_volumes; then exit_code=1; fi
    if ! check_secrets; then exit_code=1; fi
    if ! check_database; then exit_code=1; fi
    if ! check_redis; then exit_code=1; fi
    
    echo ""
    print_status "INFO" "Checking service health endpoints..."
    check_health_endpoints
    
    echo ""
    print_status "INFO" "Checking monitoring stack..."
    check_monitoring
    
    echo ""
    echo "📊 Deployment Summary:"
    echo "======================"
    kubectl get pods,svc,ingress,pvc -n $NAMESPACE
    
    echo ""
    if [ $exit_code -eq 0 ]; then
        print_status "OK" "🎉 LinkOps MLOps Platform deployment validation completed successfully!"
        echo ""
        echo "🌐 Access your platform:"
        echo "   - Frontend: https://linkops.com (if ingress configured)"
        echo "   - MLOps Platform API: http://mlops-platform:8000"
        echo "   - Grafana: https://grafana.linkops.com (if ingress configured)"
        echo ""
        echo "📚 Next steps:"
        echo "   1. Configure your API keys in the secrets"
        echo "   2. Set up your ingress DNS records"
        echo "   3. Access the platform and start using it!"
    else
        print_status "ERROR" "❌ LinkOps MLOps Platform deployment validation failed!"
        echo ""
        echo "🔧 Troubleshooting:"
        echo "   1. Check pod logs: kubectl logs -n $NAMESPACE <pod-name>"
        echo "   2. Check events: kubectl get events -n $NAMESPACE"
        echo "   3. Check service status: kubectl describe svc -n $NAMESPACE"
        echo "   4. Check ingress: kubectl describe ingress -n $NAMESPACE"
    fi
    
    exit $exit_code
}

# Run main function
main "$@" 