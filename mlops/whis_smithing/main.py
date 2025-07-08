import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from logic.orb_generator import OrbGenerator, batch_generate_orbs, generate_orb
from logic.rune_generator import (RuneGenerator, batch_generate_runes,
                                  generate_rune)

app = FastAPI(
    title="Whis Smithing Service",
    description="Turns structured data into reusable knowledge assets (Orbs & Runes)",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize generators
orb_generator = OrbGenerator()
rune_generator = RuneGenerator()


class SmithingRequest(BaseModel):
    sanitized_data: Dict[str, Any]
    asset_type: str = "both"  # "orb", "rune", or "both"


class BatchSmithingRequest(BaseModel):
    sanitized_data_list: List[Dict[str, Any]]
    asset_type: str = "both"


class SmithingResponse(BaseModel):
    message: str
    processing_id: str
    generated_assets: Dict[str, Any]


@app.get("/")
async def root():
    return {
        "service": "whis_smithing",
        "status": "healthy",
        "version": "1.0.0",
        "description": "Turns structured data into reusable knowledge assets (Orbs & Runes)",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "whis_smithing",
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.post("/smith/orb")
async def create_orb(request: SmithingRequest):
    """
    Create an Orb (best practices) from sanitized data.
    """
    try:
        orb_data = generate_orb(request.sanitized_data)

        return SmithingResponse(
            message="Orb created successfully",
            processing_id=orb_data.get("id", str(uuid.uuid4())),
            generated_assets={"orb": orb_data},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orb creation failed: {str(e)}")


@app.post("/smith/rune")
async def create_rune(request: SmithingRequest):
    """
    Create a Rune (automation script) from sanitized data.
    """
    try:
        rune_data = generate_rune(request.sanitized_data)

        return SmithingResponse(
            message="Rune created successfully",
            processing_id=rune_data.get("id", str(uuid.uuid4())),
            generated_assets={"rune": rune_data},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rune creation failed: {str(e)}")


@app.post("/smith/both")
async def create_both_assets(request: SmithingRequest):
    """
    Create both Orb and Rune from sanitized data.
    """
    try:
        orb_data = generate_orb(request.sanitized_data)
        rune_data = generate_rune(request.sanitized_data)

        return SmithingResponse(
            message="Both assets created successfully",
            processing_id=str(uuid.uuid4()),
            generated_assets={"orb": orb_data, "rune": rune_data},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Asset creation failed: {str(e)}")


@app.post("/smith/batch")
async def create_batch_assets(request: BatchSmithingRequest):
    """
    Create assets from multiple sanitized data inputs.
    """
    try:
        batch_id = str(uuid.uuid4())
        generated_orbs = []
        generated_runes = []

        if request.asset_type in ["orb", "both"]:
            generated_orbs = batch_generate_orbs(request.sanitized_data_list)

        if request.asset_type in ["rune", "both"]:
            generated_runes = batch_generate_runes(request.sanitized_data_list)

        return {
            "message": f"Batch asset creation completed",
            "batch_id": batch_id,
            "total_inputs": len(request.sanitized_data_list),
            "orbs_created": len(generated_orbs),
            "runes_created": len(generated_runes),
            "generated_assets": {"orbs": generated_orbs, "runes": generated_runes},
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch creation failed: {str(e)}")


@app.get("/assets/orb/{orb_id}")
async def get_orb(orb_id: str):
    """
    Retrieve a specific Orb by ID.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/assets/rune/{rune_id}")
async def get_rune(rune_id: str):
    """
    Retrieve a specific Rune by ID.
    """
    # TODO: Implement retrieval from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/assets/orbs")
async def list_orbs(
    limit: int = 100,
    offset: int = 0,
    orb_type: Optional[str] = None,
    min_quality: Optional[float] = None,
):
    """
    List all Orbs with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/assets/runes")
async def list_runes(
    limit: int = 100,
    offset: int = 0,
    rune_type: Optional[str] = None,
    min_effectiveness: Optional[float] = None,
):
    """
    List all Runes with optional filtering.
    """
    # TODO: Implement listing from storage
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.get("/stats")
async def get_smithing_stats():
    """
    Get smithing service statistics.
    """
    return {
        "service": "whis_smithing",
        "total_orbs_created": 0,  # TODO: Implement actual stats
        "total_runes_created": 0,
        "average_orb_quality": 0.0,
        "average_rune_effectiveness": 0.0,
        "supported_orb_types": list(orb_generator.orb_templates.keys()),
        "supported_rune_types": list(rune_generator.rune_templates.keys()),
    }


@app.post("/test/orb")
async def test_orb_generation():
    """
    Test orb generation with sample data.
    """
    test_data = {
        "id": str(uuid.uuid4()),
        "type": "qna",
        "sanitized_content": "How do I deploy a Kubernetes deployment?",
        "tags": ["kubernetes", "deployment"],
        "timestamp": datetime.utcnow().isoformat(),
    }

    orb_data = generate_orb(test_data)

    return {
        "message": "Test orb generation completed",
        "test_data": test_data,
        "generated_orb": orb_data,
    }


@app.post("/test/rune")
async def test_rune_generation():
    """
    Test rune generation with sample data.
    """
    test_data = {
        "id": str(uuid.uuid4()),
        "type": "info_dump",
        "sanitized_content": "kubectl apply -f deployment.yaml",
        "tags": ["kubernetes", "deploy"],
        "timestamp": datetime.utcnow().isoformat(),
    }

    rune_data = generate_rune(test_data)

    return {
        "message": "Test rune generation completed",
        "test_data": test_data,
        "generated_rune": rune_data,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)
