from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import logging
from datetime import datetime
from logic.scraper import (
    scrape_url,
    scrape_multiple_urls,
    extract_content,
    validate_url,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Whis WebScraper Service",
    description="Web scraping and content extraction service for the Whis pipeline",
    version="1.0.0",
)


class ScrapingRequest(BaseModel):
    url: str
    content_type: Optional[str] = "all"  # "text", "images", "links", "all"
    depth: Optional[int] = 1
    timeout: Optional[int] = 30
    user_agent: Optional[str] = None
    follow_redirects: Optional[bool] = True


class ScrapingResponse(BaseModel):
    url: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    status: str
    processing_time: float
    error_message: Optional[str] = None


class BatchScrapingRequest(BaseModel):
    urls: List[str]
    content_type: Optional[str] = "all"
    depth: Optional[int] = 1
    timeout: Optional[int] = 30
    batch_id: Optional[str] = None


class BatchScrapingResponse(BaseModel):
    batch_id: str
    results: List[ScrapingResponse]
    total_processed: int
    success_count: int
    failure_count: int


class ContentExtractionRequest(BaseModel):
    html_content: str
    extraction_type: str  # "text", "images", "links", "metadata"
    selectors: Optional[Dict[str, str]] = None


class ContentExtractionResponse(BaseModel):
    extracted_content: Dict[str, Any]
    extraction_type: str
    processing_time: float
    status: str


@app.post("/scrape", response_model=ScrapingResponse)
async def scrape_single_url(request: ScrapingRequest) -> ScrapingResponse:
    """
    Scrape a single URL and extract content.
    """
    try:
        start_time = datetime.now()

        # Validate URL
        if not await validate_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid URL format")

        # Perform scraping
        content, metadata = await scrape_url(
            url=request.url,
            content_type=request.content_type,
            depth=request.depth,
            timeout=request.timeout,
            user_agent=request.user_agent,
            follow_redirects=request.follow_redirects,
        )

        processing_time = (datetime.now() - start_time).total_seconds()

        return ScrapingResponse(
            url=request.url,
            content=content,
            metadata=metadata,
            status="completed",
            processing_time=processing_time,
        )

    except Exception as e:
        logger.error(f"Scraping failed for URL {request.url}: {str(e)}")
        return ScrapingResponse(
            url=request.url,
            content={},
            metadata={},
            status="failed",
            processing_time=0.0,
            error_message=str(e),
        )


@app.post("/scrape/batch", response_model=BatchScrapingResponse)
async def scrape_multiple_urls_endpoint(
    request: BatchScrapingRequest, background_tasks: BackgroundTasks
) -> BatchScrapingResponse:
    """
    Scrape multiple URLs in batch processing.
    """
    batch_id = request.batch_id or f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    results = []
    success_count = 0
    failure_count = 0

    for url in request.urls:
        try:
            # Validate URL
            if not await validate_url(url):
                results.append(
                    ScrapingResponse(
                        url=url,
                        content={},
                        metadata={},
                        status="failed",
                        processing_time=0.0,
                        error_message="Invalid URL format",
                    )
                )
                failure_count += 1
                continue

            # Perform scraping
            content, metadata = await scrape_url(
                url=url,
                content_type=request.content_type,
                depth=request.depth,
                timeout=request.timeout,
            )

            results.append(
                ScrapingResponse(
                    url=url,
                    content=content,
                    metadata=metadata,
                    status="completed",
                    processing_time=0.0,  # Would calculate actual time in real implementation
                )
            )
            success_count += 1

        except Exception as e:
            logger.error(f"Batch scraping failed for URL {url}: {str(e)}")
            failure_count += 1
            results.append(
                ScrapingResponse(
                    url=url,
                    content={},
                    metadata={},
                    status="failed",
                    processing_time=0.0,
                    error_message=str(e),
                )
            )

    return BatchScrapingResponse(
        batch_id=batch_id,
        results=results,
        total_processed=len(request.urls),
        success_count=success_count,
        failure_count=failure_count,
    )


@app.post("/extract", response_model=ContentExtractionResponse)
async def extract_content_from_html(
    request: ContentExtractionRequest,
) -> ContentExtractionResponse:
    """
    Extract specific content from HTML using selectors or default extraction.
    """
    try:
        start_time = datetime.now()

        extracted_content = await extract_content(
            html_content=request.html_content,
            extraction_type=request.extraction_type,
            selectors=request.selectors or {},
        )

        processing_time = (datetime.now() - start_time).total_seconds()

        return ContentExtractionResponse(
            extracted_content=extracted_content,
            extraction_type=request.extraction_type,
            processing_time=processing_time,
            status="completed",
        )

    except Exception as e:
        logger.error(f"Content extraction failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Content extraction failed: {str(e)}"
        )


@app.get("/scrape/status/{url:path}")
async def get_scraping_status(url: str) -> Dict[str, Any]:
    """
    Get the status of a scraping operation for a specific URL.
    """
    try:
        # In a real implementation, this would check a job queue or database
        return {
            "url": url,
            "status": "completed",  # Placeholder
            "last_checked": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@app.get("/scrape/validate")
async def validate_url_endpoint(url: str) -> Dict[str, bool]:
    """
    Validate if a URL is accessible and can be scraped.
    """
    try:
        is_valid = await validate_url(url)
        return {"url": url, "valid": is_valid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL validation failed: {str(e)}")


@app.get("/scrape/robots/{domain}")
async def get_robots_txt(domain: str) -> Dict[str, Any]:
    """
    Get robots.txt content for a domain.
    """
    try:
        # In real implementation, would fetch and parse robots.txt
        return {
            "domain": domain,
            "robots_content": "User-agent: *\nAllow: /",  # Placeholder
            "crawl_delay": 1,
            "disallowed_paths": [],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Robots.txt fetch failed: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "whis-webscraper",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "service": "Whis WebScraper Service",
        "version": "1.0.0",
        "description": "Web scraping and content extraction service",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
