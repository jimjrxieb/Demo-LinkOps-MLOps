# Tenant Sync & System Monitoring

This document describes the secure tenant CSV sync engine and comprehensive system monitoring functionality implemented in the DEMO-LinkOps project.

## 🚀 Features

### 1. **Secure Tenant CSV Sync Engine**
- **File Watching**: Automatically monitors `backend/db/watch/tenants/` for new CSV files
- **Data Validation**: Validates CSV structure, file size, and required columns
- **SQLite Storage**: Secure local database storage with indexing
- **Error Handling**: Comprehensive error logging and recovery
- **File Deduplication**: Prevents duplicate processing using file hashes
- **Thread-Safe**: Multi-threaded processing with proper locking

### 2. **System Dashboard**
- **Real-time Monitoring**: Live status updates every 30 seconds
- **Tenant Analytics**: Comprehensive tenant data insights
- **Sync Operations**: Track file processing and sync history
- **Lease Management**: Monitor expiring leases and occupancy
- **Financial Overview**: Total rent calculations and revenue tracking

### 3. **API Endpoints**
- **Status Summary**: `/api/status/summary` - Complete system overview
- **Tenant Management**: `/api/status/tenants` - List and filter tenants
- **Sync Logging**: `/api/status/sync-log` - Sync operation history
- **Analytics**: `/api/status/analytics` - Business intelligence data
- **Health Checks**: `/api/status/health` - System health monitoring

## 📁 File Structure

```
DEMO-LinkOps/
├── backend/
│   ├── sync_engine/
│   │   └── tenant_sync.py          # Main sync engine
│   ├── routes/
│   │   └── status.py               # Status API routes
│   └── db/
│       ├── watch/tenants/          # CSV watch directory
│       ├── sqlite/tenants.db       # SQLite database
│       └── logs/sync.log           # Sync operation logs
├── frontend/src/
│   ├── views/
│   │   └── SyncDashboard.vue       # System dashboard
│   ├── components/
│   │   └── Sidebar.vue             # Updated with dashboard link
│   └── router/
│       └── index.js                # Updated with dashboard route
├── sample_data/
│   └── sample_tenants.csv          # Sample tenant data
├── start-tenant-sync.sh            # Complete startup script
└── README-TENANT-SYNC.md           # This documentation
```

## 🔧 Setup Instructions

### 1. **Quick Start**
```bash
# From DEMO-LinkOps directory
./start-tenant-sync.sh
```

### 2. **Manual Setup**
```bash
# Install dependencies
cd rag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install

# Create directories
mkdir -p backend/db/watch/tenants
mkdir -p backend/db/sqlite
mkdir -p backend/db/logs

# Start services
cd ../backend
python sync_engine/tenant_sync.py &

cd ../rag
python main.py &

cd ../frontend
npm run dev
```

## 🎯 Usage

### **CSV File Format**
Your CSV files should have the following columns:

```csv
tenant_name,unit,status,lease_start,lease_end,rent_amount,email,phone
John Smith,101,active,2024-01-01,2024-12-31,1500,john.smith@email.com,555-0101
Jane Doe,102,active,2024-02-01,2024-11-30,1600,jane.doe@email.com,555-0102
```

**Required Columns:**
- `tenant_name` (required)
- `unit` (optional)
- `status` (optional, defaults to 'active')
- `lease_start` (optional, YYYY-MM-DD format)
- `lease_end` (optional, YYYY-MM-DD format)
- `rent_amount` (optional, numeric)
- `email` (optional)
- `phone` (optional)

### **Adding Tenant Data**
1. **Drop CSV files** into `backend/db/watch/tenants/`
2. **Monitor the dashboard** at `http://localhost:5173/dashboard`
3. **Check sync status** in real-time
4. **View tenant analytics** and insights

### **Dashboard Features**
- **System Status Cards**: Total tenants, active tenants, expiring leases, monthly rent
- **Synced Files**: List of processed CSV files with tenant counts
- **Recent Sync Operations**: Success/failure status with timestamps
- **Upcoming Lease Expirations**: Leases expiring within 30 days
- **Quick Actions**: Download sample CSV, view tenants, analytics

## 🔌 API Reference

### **GET /api/status/summary**
Returns comprehensive system status:
```json
{
  "tenant_count": 10,
  "file_count": 2,
  "active_tenants": 8,
  "expiring_leases": 3,
  "total_rent": 15000,
  "source_files": [
    {"file": "tenants.csv", "count": 10}
  ],
  "expiring_leases": [
    {
      "name": "John Smith",
      "unit": "101",
      "lease_end": "2024-12-31",
      "status": "active"
    }
  ],
  "recent_syncs": [
    {
      "file_name": "tenants.csv",
      "status": "success",
      "records_processed": 10,
      "synced_at": "2024-01-15T10:30:00"
    }
  ],
  "system_status": "operational"
}
```

