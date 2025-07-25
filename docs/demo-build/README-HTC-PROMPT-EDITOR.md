# HTC Prompt Editor - No-Code AI Customization

This document describes the **HTC Prompt Editor** system that enables property managers to customize how the AI understands their domain-specific terminology through a no-code interface.

## 🎯 Overview

The HTC Prompt Editor gives property managers their own **Grammarly-style keyword editor** that allows them to:

- **Define domain terms** and their variations
- **Customize AI understanding** of property management terminology
- **Improve search accuracy** by teaching the AI synonyms and variations
- **No technical knowledge required** - completely visual interface
- **Instant integration** with the MultiQueryRetriever for better RAG results

## 🔄 How It Works

```
Property Manager → Defines Terms → AI Keywords → Prompt Template → MultiQueryRetriever → Better Search Results
```

### **Key Components**

1. **Prompt Editor UI** (`frontend/src/views/HTCPromptEditor.vue`)
   - Visual interface for defining terms and variations
   - Category organization and validation
   - Real-time preview and statistics

2. **Prompt Editor API** (`htc/routes/prompt_editor.py`)
   - RESTful endpoints for managing keywords
   - Automatic prompt template generation
   - Statistics and analytics

3. **Prompt Template Builder** (`htc/prompt_template_builder.py`)
   - Converts custom terms into AI prompt templates
   - Supports both basic and enhanced prompt formats
   - File management and validation

4. **Integration with MultiQueryRetriever**
   - Custom prompts automatically used by search engine
   - Improved query understanding and rephrasing
   - Better document retrieval results

## 🚀 Key Features

### **For Property Managers**
- **Visual Term Editor**: Drag-and-drop style interface for defining terms
- **Category Organization**: Organize terms by property management categories
- **Real-time Validation**: Immediate feedback on term definitions
- **Preview Functionality**: See how terms will be used before saving
- **Statistics Dashboard**: Track how many terms and variations are defined

### **For System Administrators**
- **Automatic Integration**: Custom terms work immediately with existing RAG system
- **File-based Storage**: Simple JSON storage for easy backup and migration
- **Prompt Template Generation**: Automatic creation of AI prompt templates
- **Backup and Restore**: Easy to backup and restore custom terminology

### **For Developers**
- **Extensible Architecture**: Easy to add new categories and term types
- **API-First Design**: RESTful endpoints for integration
- **Validation System**: Comprehensive input validation and error handling
- **Statistics API**: Detailed analytics about term usage

## 🔧 Technical Implementation

### **1. Term Definition System**

#### **Term Structure**
```json
{
  "term": "delinquency",
  "variations": ["late rent", "rent not paid", "overdue payment", "payment delinquency"],
  "category": "rent_payment",
  "description": "Terms related to unpaid or late rent"
}
```

#### **Available Categories**
- `rent_payment`: Rent collection and payments
- `lease_management`: Lease agreements and renewals
- `maintenance`: Property maintenance and repairs
- `tenant_communication`: Tenant interactions
- `legal`: Legal matters and compliance
- `financial`: Financial operations and accounting
- `property_operations`: Day-to-day property management
- `other`: Terms that don't fit other categories

### **2. Prompt Template Generation**

#### **Basic Prompt Template**
```txt
You are an AI assistant helping generate diverse rephrasings of a user's question to improve document retrieval from a property management knowledge base.

🔄 Use these known term variations:
- "delinquency" → late rent, rent not paid, overdue payment, payment delinquency
- "eviction" → lease termination, notice to vacate, removal, expulsion

When rephrasing a query, generate 4 alternate versions using synonyms or domain-aware variations.

Format:
User Question: {question}

Alternate Rephrasings:
1.
2.
3.
4.
```

