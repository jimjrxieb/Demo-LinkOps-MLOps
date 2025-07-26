# DEMO-LinkOps Monitoring

This directory contains monitoring configurations for DEMO-LinkOps using Prometheus and Grafana.

## Components

1. **ServiceMonitor**
   - Collects metrics from all DEMO-LinkOps services
   - Scrapes HTTP metrics and health endpoints
   - 15-second collection interval

2. **Grafana Dashboard**
   - HTTP request rates and latencies
   - Memory and CPU usage
   - Service health status
   - Real-time metrics visualization

3. **Prometheus Rules**
   - High error rate alerts (>10%)
   - Slow response time alerts (>2s)
   - Resource usage alerts (>85%)
   - Service health alerts

## Setup

1. Install Prometheus Operator:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

2. Apply monitoring configurations:
```bash
kubectl apply -f service-monitor.yaml
kubectl apply -f grafana-dashboard.yaml
kubectl apply -f prometheus-rules.yaml
```

3. Access Grafana:
```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Visit http://localhost:3000
# Default credentials: admin/prom-operator
```

## Metrics

### HTTP Metrics
- Request rates by endpoint
- Response times (95th percentile)
- Error rates
- Status code distribution

### Resource Metrics
- Memory usage and limits
- CPU usage and quotas
- Container restarts
- Network I/O

### Custom Metrics
- Login success/failure rates
- Session durations
- API endpoint usage
- RAG query performance

## Alerts

1. **High Error Rate**
   - Threshold: >10% errors
   - Window: 5 minutes
   - Severity: Warning

2. **Slow Response Time**
   - Threshold: >2s (95th percentile)
   - Window: 5 minutes
   - Severity: Warning

3. **Resource Usage**
   - Memory: >85% of limit
   - CPU: >85% of quota
   - Window: 5 minutes
   - Severity: Warning

4. **Service Health**
   - Endpoint down >5 minutes
   - Frequent restarts (>3/hour)
   - Severity: Critical

## Dashboard Access

The Grafana dashboard is available at:
- URL: http://localhost:3000 (when port-forwarded)
- Dashboard Name: DEMO-LinkOps Overview
- Refresh Rate: 10 seconds
- Time Range: Last 1 hour (adjustable)

## Troubleshooting

1. **Missing Metrics**
   - Check ServiceMonitor labels
   - Verify endpoint annotations
   - Check port configurations

2. **Alert Issues**
   - Verify PrometheusRule syntax
   - Check label selectors
   - Review alert thresholds

3. **Dashboard Problems**
   - Confirm Grafana sidecar loading
   - Check ConfigMap labels
   - Verify dashboard JSON syntax 