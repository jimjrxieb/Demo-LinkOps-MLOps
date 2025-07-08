import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from logic.data_prep import (clean_data, feature_engineering, prepare_dataset,
                             validate_data)
from logic.model_eval import (compare_models, create_report, evaluate_model,
                              generate_metrics)
from logic.notebook_fixes import (fix_notebook, generate_documentation,
                                  optimize_code, validate_notebook)
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML Data Scientist AI Agent",
    description="AI agent for data preparation, model evaluation, and notebook optimization",
    version="1.0.0",
)


class DataPrepRequest(BaseModel):
    dataset_path: str
    task_type: str  # "classification", "regression", "clustering", "nlp"
    target_column: Optional[str] = None
    preprocessing_steps: Optional[List[str]] = None
    validation_split: float = 0.2
    random_state: int = 42


class ModelEvalRequest(BaseModel):
    model_path: str
    test_data_path: str
    evaluation_metrics: Optional[List[str]] = None
    comparison_models: Optional[List[str]] = None
    generate_plots: bool = True


class NotebookRequest(BaseModel):
    notebook_path: str
    action: str  # "fix", "optimize", "validate", "document"
    target_language: str = "python"
    optimization_level: str = "medium"  # "low", "medium", "high"


class DataPrepResponse(BaseModel):
    dataset_path: str
    task_type: str
    original_shape: List[int]
    processed_shape: List[int]
    features_engineered: int
    data_quality_score: float
    preprocessing_steps_applied: List[str]
    validation_split_applied: float
    output_path: str


class ModelEvalResponse(BaseModel):
    model_path: str
    test_data_path: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: Optional[float] = None
    confusion_matrix: List[List[int]]
    feature_importance: Dict[str, float]
    evaluation_report_path: str


class NotebookResponse(BaseModel):
    notebook_path: str
    action: str
    original_cells: int
    processed_cells: int
    issues_fixed: List[str]
    optimizations_applied: List[str]
    documentation_generated: bool
    output_path: str


@app.post("/data/prepare", response_model=DataPrepResponse)
async def prepare_dataset_endpoint(request: DataPrepRequest) -> DataPrepResponse:
    """
    Prepare and preprocess a dataset for machine learning.
    """
    try:
        result = await prepare_dataset(
            dataset_path=request.dataset_path,
            task_type=request.task_type,
            target_column=request.target_column,
            preprocessing_steps=request.preprocessing_steps or [],
            validation_split=request.validation_split,
            random_state=request.random_state,
        )

        return DataPrepResponse(
            dataset_path=request.dataset_path,
            task_type=request.task_type,
            original_shape=result["original_shape"],
            processed_shape=result["processed_shape"],
            features_engineered=result["features_engineered"],
            data_quality_score=result["data_quality_score"],
            preprocessing_steps_applied=result["preprocessing_steps_applied"],
            validation_split_applied=request.validation_split,
            output_path=result["output_path"],
        )

    except Exception as e:
        logger.error(f"Data preparation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Data preparation failed: {str(e)}"
        )


@app.post("/data/clean")
async def clean_dataset(
    dataset_path: str,
    cleaning_methods: List[str] = [
        "remove_duplicates",
        "handle_missing",
        "remove_outliers",
    ],
) -> Dict[str, Any]:
    """
    Clean a dataset by removing duplicates, handling missing values, and outliers.
    """
    try:
        result = await clean_data(dataset_path, cleaning_methods)
        return {
            "dataset_path": dataset_path,
            "cleaning_methods": cleaning_methods,
            "rows_before": result["rows_before"],
            "rows_after": result["rows_after"],
            "columns_cleaned": result["columns_cleaned"],
            "missing_values_handled": result["missing_values_handled"],
            "outliers_removed": result["outliers_removed"],
            "output_path": result["output_path"],
        }

    except Exception as e:
        logger.error(f"Data cleaning failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data cleaning failed: {str(e)}")