#### **Enhanced Prompt Template**
```txt
You are an AI assistant specialized in property management query understanding and rephrasing.
Your goal is to generate diverse, semantically equivalent rephrasings of user questions to improve document retrieval.

🔄 Domain-Specific Term Variations:

📂 Rent Payment:
  - "delinquency" → late rent, rent not paid, overdue payment, payment delinquency

📂 Legal & Compliance:
  - "eviction" → lease termination, notice to vacate, removal, expulsion

🎯 Rephrasing Guidelines:
1. Use domain-specific synonyms and variations
2. Maintain the original intent and context
3. Consider different ways users might phrase the same question
4. Include both formal and informal variations
5. Account for regional or company-specific terminology

📝 Output Format:
User Question: {question}

Alternate Rephrasings:
1. [First variation using domain terms]
2. [Second variation with different synonyms]
3. [Third variation with alternative phrasing]
4. [Fourth variation considering context]
```

### **3. API Endpoints**

#### **Core Endpoints**
```python
# Update custom keywords
POST /api/htc/prompt/keywords
{
    "terms": [
        {
            "term": "delinquency",
            "variations": ["late rent", "rent not paid"],
            "category": "rent_payment",
            "description": "Terms related to unpaid rent"
        }
    ]
}

# Get current keywords
GET /api/htc/prompt/keywords

# Get prompt template
GET /api/htc/prompt/template

# Get statistics
GET /api/htc/prompt/stats

# Clear all keywords
DELETE /api/htc/prompt/keywords
```

#### **Response Examples**
```json
{
    "status": "success",
    "terms_count": 5,
    "total_variations": 20,
    "prompt_file": "prompts/query_rewrite_prompt.txt",
    "terms_file": "htc/prompt_terms.json"
}
```

### **4. UI Components**

#### **Term Editor Interface**
- **Domain Term Input**: Text field for the main term
- **Variations Textarea**: Comma-separated list of variations
- **Category Dropdown**: Select from predefined categories
- **Description Field**: Optional description of the term
- **Preview Section**: Shows how the term will be formatted
- **Validation**: Real-time error checking and feedback

#### **Dashboard Features**
- **Statistics Cards**: Total terms, variations, categories
- **Term List**: All defined terms with edit/delete options
- **Category Filter**: Filter terms by category
- **Save/Reset**: Save changes or reset to defaults
- **Usage Examples**: Before/after examples of AI behavior

## 🎯 Usage Examples

### **Property Management Scenarios**

#### **Scenario 1: Rent Payment Terms**
```
Term: "delinquency"
Variations: "late rent", "rent not paid", "overdue payment", "payment delinquency", "past due"
Category: rent_payment
Description: Terms related to unpaid or late rent

Result: When someone asks "Who has late rent?", the AI also searches for "delinquency", "overdue payment", etc.
```

#### **Scenario 2: Maintenance Terms**
```
Term: "maintenance request"
Variations: "repair request", "service request", "work order", "fix request", "maintenance ticket"
Category: maintenance
Description: Terms related to property maintenance and repairs

Result: When someone asks "How do I submit a repair request?", the AI understands it's about maintenance requests.
```

#### **Scenario 3: Legal Terms**
```
Term: "eviction"
Variations: "lease termination", "notice to vacate", "removal", "expulsion", "legal removal"
Category: legal
Description: Terms related to tenant removal from property

Result: When someone asks about "lease termination", the AI includes eviction-related documents in search.
```

### **Before vs After Examples**

#### **Before Custom Terms**
```
User asks: "Who has late rent?"
AI searches for: "late rent" only
Misses: Documents about "delinquency" or "overdue payments"
```

#### **After Custom Terms**
```
User asks: "Who has late rent?"
AI searches for: "late rent", "delinquency", "overdue payments", "rent not paid", "payment delinquency"
Finds: All relevant documents regardless of terminology used
```

## 📊 Performance Impact

### **Search Accuracy Improvements**
- **Broader Coverage**: AI finds documents using different terminology
- **Synonym Recognition**: Understands equivalent terms automatically
- **Context Awareness**: Better understanding of domain-specific language
- **Reduced False Negatives**: Fewer missed relevant documents

