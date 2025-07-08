import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from logic.enhancer import enhance_content, enhance_metadata, enhance_quality
from logic.loopback import get_loopback_statistics, loopback_refine
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Whis Enhance Service",
    description="Content enhancement and quality improvement service for the Whis pipeline",
    version="1.0.0",
)


class EnhancementRequest(BaseModel):
    content_id: str
    content_type: str  # "text", "image", "audio", "video"
    content_data: Dict[str, Any]
    enhancement_type: str  # "quality", "metadata", "content"
    parameters: Optional[Dict[str, Any]] = None


class EnhancementResponse(BaseModel):
    content_id: str
    enhanced_content: Dict[str, Any]
    quality_score: float
    enhancement_metadata: Dict[str, Any]
    processing_time: float
    status: str


class BatchEnhancementRequest(BaseModel):
    items: List[EnhancementRequest]
    batch_id: Optional[str] = None


class BatchEnhancementResponse(BaseModel):
    batch_id: str
    results: List[EnhancementResponse]
    total_processed: int
    success_count: int
    failure_count: int


@app.post("/enhance", response_model=EnhancementResponse)
async def enhance_single_item(request: EnhancementRequest) -> EnhancementResponse:
    """
    Enhance a single content item with quality improvements, metadata enhancement, or content enhancement.
    """
    try:
        start_time = datetime.now()

        # Process enhancement based on type
        if request.enhancement_type == "quality":
            enhanced_data, quality_score = await enhance_quality(
                request.content_data, request.parameters or {}
            )
        elif request.enhancement_type == "metadata":
            enhanced_data, quality_score = await enhance_metadata(
                request.content_data, request.parameters or {}
            )
        elif request.enhancement_type == "content":
            enhanced_data, quality_score = await enhance_content(
                request.content_data, request.parameters or {}
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid enhancement type")

        processing_time = (datetime.now() - start_time).total_seconds()

        return EnhancementResponse(
            content_id=request.content_id,
            enhanced_content=enhanced_data,
            quality_score=quality_score,
            enhancement_metadata={
                "enhancement_type": request.enhancement_type,
                "content_type": request.content_type,
                "parameters_used": request.parameters or {},
                "timestamp": datetime.now().isoformat(),
            },
            processing_time=processing_time,
            status="completed",
        )

    except Exception as e:
        logger.error(f"Enhancement failed for content {request.content_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")


@app.post("/enhance/batch", response_model=BatchEnhancementResponse)
async def enhance_batch(
    request: BatchEnhancementRequest, background_tasks: BackgroundTasks
) -> BatchEnhancementResponse:
    """
    Enhance multiple content items in batch processing.
    """
    batch_id = request.batch_id or f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    results = []
    success_count = 0
    failure_count = 0

    for item in request.items:
        try:
            # Process each item
            if item.enhancement_type == "quality":
                enhanced_data, quality_score = await enhance_quality(
                    item.content_data, item.parameters or {}
                )
            elif item.enhancement_type == "metadata":
                enhanced_data, quality_score = await enhance_metadata(
                    item.content_data, item.parameters or {}
                )
            elif item.enhancement_type == "content":
                enhanced_data, quality_score = await enhance_content(
                    item.content_data, item.parameters or {}
                )
            else:
                raise ValueError("Invalid enhancement type")

            results.append(
                EnhancementResponse(
                    content_id=item.content_id,
                    enhanced_content=enhanced_data,
                    quality_score=quality_score,
                    enhancement_metadata={
                        "enhancement_type": item.enhancement_type,
                        "content_type": item.content_type,
                        "parameters_used": item.parameters or {},
                        "timestamp": datetime.now().isoformat(),
                    },
                    processing_time=0.0,  # Would calculate actual time in real implementation
                    status="completed",
                )
            )
            success_count += 1

        except Exception as e:
            logger.error(
                f"Batch enhancement failed for content {item.content_id}: {str(e)}"
            )
            failure_count += 1
            results.append(
                EnhancementResponse(
                    content_id=item.content_id,
                    enhanced_content={},
                    quality_score=0.0,
                    enhancement_metadata={"error": str(e)},
                    processing_time=0.0,
                    status="failed",
                )
            )

    return BatchEnhancementResponse(
        batch_id=batch_id,
        results=results,
        total_processed=len(request.items),
        success_count=success_count,
        failure_count=failure_count,
    )


@app.get("/enhance/quality/score")
async def get_quality_score(content_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Get quality score for content without performing enhancement.
    """
    try:
        _, quality_score = await enhance_quality(content_data, {})
        return {"quality_score": quality_score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quality scoring failed: {str(e)}")


@app.get("/enhance/metadata/analyze")
async def analyze_metadata(content_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze metadata without performing enhancement.
    """
    try:
        enhanced_data, _ = await enhance_metadata(content_data, {})
        return {"metadata_analysis": enhanced_data}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Metadata analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "whis-enhance",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "service": "Whis Enhance Service",
        "version": "1.0.0",
        "description": "Content enhancement and quality improvement service",
    }


@app.post("/loopback")
async def trigger_loopback(threshold: int = 2) -> Dict[str, Any]:
    """
    Trigger the loopback refinement process to improve runes based on repeated/failed tasks.

    Args:
        threshold: Minimum number of occurrences for a task to be considered repeated

    Returns:
        Summary of loopback refinement results
    """
    try:
        results = await loopback_refine(threshold)
        return {
            "status": "success",
            "message": f"Loopback refinement completed with {results.get('total_improvements', 0)} improvements",
            "results": results,
        }
    except Exception as e:
        logger.error(f"Loopback refinement failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Loopback refinement failed: {str(e)}"
        )


@app.get("/loopback/stats")
async def get_loopback_stats() -> Dict[str, Any]:
    """
    Get statistics about loopback processing and version control.

    Returns:
        Loopback and version control statistics
    """
    try:
        loopback_stats = get_loopback_statistics()
        return {"status": "success", "loopback_statistics": loopback_stats}
    except Exception as e:
        logger.error(f"Error getting loopback statistics: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error getting statistics: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
