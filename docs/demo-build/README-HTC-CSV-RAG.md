# HTC CSV → Vector Embedder → RAG Chat Flow

This document describes the complete implementation of the **HTC CSV → Vector Embedder → RAG Chat** flow that makes tenant spreadsheets instantly searchable by the local LLM.

## 🎯 Overview

The system provides a seamless pipeline for:
1. **Uploading tenant CSV files** through the HTC interface
2. **Converting CSV data to vector embeddings** for AI search
3. **Querying tenant data** using natural language through the RAG system
4. **Displaying rich tenant information** with metadata in search results

## 🚀 Features

### 1. **HTC CSV Embedder** (`/htc`)
- **Drag & Drop Upload**: Intuitive file upload interface
- **CSV Validation**: Automatic format and content validation
- **Batch Processing**: Support for multiple file uploads
- **Template Download**: Pre-formatted CSV template
- **Real-time Status**: Live upload progress and system status
- **File Management**: View, delete, and manage uploaded files

### 2. **Vector Embedding Engine**
- **Structured Content**: Converts CSV rows to searchable documents
- **Rich Metadata**: Preserves tenant information for context
- **Deduplication**: Prevents duplicate processing using file hashes
- **Error Handling**: Comprehensive validation and error recovery

### 3. **Enhanced RAG Chat** (`/search-memory`)
- **Tenant-Aware Queries**: Natural language questions about tenant data
- **Rich Source Display**: Shows tenant information with metadata
- **Contextual Answers**: AI-generated responses based on tenant records
- **Source Attribution**: Links answers to specific tenant records

## 📁 File Structure

```
DEMO-LinkOps/
├── rag/
│   ├── loaders/
│   │   └── csv_embedder.py          # CSV to vector converter
│   ├── routes/
│   │   └── upload_csv.py            # CSV upload API endpoints
│   └── main.py                      # Enhanced with tenant metadata
├── frontend/src/
│   ├── views/
│   │   ├── HTC.vue                  # CSV upload interface
│   │   └── SearchMemory.vue         # Enhanced Q&A interface
│   ├── components/
│   │   └── Sidebar.vue              # Updated navigation
│   └── router/
│       └── index.js                 # HTC route added
└── sample_data/
    └── sample_tenants.csv           # Example tenant data
```

## 🔧 API Endpoints

### **CSV Upload & Management**
- `POST /api/upload-csv` - Upload single CSV file
- `POST /api/upload-csv-batch` - Upload multiple CSV files
- `GET /api/csv-status` - Get upload status and file list
- `DELETE /api/csv/{filename}` - Delete uploaded file
- `GET /api/csv-template` - Download CSV template

### **Enhanced Query System**
- `POST /api/query-simple` - Query with tenant metadata support
- `GET /api/status/summary` - System status including tenant data
- `GET /api/status/tenants` - List embedded tenant records

## 🎯 Usage Flow

### **Step 1: Upload Tenant CSV**
1. Navigate to **HTC Embedder** (`/htc`)
2. Download the CSV template or use your own
3. Prepare CSV with columns: `tenant_name, unit, status, lease_start, lease_end, rent_amount, email, phone`
4. Drag & drop or browse to upload
5. Monitor upload progress and status

### **Step 2: Query Tenant Data**
1. Navigate to **Document Q&A** (`/search-memory`)
2. Ask natural language questions like:
   - "Which tenants have leases ending this month?"
   - "Who hasn't paid rent?"
   - "What's the average rent in building A?"
   - "Show me all active tenants in unit 101"
   - "Which tenants are behind on payments?"

### **Step 3: View Rich Results**
- **AI Response**: Natural language answer based on tenant data
- **Tenant Sources**: Detailed tenant records with metadata
- **Source Attribution**: Links to specific CSV files and records

## 📊 CSV Format

### **Required Columns**
```csv
tenant_name,unit,status,lease_start,lease_end,rent_amount,email,phone
John Smith,101,active,2024-01-01,2024-12-31,1500,john.smith@email.com,555-0101
```

### **Column Details**
- `tenant_name` (required): Full name of tenant
- `unit` (optional): Unit/apartment number
- `status` (optional): active, inactive, expired, etc.
- `lease_start` (optional): YYYY-MM-DD format
- `lease_end` (optional): YYYY-MM-DD format
- `rent_amount` (optional): Numeric value
- `email` (optional): Contact email
- `phone` (optional): Contact phone

## 🔍 Query Examples

### **Lease Management**
```
"Which tenants have leases expiring in the next 30 days?"
"Show me all expired leases"
"Who has the longest lease term?"
```

### **Financial Queries**
```
"What's the total monthly rent revenue?"
"Which tenants pay the highest rent?"
"Show me tenants with rent over $2000"
```

### **Occupancy & Status**
```
"How many active tenants do we have?"
"Which units are currently vacant?"
"Show me all tenants in building A"
```