### **User Experience Benefits**
- **Natural Language**: Users can ask questions in their own terms
- **Consistent Results**: Same results regardless of terminology used
- **Faster Answers**: Better search means faster, more relevant responses
- **Reduced Frustration**: No need to guess the "right" words to use

## 🔧 Configuration

### **File Storage**
```python
# Terms storage
TERMS_FILE = Path("htc/prompt_terms.json")

# Prompt template storage
PROMPT_FILE = Path("prompts/query_rewrite_prompt.txt")

# Directory structure
htc/
├── prompt_terms.json          # Custom terms and variations
└── routes/
    └── prompt_editor.py       # API routes

prompts/
└── query_rewrite_prompt.txt   # Generated prompt template
```

### **Validation Rules**
- **Term Name**: Minimum 2 characters, required
- **Variations**: At least 1 variation, maximum 10 variations
- **Category**: Must be from predefined list
- **Description**: Optional, for documentation

### **Integration Points**
- **MultiQueryRetriever**: Automatically uses custom prompts
- **RAG Search**: Improved document retrieval
- **Feedback System**: Can be combined with feedback loop
- **Training System**: Custom terms can be used in model training

## 🚀 Getting Started

### **1. Access the Prompt Editor**
1. Navigate to **AI Keywords** in the sidebar
2. Click **Add Term** to start defining your terminology
3. Fill in the term, variations, and category
4. Click **Save Keywords** to apply changes

### **2. Define Your Terms**
```bash
# Example workflow
1. Add term: "delinquency"
2. Add variations: "late rent", "rent not paid", "overdue payment"
3. Select category: "rent_payment"
4. Add description: "Terms related to unpaid or late rent"
5. Save and test
```

### **3. Test the Improvements**
```bash
# Test with different phrasings
"Who has late rent?" → Should find delinquency documents
"How many overdue payments?" → Should find delinquency documents
"List all rent not paid cases" → Should find delinquency documents
```

### **4. Monitor Performance**
- Check statistics in the UI
- Review search results quality
- Adjust terms based on usage patterns
- Add new terms as needed

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Terms Not Working**
```
Issue: Custom terms not improving search results
Solution: Check that terms are saved and prompt template is generated
```

#### **2. Too Many Variations**
```
Issue: Error about maximum variations
Solution: Reduce variations to 10 or fewer per term
```

#### **3. Invalid Categories**
```
Issue: Category not recognized
Solution: Use only predefined categories from the dropdown
```

#### **4. Terms Not Saving**
```
Issue: Changes not persisting
Solution: Check file permissions and ensure proper save
```

### **Best Practices**

#### **Term Definition**
- **Be Specific**: Use clear, unambiguous terms
- **Include Variations**: Add common synonyms and phrasings
- **Use Categories**: Organize terms logically
- **Test Thoroughly**: Verify terms work with actual queries

#### **Maintenance**
- **Regular Updates**: Add new terms as terminology evolves
- **Remove Obsolete**: Delete terms that are no longer used
- **Monitor Usage**: Track which terms are most effective
- **Backup Regularly**: Export terms for safekeeping

## 🎉 Benefits Summary

### **For Property Managers**
- **Customized AI**: AI understands your specific terminology
- **Better Search**: Find documents regardless of how questions are phrased
- **No Technical Skills**: Visual interface requires no coding
- **Immediate Results**: Changes take effect instantly

### **For System Administrators**
- **Easy Management**: Simple file-based storage
- **Automatic Integration**: Works with existing RAG system
- **Backup Friendly**: Easy to backup and restore
- **Scalable**: Can handle hundreds of terms and variations

### **For Developers**
- **Extensible Design**: Easy to add new features
- **API-First**: RESTful endpoints for integration
- **Validation Built-in**: Comprehensive input validation
- **Statistics Available**: Detailed usage analytics

The HTC Prompt Editor transforms your AI from a generic assistant into a **domain-expert assistant** that speaks your language and understands your terminology, all through a simple no-code interface that property managers can use without any technical knowledge. 