# Enhanced Demo Flow Documentation

## Overview

This document describes the complete enhanced demo flow for the ZRS Property Management system, including ML model integration, sync workflows, and end-to-end testing scenarios.

## Demo Components

### 1. Core Demo Flow
- **RAG Search**: Query property management data
- **Demo Sync**: Load and manage demo data
- **ML Model Training**: Train vendor suggestion models
- **Auto-Sync**: Automated retraining workflows
- **Manager Confirmation**: Safe email sending with approval

### 2. ML Model Integration
- **Vendor Suggestion Model**: TensorFlow-based contractor recommendations
- **Quick Training**: Fast model training with demo data
- **Retraining**: Update existing models with new data
- **Auto-Sync**: Automated model updates

## Complete Demo Scenarios

### Scenario 1: Basic RAG Demo Flow
```
1. Initial State: No data loaded
2. User Query: "Who has overdue payments?"
3. Response: Fallback message + "Go Sync Demo Data" link
4. Sync Data: Load delinquency.csv → Success
5. Re-query: Get accurate answer + "Send Reminder Emails" button
6. Send Emails: Manager confirmation → Success
7. Clear Data: Reset to initial state
```

### Scenario 2: ML Model Training Flow
```
1. Navigate to ML Model Creator
2. Upload vendor_suggestions.csv
3. Configure model settings
4. Quick Training: ⚡ Train Now (Quick)
5. View training results and vendor recommendations
6. Retrain: 🔄 Retrain Existing
7. Compare improved metrics
```

### Scenario 3: Auto-Sync Workflow
```
1. Enable Auto-Sync in advanced settings
2. Add new data to demo_data/
3. Trigger auto-sync: /api/train-model/auto-sync
4. Monitor background retraining
5. Verify updated models
```

### Scenario 4: End-to-End Property Management
```
1. Sync demo data (delinquency.csv)
2. Query: "Which tenants need immediate attention?"
3. Get RAG results with tenant details
4. Train vendor suggestion model
5. Query: "Recommend contractors for HVAC repair"
6. Get ML-powered vendor recommendations
7. Send reminder emails (with confirmation)
8. Clear demo state
```

## API Endpoints

### Demo Sync Endpoints
```http
POST /api/demo/sync          # Sync demo data
GET  /api/demo/status        # Check demo status
DELETE /api/demo/clear       # Clear demo data
```

### ML Model Endpoints
```http
POST /api/train-model/quick      # Quick training
POST /api/train-model/retrain    # Retrain existing
POST /api/train-model/auto-sync  # Trigger auto-sync
GET  /api/train-model/health     # Health check
GET  /api/train-model/models     # List models
GET  /api/train-model/progress/{model_name}  # Training progress
```

### RAG Search Endpoints
```http
POST /api/rag/query         # Basic search
POST /api/rag/query-llm     # LLM-enhanced search
```

### MCP Tool Endpoints
```http
POST /api/mcp-tool/execute/send_emails  # Send reminder emails
```

## Data Files

### Demo Data Structure
```
demo_data/
├── delinquency.csv              # Property management data
└── vendor_suggestions.csv       # Vendor recommendation data
```

### Model Storage
```
db/
├── models/                      # Trained model files
│   ├── *.pkl                   # Model files
│   ├── *_metadata.json         # Model metadata
│   └── deployments.json        # Deployment info
└── mcp_tools/
    └── send_emails.json        # Preloaded MCP tool
```

## Frontend Components

### Key Vue Components
- **LLMChat.vue**: Main chat interface with Q&A flow
- **DemoSync.vue**: Demo data management
- **ModelCreator.vue**: ML model training interface
- **Sidebar.vue**: Navigation

### Enhanced Features
- **Manager Confirmation**: Email sending approval
- **Training Options**: Quick training, retraining, auto-sync
- **Progress Tracking**: Real-time training progress
- **Demo Reset**: Complete state management

## Testing Scenarios

### E2E Smoke Tests

#### Test 1: Complete Demo Cycle
```bash
# 1. Start with no data
curl -X GET /api/demo/status
# Expected: {"status": "not_loaded"}

# 2. Sync demo data
curl -X POST /api/demo/sync
# Expected: {"status": "Sync complete"}

# 3. Query RAG
curl -X POST /api/rag/query -d '{"query": "overdue payments"}'
# Expected: Results with tenant data

# 4. Train ML model
curl -X POST /api/train-model/quick -d '{"model_name": "test_model"}'
# Expected: Training started

# 5. Check progress
curl -X GET /api/train-model/progress/test_model
# Expected: Training progress

# 6. Clear demo data
curl -X DELETE /api/demo/clear
# Expected: Data cleared
```