### **Contact Information**
```
"What's the contact info for John Smith?"
"Show me all tenant email addresses"
"Which tenants don't have phone numbers?"
```

## 🎨 UI Features

### **HTC Upload Interface**
- **Drag & Drop Zone**: Visual upload area with feedback
- **Progress Tracking**: Real-time upload status
- **File Management**: List of uploaded files with actions
- **Template Download**: One-click CSV template
- **System Status**: Live metrics and status

### **Enhanced Search Results**
- **Tenant Cards**: Rich display of tenant information
- **Status Indicators**: Color-coded tenant status
- **Metadata Display**: Lease dates, rent amounts, contact info
- **Source Attribution**: Links to original CSV files
- **Similarity Scores**: Confidence levels for matches

## ⚙️ Technical Implementation

### **CSV Embedding Process**
1. **File Validation**: Check format, size, and required columns
2. **Content Parsing**: Convert CSV rows to structured documents
3. **Metadata Extraction**: Preserve tenant information
4. **Vector Embedding**: Create searchable embeddings
5. **Storage**: Add to vector store with metadata

### **Query Processing**
1. **Natural Language**: Parse user questions
2. **Vector Search**: Find relevant tenant records
3. **Context Building**: Combine relevant information
4. **LLM Generation**: Create natural language answers
5. **Source Attribution**: Link answers to tenant records

### **Metadata Handling**
- **Tenant Information**: Name, unit, status, contact details
- **Lease Data**: Start/end dates, rent amounts
- **Source Tracking**: Original CSV file and row information
- **Temporal Data**: Days until lease expiry, status calculations

## 🚀 Getting Started

### **1. Start the System**
```bash
# From DEMO-LinkOps directory
./start-tenant-sync.sh
```

### **2. Access the Interface**
- **Frontend**: http://localhost:5173
- **HTC Embedder**: http://localhost:5173/htc
- **Document Q&A**: http://localhost:5173/search-memory
- **System Dashboard**: http://localhost:5173/dashboard

### **3. Upload Sample Data**
```bash
# Copy sample CSV to upload
cp sample_data/sample_tenants.csv rag/uploads/csv/
```

### **4. Test the System**
1. Upload the sample CSV through HTC interface
2. Navigate to Document Q&A
3. Ask questions about the tenant data
4. View rich results with tenant metadata

## 🔧 Configuration

### **CSV Embedder Settings**
Edit `rag/loaders/csv_embedder.py`:
```python
# Configuration options
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
REQUIRED_COLUMNS = {'tenant_name'}
ALLOWED_EXTENSIONS = {'.csv'}
```

### **Query Settings**
Edit `rag/main.py`:
```python
# Query parameters
TOP_K = 5  # Number of results to return
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score
```

## 📈 Performance Tips

### **CSV Optimization**
- Use consistent date formats (YYYY-MM-DD)
- Clean data before uploading
- Remove unnecessary columns
- Keep file sizes under 10MB

### **Query Optimization**
- Be specific in questions
- Use tenant names when possible
- Ask about specific time periods
- Include unit numbers for precise results

## 🔒 Security Considerations

### **Data Protection**
- Local storage only
- No external API calls
- File validation and sanitization
- Access control through file system permissions

### **Privacy**
- Tenant data stays local
- No data transmission to external services
- Secure file handling
- Audit trail through logs

## 🎉 Benefits

### **For Property Managers**
- **Instant Search**: Find tenant information quickly
- **Natural Language**: Ask questions in plain English
- **Rich Context**: See complete tenant profiles
- **Automated Insights**: AI-generated summaries and analysis

### **For System Administrators**
- **Easy Integration**: Simple CSV upload process
- **Scalable Architecture**: Handles multiple files and tenants
- **Rich Metadata**: Comprehensive data tracking
- **Error Handling**: Robust validation and recovery

## 🔮 Future Enhancements

### **Advanced Features**
- **Email Notifications**: Automated lease expiry alerts
- **Report Generation**: AI-powered tenant reports
- **Data Analytics**: Revenue forecasting and occupancy optimization
- **Integration**: Connect with property management systems

### **AI Improvements**
- **Multi-language Support**: Query in different languages
- **Voice Interface**: Speech-to-text queries
- **Predictive Analytics**: Lease renewal predictions
- **Smart Recommendations**: Tenant management suggestions

## 🧪 Testing

### **Sample Queries to Try**
```bash
# Start the system
./start-tenant-sync.sh

# Upload sample data
curl -X POST http://localhost:8005/api/upload-csv \
  -F "file=@sample_data/sample_tenants.csv"

# Test queries
curl -X POST http://localhost:8005/api/query-simple \
  -H "Content-Type: application/json" \
  -d '{"query": "Which tenants have leases ending this month?"}'
```

The system is now ready for production use with real tenant data! 