# Agent Creator

A FastAPI-based service for generating AI agents and taskbots using Jinja2 templates.

## 🚀 Features

- **Agent Generation**: Create various types of AI agents (base, taskbot, commandbot, assistant, workflow)
- **Security Controls**: Configurable security levels and input validation
- **Template System**: Jinja2-based templates for customizable agent generation
- **Workflow Support**: Generate workflow orchestration agents
- **Tool Integration**: Support for various tools and capabilities
- **RESTful API**: Clean REST API with comprehensive documentation

## 📁 Structure

```
agent-creator/
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # This file
├── logic/
│   └── agent_generator.py  # Core generation logic
├── templates/
│   ├── base_agent.py.jinja
│   ├── taskbot.py.jinja
│   ├── commandbot.py.jinja
│   ├── assistant.py.jinja
│   └── workflow.py.jinja
└── api/
    └── __init__.py
```

## 🛠️ Installation

### Local Development

```bash
# Clone the repository
cd ml-models/agent-creator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Docker

```bash
# Build the image
docker build -t agent-creator .

# Run the container
docker run -p 8001:8001 agent-creator
```

## 📚 API Endpoints

### Health Check
```bash
GET /health
```

### Generate Agent
```bash
POST /generate-agent/
```

**Parameters:**
- `agent_type` (str): Type of agent (base, taskbot, commandbot, assistant, workflow)
- `agent_name` (str): Name for the agent
- `tools` (str, optional): Comma-separated list of tools/commands
- `capabilities` (str, optional): Comma-separated list of capabilities
- `security_level` (str, optional): Security level (low, medium, high)
- `description` (str, optional): Agent description

**Example:**
```bash
curl -X POST "http://localhost:8001/generate-agent/" \
  -F "agent_type=commandbot" \
  -F "agent_name=SecureShell" \
  -F "tools=ls,pwd,whoami,echo" \
  -F "capabilities=command_execution,security_validation" \
  -F "security_level=high"
```

### Generate Workflow Agent
```bash
POST /generate-workflow-agent/
```

**Parameters:**
- `workflow_name` (str): Name for the workflow
- `steps` (str): JSON string defining workflow steps
- `triggers` (str, optional): Comma-separated list of triggers
- `error_handling` (str, optional): Error handling strategy (retry, skip, stop)

**Example:**
```bash
curl -X POST "http://localhost:8001/generate-workflow-agent/" \
  -F "workflow_name=DataPipeline" \
  -F "steps=[{\"step\": \"extract\", \"action\": \"read_data\"}, {\"step\": \"transform\", \"action\": \"process_data\"}]" \
  -F "triggers=schedule,manual" \
  -F "error_handling=retry"
```

### Get Supported Agents
```bash
GET /supported-agents
```

### Get Agent Templates
```bash
GET /agent-templates
```

### Validate Agent Configuration
```bash
POST /validate-agent/
```

## 🎯 Supported Agent Types

### Base Agent
Basic agent template with minimal functionality.

**Use Cases:**
- Simple automation
- Learning and prototyping
- Basic task handling

### TaskBot
Task-oriented agent for handling specific tasks.

**Use Cases:**
- Data processing
- File operations
- API interactions

**Example Tools:**
- pandas, numpy, requests, json, csv, datetime

### CommandBot
Command execution agent with security controls.

**Use Cases:**
- System administration
- DevOps automation
- Shell scripting

**Example Commands:**
- ls, pwd, whoami, echo, cat, grep, find

### Assistant
AI assistant agent with conversation capabilities.

**Use Cases:**
- Customer support
- Information retrieval
- Conversational AI

**Example Capabilities:**
- search, calculate, format, translate, summarize

### Workflow
Workflow orchestration agent.

**Use Cases:**
- Pipeline automation
- Process orchestration
- Multi-step tasks

**Example Capabilities:**
- validate, execute, monitor, notify, rollback

## 🔒 Security Levels

### Low Security
- No input validation
- No output sanitization
- No command whitelist
- 30-second timeout
- 3 retries

### Medium Security (Default)
- Input validation enabled
- Output sanitization enabled
- Command whitelist enabled
- 60-second timeout
- 2 retries

### High Security
- Strict input validation
- Comprehensive output sanitization
- Strict command whitelist
- 120-second timeout
- 1 retry

## 📊 Example Usage

### Generate a CommandBot

```python
import requests

# Generate commandbot
response = requests.post(
    "http://localhost:8001/generate-agent/",
    data={
        "agent_type": "commandbot",
        "agent_name": "SecureShell",
        "tools": "ls,pwd,whoami,echo,cat,grep",
        "capabilities": "command_execution,security_validation",
        "security_level": "high"
    }
)

result = response.json()
print(f"Agent generated: {result['output_path']}")
print(f"Agent code:\n{result['agent_code']}")
```

### Generate a Workflow Agent

```python
import requests
import json

# Define workflow steps
steps = [
    {"step": "extract", "action": "read_data", "params": {"source": "input.csv"}},
    {"step": "transform", "action": "process_data", "params": {"transformations": ["clean", "validate"]}},
    {"step": "load", "action": "save", "params": {"destination": "output.csv"}}
]

# Generate workflow agent
response = requests.post(
    "http://localhost:8001/generate-workflow-agent/",
    data={
        "workflow_name": "DataPipeline",
        "steps": json.dumps(steps),
        "triggers": "schedule,manual,event",
        "error_handling": "retry"
    }
)

result = response.json()
print(f"Workflow agent generated: {result['output_path']}")
```

## 🔧 Configuration

The service can be configured using environment variables:

- `ENVIRONMENT`: Set to "demo" for demo mode
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `TEMPLATE_DIR`: Custom template directory path

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8001/health

# Test agent generation
curl -X POST "http://localhost:8001/generate-agent/" \
  -F "agent_type=base" \
  -F "agent_name=TestAgent"

# Test workflow generation
curl -X POST "http://localhost:8001/generate-workflow-agent/" \
  -F "workflow_name=TestWorkflow" \
  -F "steps=[{\"step\": \"test\", \"action\": \"execute\"}]"

# Get supported agents
curl http://localhost:8001/supported-agents
```

## 📈 Monitoring

The service includes health checks and logging:

- Health endpoint: `GET /health`
- Logs are written to stdout/stderr
- Docker health checks are configured

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Update tests if needed
5. Submit a pull request

## 📄 License

This project is part of the LinkOps platform. 