# MLOps Utils - Toolbox

A collection of CLI utilities and helper functions for MLOps operations.

## 🛠️ Tools

### `format_yaml.py`
Format and validate YAML files.

```bash
# Format a single file
python tools/format_yaml.py config.yaml

# Validate only (don't format)
python tools/format_yaml.py config.yaml --validate-only

# Process directory recursively
python tools/format_yaml.py ./helm/ --recursive
```

### `convert_csv_to_json.py`
Convert between CSV and JSON formats.

```bash
# CSV to JSON
python tools/convert_csv_to_json.py data.csv --output data.json

# JSON to CSV
python tools/convert_csv_to_json.py data.json --reverse --output data.csv

# CSV to JSON with dict format
python tools/convert_csv_to_json.py data.csv --format dict
```

### `extract_metadata.py`
Extract metadata from Git repositories, Dockerfiles, and general repository insights.

```bash
# Extract all metadata
python tools/extract_metadata.py /path/to/repo --all

# Git metadata only
python tools/extract_metadata.py /path/to/repo --git

# Dockerfile analysis
python tools/extract_metadata.py /path/to/repo --dockerfile Dockerfile

# Repository insights
python tools/extract_metadata.py /path/to/repo --insights
```

### `run_pipeline.py`
Execute MLOps pipelines defined in JSON configuration.

```bash
# Run pipeline
python tools/run_pipeline.py pipeline.json

# Dry run (show config without executing)
python tools/run_pipeline.py pipeline.json --dry-run

# Save results to file
python tools/run_pipeline.py pipeline.json --output results.json
```

## 🚀 CLI Wrapper

Use the unified CLI wrapper for all tools:

```bash
# Install Google Fire
pip install fire

# Use CLI wrapper
python cli.py format_yaml --path ./helm/chart.yaml
python cli.py convert_csv data.csv --output data.json
python cli.py extract_metadata . --all
python cli.py run_pipeline pipeline.json
```

## 📋 Pipeline Configuration

Example pipeline configuration (`pipeline.json`):

```json
{
  "name": "MLOps Deployment Pipeline",
  "steps": [
    {
      "name": "validate_yaml",
      "type": "validation",
      "validation_type": "json_valid",
      "file_path": "config.json"
    },
    {
      "name": "build_image",
      "type": "command",
      "command": "docker build -t myapp .",
      "cwd": "./app",
      "timeout": 600
    },
    {
      "name": "deploy",
      "type": "script",
      "script": "deploy.py",
      "args": ["--env", "production"],
      "depends_on": ["build_image"]
    }
  ]
}
```

## 🐳 Docker Usage

```bash
# Build the utils image
docker build -t mlops-utils .

# Run a tool
docker run --rm -v $(pwd):/workspace mlops-utils format_yaml config.yaml

# Run CLI wrapper
docker run --rm -v $(pwd):/workspace mlops-utils cli format_yaml --path config.yaml
``` 