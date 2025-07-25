# HTC Feedback Loop + Local Learning

This document describes the **HTC Feedback Loop** system that enables property managers to correct AI answers and retrain the model locally, creating a closed-loop system for continuous improvement.

## 🎯 Overview

The HTC Feedback Loop transforms the RAG system from a static AI into a **learning system** that improves over time based on real user feedback. Property managers can now:

- **Correct AI mistakes** through an intuitive interface
- **Provide better answers** for future queries
- **Train the model locally** without internet connectivity
- **Track improvement** through feedback statistics
- **Maintain data privacy** with all processing done locally

## 🔄 Feedback Loop Architecture

```
User Query → AI Answer → User Correction → Feedback Storage → Local Training → Improved Model
     ↑                                                                              ↓
     └─────────────────────── Better Future Answers ←──────────────────────────────┘
```

### **Key Components**

1. **Feedback Collector** (`htc/feedback_collector.py`)
   - Logs user corrections and feedback
   - Manages feedback metadata and categorization
   - Builds training datasets from feedback

2. **Feedback API** (`htc/routes/feedback.py`)
   - RESTful endpoints for feedback management
   - Statistics and analytics
   - Dataset generation for training

3. **Feedback UI** (`frontend/src/views/HTCFeedback.vue`)
   - Intuitive interface for submitting corrections
   - Feedback history and statistics
   - Category filtering and management

4. **LoRA Trainer** (`htc/train_lora.py`)
   - Local model fine-tuning using feedback data
   - LoRA (Low-Rank Adaptation) for efficient training
   - Offline training without internet dependency

## 🚀 Key Features

### **For Property Managers**
- **Easy Correction Interface**: Simple form to correct AI answers
- **Feedback Categories**: Categorize issues (incorrect, incomplete, wrong context, etc.)
- **Training Tracking**: See which feedback has been used for training
- **Improvement Metrics**: Track how the AI improves over time

### **For System Administrators**
- **Local Training**: All training happens offline
- **Data Privacy**: No data leaves the local system
- **Configurable Training**: Adjust training parameters as needed
- **Fallback Support**: Graceful handling when training dependencies aren't available

### **For Developers**
- **Extensible Architecture**: Easy to add new feedback types
- **Comprehensive API**: Full CRUD operations for feedback
- **Training Integration**: Seamless integration with existing RAG system
- **Monitoring**: Detailed logging and status tracking

## 🔧 Technical Implementation

### **1. Feedback Collection System**

#### **Feedback Collector** (`htc/feedback_collector.py`)
```python
class FeedbackCollector:
    def log_feedback(
        self,
        query: str,
        generated_answer: str,
        expected_answer: str,
        context: str = "",
        category: str = "incorrect_answer",
        user_notes: str = "",
        tenant_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Log feedback for AI answer correction."""
        
        # Generate unique feedback ID
        feedback_id = self._generate_feedback_id(query, timestamp)
        
        # Create feedback entry with metadata
        entry = {
            "feedback_id": feedback_id,
            "timestamp": timestamp.isoformat(),
            "query": query,
            "generated_answer": generated_answer,
            "expected_answer": expected_answer,
            "context": context,
            "category": category,
            "user_notes": user_notes,
            "tenant_data": tenant_data or {},
            "status": "pending_training",
            "training_round": 0
        }
        
        # Save to JSON file
        self._save_feedback_entry(entry)
        return entry
```

#### **Feedback Categories**
- `incorrect_answer`: AI provided wrong information
- `incomplete_answer`: AI missed important details
- `wrong_context`: AI used irrelevant context
- `missing_information`: AI didn't include required info
- `unclear_response`: AI's answer was confusing
- `other`: Other issues not covered above

### **2. Feedback API Endpoints**

#### **Core Endpoints**
```python
# Submit feedback
POST /api/htc/feedback
{
    "query": "When is rent due?",
    "answer": "Rent is due on the 1st.",
    "expected": "Rent is due on the 1st with a 5-day grace period.",
    "category": "incomplete_answer",
    "user_notes": "Missing grace period information"
}

# Get feedback entries
GET /api/htc/feedback?limit=50&category=incorrect_answer

# Get feedback statistics
GET /api/htc/feedback/stats

# Build training dataset
POST /api/htc/feedback/build-dataset

# Update feedback status
PUT /api/htc/feedback/{feedback_id}/status?status=trained
```