#### Test 2: ML Model Workflow
```bash
# 1. Quick training
curl -X POST /api/train-model/quick -d '{
  "model_name": "vendor_model",
  "include_demo_data": true,
  "auto_sync": false
}'

# 2. Retrain model
curl -X POST /api/train-model/retrain -d '{
  "model_name": "vendor_model",
  "include_demo_data": true
}'

# 3. Auto-sync
curl -X POST /api/train-model/auto-sync

# 4. Health check
curl -X GET /api/train-model/health
```

#### Test 3: Manager Confirmation Flow
```bash
# 1. Sync demo data
curl -X POST /api/demo/sync

# 2. Query with delinquency
curl -X POST /api/rag/query -d '{"query": "delinquent tenants"}'

# 3. Send emails (should require confirmation in frontend)
curl -X POST /api/mcp-tool/execute/send_emails
```

## Configuration

### Environment Variables
```bash
# Demo configuration
DEMO_DATA_PATH=demo_data/
DEMO_AUTO_SYNC=true
DEMO_CONFIRMATION_REQUIRED=true

# ML model configuration
ML_MODEL_PATH=db/models/
ML_AUTO_SYNC_ENABLED=true
ML_TRAINING_TIMEOUT=300
```

### Advanced Settings
```json
{
  "autoSync": false,
  "includeDemoData": true,
  "trainingTimeout": 300,
  "maxModels": 10,
  "retentionDays": 30
}
```

## Troubleshooting

### Common Issues

#### 1. Demo Sync Fails
```bash
# Check file existence
ls -la demo_data/delinquency.csv

# Check permissions
chmod 644 demo_data/delinquency.csv

# Verify CSV format
head -5 demo_data/delinquency.csv
```

#### 2. ML Training Fails
```bash
# Check model service
curl -X GET /api/train-model/health

# Check disk space
df -h db/models/

# Check logs
tail -f logs/ml_models.log
```

#### 3. RAG Search Issues
```bash
# Check RAG service
curl -X GET /api/rag/health

# Check document count
curl -X GET /api/rag/count

# Clear and re-sync
curl -X DELETE /api/demo/clear
curl -X POST /api/demo/sync
```

### Debug Commands
```bash
# Check all services
curl -X GET /health

# List all models
curl -X GET /api/train-model/models

# Check demo status
curl -X GET /api/demo/status

# Monitor training progress
watch -n 2 'curl -s /api/train-model/progress/test_model | jq'
```

## Performance Metrics

### Expected Performance
- **Demo Sync**: < 5 seconds
- **Quick Training**: < 30 seconds
- **RAG Query**: < 2 seconds
- **ML Prediction**: < 1 second
- **Auto-Sync**: < 60 seconds

### Monitoring
```bash
# Monitor API performance
curl -w "@curl-format.txt" -X GET /health

# Check model accuracy
curl -X GET /api/train-model/models | jq '.[].metrics'

# Monitor training progress
curl -X GET /api/train-model/progress/* | jq
```

## Security Considerations

### Manager Confirmation
- ✅ Email sending requires explicit approval
- ✅ Confirmation dialog prevents accidental actions
- ✅ Clear audit trail of confirmations

### Data Protection
- ✅ Demo data is isolated
- ✅ No real emails sent in demo mode
- ✅ Secure model storage

### Access Control
- ✅ API rate limiting
- ✅ Input validation
- ✅ Error handling

## Future Enhancements

### Planned Features
- **Multi-step Confirmation**: Advanced approval workflows
- **Audit Trail**: Complete action logging
- **Role-based Permissions**: Different confirmation levels
- **Email Templates**: Preview before sending
- **Batch Operations**: Multiple action confirmations

### Scalability Improvements
- **Confirmation History**: Track user confirmations
- **Approval Workflows**: Multi-level approval chains
- **Demo Snapshots**: Save/restore demo states
- **Automated Testing**: E2E test automation

## Conclusion

This enhanced demo flow provides a **comprehensive, safe, and professional** demonstration of the ZRS Property Management system with:

- ✅ **Complete RAG integration** with fallback messaging
- ✅ **Advanced ML model training** with quick training and retraining
- ✅ **Manager confirmation** for safe email sending
- ✅ **Auto-sync capabilities** for automated workflows
- ✅ **Complete demo reset** functionality
- ✅ **Professional documentation** and testing scenarios

The demo is **production-ready** and provides an excellent foundation for showcasing the system's capabilities while maintaining security and user experience standards. 