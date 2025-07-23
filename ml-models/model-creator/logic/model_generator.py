import os
import tempfile
import uuid

from jinja2 import Environment, FileSystemLoader

# Get template directory
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def generate_model_code(
    model_type: str, target_column: str, algorithm: str = "auto", data_path: str = None
) -> str:
    """
    Generate ML model code using Jinja2 templates.

    Args:
        model_type: Type of model (classification, regression, clustering, time_series)
        target_column: Name of the target column
        algorithm: ML algorithm to use
        data_path: Path to the data file

    Returns:
        Path to the generated model file
    """
    try:
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

        # Map model types to template names
        template_mapping = {
            "classification": "classification_model.py.jinja",
            "regression": "regression_model.py.jinja",
            "clustering": "clustering_model.py.jinja",
            "time_series": "time_series_model.py.jinja",
        }

        template_name = template_mapping.get(
            model_type, "classification_model.py.jinja"
        )
        template = env.get_template(template_name)

        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f"generated_{model_type}_{algorithm}_{unique_id}.py"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)

        # Render template with context
        context = {
            "target_column": target_column,
            "algorithm": algorithm,
            "data_path": data_path or "/tmp/sample_data.csv",
            "model_type": model_type,
        }

        rendered_code = template.render(**context)

        # Write generated code to file
        with open(output_path, "w") as f:
            f.write(rendered_code)

        return output_path

    except Exception as e:
        raise Exception(f"Failed to generate model code: {str(e)}")


def generate_agent_code(
    agent_type: str, capabilities: list, model_type: str = "classification"
) -> str:
    """
    Generate AI agent code using Jinja2 templates.

    Args:
        agent_type: Type of agent (task_evaluator, data_analyzer, model_trainer, pipeline_orchestrator)
        capabilities: List of agent capabilities
        model_type: Type of model the agent will work with

    Returns:
        Path to the generated agent file
    """
    try:
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

        # Map agent types to template names
        template_mapping = {
            "task_evaluator": "task_evaluator_agent.py.jinja",
            "data_analyzer": "data_analyzer_agent.py.jinja",
            "model_trainer": "model_trainer_agent.py.jinja",
            "pipeline_orchestrator": "pipeline_orchestrator_agent.py.jinja",
        }

        template_name = template_mapping.get(
            agent_type, "task_evaluator_agent.py.jinja"
        )
        template = env.get_template(template_name)

        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f"generated_{agent_type}_{unique_id}.py"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)

        # Render template with context
        context = {
            "agent_type": agent_type,
            "capabilities": capabilities,
            "model_type": model_type,
            "capabilities_str": ", ".join(capabilities),
        }

        rendered_code = template.render(**context)

        # Write generated code to file
        with open(output_path, "w") as f:
            f.write(rendered_code)

        return output_path

    except Exception as e:
        raise Exception(f"Failed to generate agent code: {str(e)}")


def get_available_algorithms(model_type: str) -> list:
    """Get available algorithms for a given model type."""
    algorithms = {
        "classification": [
            "random_forest",
            "svm",
            "neural_network",
            "logistic_regression",
            "decision_tree",
            "gradient_boosting",
            "naive_bayes",
            "knn",
        ],
        "regression": [
            "linear_regression",
            "random_forest",
            "neural_network",
            "xgboost",
            "gradient_boosting",
            "svr",
            "ridge",
            "lasso",
        ],
        "clustering": [
            "kmeans",
            "dbscan",
            "hierarchical",
            "gaussian_mixture",
            "spectral",
            "agglomerative",
        ],
        "time_series": [
            "arima",
            "lstm",
            "prophet",
            "exponential_smoothing",
            "sarima",
            "var",
        ],
    }

    return algorithms.get(model_type, [])


def validate_model_parameters(
    model_type: str, algorithm: str, target_column: str
) -> bool:
    """Validate model generation parameters."""
    if not model_type:
        raise ValueError("Model type is required")

    if not target_column:
        raise ValueError("Target column is required")

    available_algorithms = get_available_algorithms(model_type)
    if algorithm != "auto" and algorithm not in available_algorithms:
        raise ValueError(
            f"Algorithm '{algorithm}' not supported for model type '{model_type}'"
        )

    return True


def get_model_metadata(model_type: str, algorithm: str) -> dict:
    """Get metadata about the model type and algorithm."""
    metadata = {
        "classification": {
            "description": "Predicts categorical outcomes",
            "metrics": ["accuracy", "precision", "recall", "f1_score"],
            "use_cases": [
                "spam detection",
                "image classification",
                "sentiment analysis",
            ],
        },
        "regression": {
            "description": "Predicts continuous values",
            "metrics": ["mse", "mae", "r2_score", "rmse"],
            "use_cases": ["price prediction", "sales forecasting", "risk assessment"],
        },
        "clustering": {
            "description": "Groups similar data points",
            "metrics": [
                "silhouette_score",
                "calinski_harabasz_score",
                "davies_bouldin_score",
            ],
            "use_cases": [
                "customer segmentation",
                "anomaly detection",
                "market research",
            ],
        },
        "time_series": {
            "description": "Predicts future values based on temporal patterns",
            "metrics": ["mae", "rmse", "mape", "smape"],
            "use_cases": ["stock prediction", "weather forecasting", "demand planning"],
        },
    }

    return metadata.get(model_type, {})