#### **Response Examples**
```json
{
    "total_feedback": 25,
    "pending_training": 15,
    "trained": 10,
    "recent_feedback": 5,
    "categories": {
        "incorrect_answer": 8,
        "incomplete_answer": 12,
        "wrong_context": 3,
        "other": 2
    }
}
```

### **3. Feedback UI Components**

#### **Feedback Form**
- **Original Question**: The user's original query
- **AI's Answer**: The incorrect/incomplete AI response
- **Correct Answer**: What the answer should be
- **Context**: Additional context that was used
- **Category**: Type of issue (dropdown)
- **Notes**: Additional comments from user

#### **Feedback Dashboard**
- **Statistics Cards**: Total feedback, pending training, trained, recent
- **Feedback List**: All feedback entries with filtering
- **Category Filter**: Filter by feedback type
- **Status Tracking**: See which feedback has been used for training

### **4. LoRA Training System**

#### **Training Configuration**
```python
TRAINING_CONFIG = {
    "lora_r": 8,                    # LoRA rank
    "lora_alpha": 32,               # LoRA alpha parameter
    "lora_dropout": 0.1,            # LoRA dropout
    "learning_rate": 2e-4,          # Learning rate
    "num_epochs": 3,                # Number of training epochs
    "batch_size": 4,                # Batch size
    "max_length": 512,              # Maximum sequence length
    "warmup_steps": 100,            # Warmup steps
    "save_steps": 50,               # Save checkpoint every N steps
}
```

#### **Training Process**
1. **Data Preparation**: Convert feedback to training format
2. **Model Loading**: Load base Mistral model
3. **LoRA Configuration**: Apply LoRA adapters
4. **Training**: Fine-tune on feedback data
5. **Model Saving**: Save improved model
6. **Status Update**: Mark feedback as trained

## 🎯 Usage Examples

### **Property Management Scenarios**

#### **Scenario 1: Rent Payment Policy**
```
User Query: "When is rent considered late?"
AI Answer: "Rent is due on the 1st of each month."
User Correction: "Rent is due on the 1st of each month, with a 5-day grace period. After the 5th, a $50 late fee applies."
Category: incomplete_answer
Notes: "Missing grace period and late fee information"
```

#### **Scenario 2: Lease Renewal Process**
```
User Query: "How do I renew my lease?"
AI Answer: "Contact the property manager."
User Correction: "Submit a lease renewal form 60 days before expiration. Forms are available in the office or online portal. Processing takes 5-7 business days."
Category: incomplete_answer
Notes: "Need specific process details and timeline"
```

#### **Scenario 3: Maintenance Requests**
```
User Query: "What's the emergency maintenance number?"
AI Answer: "Call the office during business hours."
User Correction: "Emergency maintenance: 555-EMERGE (555-363-743). Available 24/7 for urgent issues like water leaks, heating failures, or security problems."
Category: incorrect_answer
Notes: "Wrong answer - emergency number needed, not office hours"
```

### **Training Workflow**

#### **Step 1: Collect Feedback**
```bash
# Property manager corrects AI answers through the UI
# Feedback is automatically logged to htc/feedback/
```

#### **Step 2: Review Feedback**
```bash
# Check feedback statistics
curl http://localhost:8000/api/htc/feedback/stats

# View pending training feedback
curl http://localhost:8000/api/htc/feedback?status=pending_training
```

#### **Step 3: Build Training Dataset**
```bash
# Generate training dataset from feedback
curl -X POST http://localhost:8000/api/htc/feedback/build-dataset
```

#### **Step 4: Train Model**
```bash
# Run LoRA training
cd htc
python train_lora.py
```

#### **Step 5: Verify Improvement**
```bash
# Test the improved model with similar queries
# Check if answers are now more accurate
```

## 📊 Performance Metrics

### **Feedback Collection**
- **Total Feedback**: Number of corrections submitted
- **Feedback Categories**: Distribution of issue types
- **Recent Activity**: Feedback submitted in last 7 days
- **Training Status**: How much feedback has been used for training

### **Training Performance**
- **Training Time**: How long training takes
- **Model Loss**: Training loss reduction
- **Examples Used**: Number of feedback examples in training
- **Training Rounds**: How many times the model has been updated