@app.post("/data/features")
async def engineer_features(
    dataset_path: str,
    feature_methods: List[str] = ["scaling", "encoding", "polynomial"],
) -> Dict[str, Any]:
    """
    Perform feature engineering on a dataset.
    """
    try:
        result = await feature_engineering(dataset_path, feature_methods)
        return {
            "dataset_path": dataset_path,
            "feature_methods": feature_methods,
            "original_features": result["original_features"],
            "engineered_features": result["engineered_features"],
            "total_features": result["total_features"],
            "feature_importance": result["feature_importance"],
            "output_path": result["output_path"],
        }

    except Exception as e:
        logger.error(f"Feature engineering failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Feature engineering failed: {str(e)}"
        )


@app.post("/data/validate")
async def validate_dataset_quality(
    dataset_path: str, validation_rules: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Validate dataset quality and integrity.
    """
    try:
        result = await validate_data(dataset_path, validation_rules or {})
        return {
            "dataset_path": dataset_path,
            "quality_score": result["quality_score"],
            "validation_passed": result["validation_passed"],
            "issues_found": result["issues_found"],
            "recommendations": result["recommendations"],
            "validation_report": result["validation_report"],
        }

    except Exception as e:
        logger.error(f"Data validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Data validation failed: {str(e)}")


@app.post("/model/evaluate", response_model=ModelEvalResponse)
async def evaluate_model_endpoint(request: ModelEvalRequest) -> ModelEvalResponse:
    """
    Evaluate a machine learning model performance.
    """
    try:
        result = await evaluate_model(
            model_path=request.model_path,
            test_data_path=request.test_data_path,
            evaluation_metrics=request.evaluation_metrics
            or ["accuracy", "precision", "recall", "f1"],
            generate_plots=request.generate_plots,
        )

        return ModelEvalResponse(
            model_path=request.model_path,
            test_data_path=request.test_data_path,
            accuracy=result["accuracy"],
            precision=result["precision"],
            recall=result["recall"],
            f1_score=result["f1_score"],
            roc_auc=result.get("roc_auc"),
            confusion_matrix=result["confusion_matrix"],
            feature_importance=result["feature_importance"],
            evaluation_report_path=result["evaluation_report_path"],
        )

    except Exception as e:
        logger.error(f"Model evaluation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Model evaluation failed: {str(e)}"
        )


@app.post("/model/compare")
async def compare_multiple_models(
    model_paths: List[str],
    test_data_path: str,
    comparison_metrics: List[str] = ["accuracy", "precision", "recall", "f1"],
) -> Dict[str, Any]:
    """
    Compare multiple machine learning models.
    """
    try:
        result = await compare_models(
            model_paths=model_paths,
            test_data_path=test_data_path,
            comparison_metrics=comparison_metrics,
        )

        return {
            "model_paths": model_paths,
            "test_data_path": test_data_path,
            "comparison_results": result["comparison_results"],
            "best_model": result["best_model"],
            "comparison_plot_path": result.get("comparison_plot_path"),
            "detailed_report_path": result["detailed_report_path"],
        }

    except Exception as e:
        logger.error(f"Model comparison failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Model comparison failed: {str(e)}"
        )


@app.post("/model/metrics")
async def generate_comprehensive_metrics(
    model_path: str, test_data_path: str, include_advanced_metrics: bool = True
) -> Dict[str, Any]:
    """
    Generate comprehensive model evaluation metrics.
    """
    try:
        result = await generate_metrics(
            model_path=model_path,
            test_data_path=test_data_path,
            include_advanced_metrics=include_advanced_metrics,
        )

        return {
            "model_path": model_path,
            "test_data_path": test_data_path,
            "basic_metrics": result["basic_metrics"],
            "advanced_metrics": result.get("advanced_metrics", {}),
            "classification_report": result.get("classification_report"),
            "metrics_plot_path": result.get("metrics_plot_path"),
        }

    except Exception as e:
        logger.error(f"Metrics generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Metrics generation failed: {str(e)}"
        )


@app.post("/model/report")
async def create_model_evaluation_report(
    model_path: str,
    test_data_path: str,
    report_format: str = "html",  # "html", "pdf", "markdown"
) -> Dict[str, Any]:
    """
    Create a comprehensive model evaluation report.
    """
    try:
        result = await create_report(
            model_path=model_path,
            test_data_path=test_data_path,
            report_format=report_format,
        )

        return {
            "model_path": model_path,
            "test_data_path": test_data_path,
            "report_format": report_format,
            "report_path": result["report_path"],
            "report_url": result.get("report_url"),
        }

    except Exception as e:
        logger.error(f"Report creation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Report creation failed: {str(e)}")


@app.post("/notebook/fix", response_model=NotebookResponse)
async def fix_notebook_endpoint(request: NotebookRequest) -> NotebookResponse:
    """
    Fix common issues in Jupyter notebooks.
    """
    try:
        result = await fix_notebook(
            notebook_path=request.notebook_path, target_language=request.target_language
        )

        return NotebookResponse(
            notebook_path=request.notebook_path,
            action=request.action,
            original_cells=result["original_cells"],
            processed_cells=result["processed_cells"],
            issues_fixed=result["issues_fixed"],
            optimizations_applied=[],
            documentation_generated=False,
            output_path=result["output_path"],
        )

    except Exception as e:
        logger.error(f"Notebook fixing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Notebook fixing failed: {str(e)}")


@app.post("/notebook/optimize")
async def optimize_notebook_code(
    notebook_path: str, optimization_level: str = "medium"
) -> Dict[str, Any]:
    """
    Optimize code in Jupyter notebooks for better performance.
    """
    try:
        result = await optimize_code(notebook_path, optimization_level)
        return {
            "notebook_path": notebook_path,
            "optimization_level": optimization_level,
            "original_cells": result["original_cells"],
            "optimized_cells": result["optimized_cells"],
            "optimizations_applied": result["optimizations_applied"],
            "performance_improvement": result["performance_improvement"],
            "output_path": result["output_path"],
        }

    except Exception as e:
        logger.error(f"Notebook optimization failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Notebook optimization failed: {str(e)}"
        )


@app.post("/notebook/validate")
async def validate_notebook_structure(notebook_path: str) -> Dict[str, Any]:
    """
    Validate notebook structure and code quality.
    """
    try:
        result = await validate_notebook(notebook_path)
        return {
            "notebook_path": notebook_path,
            "is_valid": result["is_valid"],
            "validation_score": result["validation_score"],
            "issues_found": result["issues_found"],
            "recommendations": result["recommendations"],
            "structure_analysis": result["structure_analysis"],
        }

    except Exception as e:
        logger.error(f"Notebook validation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Notebook validation failed: {str(e)}"
        )


@app.post("/notebook/document")
async def generate_notebook_documentation(
    notebook_path: str,
    documentation_format: str = "markdown",  # "markdown", "html", "pdf"
) -> Dict[str, Any]:
    """
    Generate documentation for a Jupyter notebook.
    """
    try:
        result = await generate_documentation(notebook_path, documentation_format)
        return {
            "notebook_path": notebook_path,
            "documentation_format": documentation_format,
            "documentation_path": result["documentation_path"],
            "sections_generated": result["sections_generated"],
            "code_examples": result["code_examples"],
            "documentation_url": result.get("documentation_url"),
        }

    except Exception as e:
        logger.error(f"Documentation generation failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Documentation generation failed: {str(e)}"
        )


@app.get("/ml/dashboard")
async def get_ml_dashboard() -> Dict[str, Any]:
    """
    Get ML dashboard with overview metrics.
    """
    try:
        return {
            "datasets_processed": 15,
            "models_trained": 8,
            "models_deployed": 3,
            "average_accuracy": 87.5,
            "active_experiments": 2,
            "notebooks_optimized": 12,
            "last_model_evaluation": datetime.now().isoformat(),
            "data_quality_score": 92.3,
        }

    except Exception as e:
        logger.error(f"Failed to get ML dashboard: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get ML dashboard: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "ml-data-scientist",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "agent": "ML Data Scientist AI Agent",
        "version": "1.0.0",
        "capabilities": [
            "Data Preparation",
            "Model Evaluation",
            "Notebook Optimization",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