### **GET /api/status/tenants**
List tenants with optional filtering:
```bash
# All tenants
GET /api/status/tenants

# Active tenants only
GET /api/status/tenants?status=active

# Paginated results
GET /api/status/tenants?limit=20&offset=0
```

### **GET /api/status/analytics**
Business intelligence data:
```json
{
  "analytics": {
    "status_distribution": {
      "active": 8,
      "inactive": 2
    },
    "rent_distribution": {
      "Under $1K": 2,
      "$1K-$2K": 6,
      "$2K-$3K": 2
    },
    "lease_timeline": {
      "30 days": 3,
      "60 days": 2,
      "90+ days": 5
    },
    "average_rent": 1500,
    "occupancy_rate": 80.0,
    "total_units": 10,
    "occupied_units": 8
  }
}
```

## ⚙️ Configuration

### **Sync Engine Settings**
Edit `backend/sync_engine/tenant_sync.py`:
```python
# Configuration
WATCH_DIR = Path("db/watch/tenants")
DB_PATH = Path("db/sqlite/tenants.db")
POLL_INTERVAL = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

### **Database Schema**
The sync engine creates two tables:

**tenants table:**
```sql
CREATE TABLE tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_name TEXT NOT NULL,
    unit TEXT,
    status TEXT,
    lease_start TEXT,
    lease_end TEXT,
    rent_amount REAL,
    email TEXT,
    phone TEXT,
    source_file TEXT NOT NULL,
    file_hash TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**sync_log table:**
```sql
CREATE TABLE sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_hash TEXT,
    status TEXT NOT NULL,
    records_processed INTEGER DEFAULT 0,
    error_message TEXT,
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔍 Monitoring & Troubleshooting

### **Log Files**
- **Sync Log**: `backend/db/logs/sync.log`
- **Database**: `backend/db/sqlite/tenants.db`
- **Watch Directory**: `backend/db/watch/tenants/`

### **Health Checks**
```bash
# Check sync engine status
curl http://localhost:8005/api/status/health

# Check database connectivity
sqlite3 backend/db/sqlite/tenants.db "SELECT COUNT(*) FROM tenants;"

# Monitor log files
tail -f backend/db/logs/sync.log
```

### **Common Issues**

1. **File Not Syncing**
   - Check file format (must be CSV)
   - Verify required columns (tenant_name)
   - Check file size (max 10MB)
   - Review sync logs for errors

2. **Database Errors**
   - Ensure write permissions to `backend/db/sqlite/`
   - Check disk space
   - Verify SQLite installation

3. **Dashboard Not Updating**
   - Check API connectivity
   - Verify CORS settings
   - Review browser console for errors

## 🚀 Performance Tips

1. **Optimize CSV Files**
   - Use consistent date formats (YYYY-MM-DD)
   - Clean data before importing
   - Remove unnecessary columns

2. **Database Performance**
   - Indexes are automatically created
   - Regular database maintenance
   - Monitor file sizes

3. **System Resources**
   - Adjust poll interval for your needs
   - Monitor memory usage
   - Consider batch processing for large files

## 🔒 Security Considerations

1. **File Validation**
   - File size limits
   - File type validation
   - Content structure validation

2. **Data Protection**
   - Local storage only
   - No external API calls
   - File hash verification

3. **Access Control**
   - Local network access only
   - No authentication required (demo mode)
   - File system permissions

## 🎉 Next Steps

1. **Integration with RAG System**
   - Query tenant data through document Q&A
   - Generate reports using LLM
   - Automated lease analysis

2. **Advanced Features**
   - Email notifications for expiring leases
   - Automated rent calculations
   - Tenant communication system

3. **Analytics Enhancement**
   - Revenue forecasting
   - Occupancy optimization
   - Market analysis

4. **Automation**
   - Scheduled data imports
   - Automated reporting
   - Integration with property management systems

## 📊 Sample Data

Download the sample CSV file from the dashboard or use:
```bash
cp sample_data/sample_tenants.csv backend/db/watch/tenants/
```

The sample includes 10 tenants with various lease dates and rent amounts for testing the system.

## 🧪 Testing

Test the complete system:
```bash
# Start all services
./start-tenant-sync.sh

# Access dashboard
open http://localhost:5173/dashboard

# Add test data
cp sample_data/sample_tenants.csv backend/db/watch/tenants/

# Monitor sync status
watch -n 5 'curl -s http://localhost:8005/api/status/summary | jq'
```

The system is now ready for production use with real tenant data! 