### **Improvement Tracking**
- **Answer Quality**: Reduction in similar errors
- **User Satisfaction**: Fewer corrections needed over time
- **Response Completeness**: More comprehensive answers
- **Context Accuracy**: Better context selection

## 🔧 Configuration

### **Feedback Storage**
```python
# Feedback directory
LOG_DIR = Path("htc/feedback/")

# Feedback file format
{
    "feedback_id": "feedback_20241201_143022_abc12345",
    "timestamp": "2024-12-01T14:30:22",
    "query": "When is rent due?",
    "generated_answer": "Rent is due on the 1st.",
    "expected_answer": "Rent is due on the 1st with a 5-day grace period.",
    "category": "incomplete_answer",
    "status": "pending_training"
}
```

### **Training Configuration**
```python
# LoRA training parameters
TRAINING_CONFIG = {
    "lora_r": 8,                    # LoRA rank (higher = more parameters)
    "lora_alpha": 32,               # LoRA alpha (scaling factor)
    "lora_dropout": 0.1,            # Dropout for regularization
    "learning_rate": 2e-4,          # Learning rate
    "num_epochs": 3,                # Training epochs
    "batch_size": 4,                # Batch size
    "max_length": 512,              # Maximum sequence length
}
```

### **API Configuration**
```python
# Feedback API endpoints
FEEDBACK_ENDPOINTS = {
    "submit": "/api/htc/feedback",
    "list": "/api/htc/feedback",
    "stats": "/api/htc/feedback/stats",
    "build_dataset": "/api/htc/feedback/build-dataset",
    "update_status": "/api/htc/feedback/{id}/status"
}
```

## 🚀 Getting Started

### **1. Setup Feedback System**
```bash
# Navigate to project directory
cd DEMO-LinkOps

# Create feedback directories
mkdir -p htc/feedback
mkdir -p htc/lora_models

# Install dependencies (if needed)
pip install transformers peft torch
```

### **2. Start Services**
```bash
# Start RAG service with feedback endpoints
cd rag
python main.py

# Start frontend
cd ../frontend
npm run dev
```

### **3. Collect Feedback**
1. Navigate to **AI Feedback** in the sidebar
2. Click **Add Feedback**
3. Fill in the correction form
4. Submit feedback

### **4. Train Model**
```bash
# Build training dataset
curl -X POST http://localhost:8000/api/htc/feedback/build-dataset

# Run training
cd htc
python train_lora.py
```

### **5. Monitor Progress**
- Check feedback statistics in the UI
- Review training logs in `htc/lora_models/`
- Test improved model with similar queries

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Training Dependencies Missing**
```
Error: Missing training dependencies
Solution: pip install transformers peft torch
```

#### **2. Model File Not Found**
```
Error: Model file not found
Solution: Ensure mistral.gguf exists in llm_weights/
```

#### **3. Insufficient Training Data**
```
Warning: Very few training examples
Solution: Collect more feedback before training
```

#### **4. Training Takes Too Long**
```
Issue: Training is slow
Solution: Reduce batch_size, num_epochs, or use GPU
```

### **Performance Optimization**

#### **Training Speed**
- Use GPU if available (`torch.cuda.is_available()`)
- Reduce batch size for memory constraints
- Use fewer epochs for quick iterations

#### **Model Quality**
- Increase LoRA rank for more parameters
- Use more training examples
- Adjust learning rate based on loss curves

#### **Storage Management**
- Clean up old feedback entries periodically
- Limit saved model checkpoints
- Compress training datasets

## 🎉 Benefits Summary

### **For Property Managers**
- **Continuous Improvement**: AI gets better with each correction
- **Domain Expertise**: Model learns property management specifics
- **Faster Responses**: More accurate answers reduce follow-up questions
- **Data Privacy**: All training happens locally

### **For System Administrators**
- **Offline Operation**: No internet required for training
- **Scalable Architecture**: Easy to add new feedback types
- **Monitoring**: Comprehensive tracking of improvements
- **Backup/Restore**: Simple file-based storage

### **For Developers**
- **Extensible Design**: Easy to customize for different domains
- **API-First**: RESTful endpoints for integration
- **Comprehensive Logging**: Detailed debugging information
- **Fallback Support**: Graceful degradation when dependencies missing

The HTC Feedback Loop transforms your RAG system from a static AI into a **learning assistant** that continuously improves based on real user feedback, all while maintaining complete data privacy and offline operation. 