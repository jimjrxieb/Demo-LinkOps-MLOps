import logging
import os
from http.client import HTTPException

import requests
from demo_db.db import save_ml_model
from jinja2 import Environment, FileSystemLoader

logging.basicConfig(level=logging.INFO)


def generate_model(model_name: str, purpose: str, algorithm: str, dataset: str):
    try:
        env = Environment(loader=FileSystemLoader("ml-creator/templates"))
        template_file = (
            "classification_model.py.jinja"
            if "predict" in purpose.lower()
            else "regression_model.py.jinja"
        )
        template = env.get_template(template_file)

        model_code = template.render(
            model_name=model_name, algorithm=algorithm, dataset=dataset, purpose=purpose
        )

        os.makedirs("demo-db/ml-models/models", exist_ok=True)
        model_path = f"demo-db/ml-models/models/{model_name}.py"
        with open(model_path, "w") as f:
            f.write(model_code)

        save_ml_model(
            model_name,
            {
                "data": {
                    "purpose": purpose,
                    "algorithm": algorithm,
                    "dataset": dataset,
                },
                "training_history": [],
            },
        )

        # Notify demo-jamesos for processing
        requests.post(
            "http://demo-jamesos:8003/rank_task",
            json={"task": model_name, "category": "ml_model", "model_path": model_path},
        )

        # Trigger demo-htc training
        requests.post(
            "http://demo-htc:8001/train",
            json={"model_name": model_name, "model_path": model_path},
        )

        logging.info(f"Generated ML model {model_name} at {model_path}")
        return {"model_name": model_name, "path": model_path}
    except Exception as e:
        logging.error(f"Model generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Model generation failed: {e}")
