# ML Creator - DEMO-LinkOps

The `ml-creator/` module enables non-data scientists to create ML models and AI agents for the DEMO-LinkOps platform, integrated with demo-jamesos (your Jarvis-like AI).

## Features
- **ML Model Creation**: Use a GUI to define model purpose (e.g., "predict customer churn"), select algorithms (e.g., RandomForest), and upload `.csv` datasets.
- **AI Agent Creation**: Create agents (e.g., backlog scanners) that execute via demo-jamesos, sending reports to email/Confluence.
- **Integration**: Models are saved to `demo-db/ml-models/models/`, trained in `demo-htc/mlm-repo/`, and indexed by `demo-rag/`. Agents leverage `demo-jamesos/pipeline/`.

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables in `env.template`:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   JIRA_API_TOKEN=your_jira_token
   OPENAI_API_KEY=your_openai_key
   ```
3. Run: `docker-compose up demo-ml-creator-service`

## Usage
- **Create Model**: Go to `http://localhost:8080/ml-creator`, enter model details, and upload a dataset. Models are saved and trained in `demo-htc/`.
- **Create Agent**: Go to `http://localhost:8080/agent-creator`, specify agent name, Jira URL, and email. Agents run via demo-jamesos.
- **Train Model**: Use `http://localhost:8080/demo-htc` to train models with Q&A data.

## Example
- **Model**: Create a churn prediction model, saved to `demo-db/ml-models/models/churn_predictor.py`.
- **Agent**: Create a backlog scanner, executed via `demo-jamesos/pipeline/`, with reports emailed to your manager.

## Integration Points
- **demo-db**: PostgreSQL database for storing model metadata
- **demo-rag**: Vector database for indexing models and agents
- **demo-jamesos**: AI assistant for task execution and ranking
- **demo-htc**: Training environment for ML models
- **demo-client-audits**: For Confluence integration

## Development
- **Frontend**: Vue.js components in `frontend/src/components/`
- **Backend**: FastAPI service with Jinja2 templates
- **CI/CD**: GitHub Actions workflow for automated testing
- **Docker**: Containerized deployment with docker-compose 