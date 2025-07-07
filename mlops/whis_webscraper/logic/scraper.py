"""
Web scraping logic for the Whis pipeline.
Handles URL scraping, content extraction, and validation.
"""

import asyncio
import re
import json
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
import logging
from urllib.parse import urlparse, urljoin
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def scrape_url(
    url: str,
    content_type: str = "all",
    depth: int = 1,
    timeout: int = 30,
    user_agent: Optional[str] = None,
    follow_redirects: bool = True,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Scrape a single URL and extract content.

    Args:
        url: The URL to scrape
        content_type: Type of content to extract ("text", "images", "links", "all")
        depth: Depth of scraping (1 = single page, 2+ = follow links)
        timeout: Request timeout in seconds
        user_agent: Custom user agent string
        follow_redirects: Whether to follow redirects

    Returns:
        Tuple of (content, metadata)
    """
    try:
        # Default user agent
        if not user_agent:
            user_agent = "Whis-WebScraper/1.0"

        # Headers for the request
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout), headers=headers
        ) as session:
            async with session.get(url, allow_redirects=follow_redirects) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {response.reason}")

                html_content = await response.text()

                # Parse HTML
                soup = BeautifulSoup(html_content, "html.parser")

                # Extract content based on type
                content = {}
                if content_type in ["text", "all"]:
                    content["text"] = await _extract_text(soup)

                if content_type in ["images", "all"]:
                    content["images"] = await _extract_images(soup, url)

                if content_type in ["links", "all"]:
                    content["links"] = await _extract_links(soup, url)

                if content_type in ["metadata", "all"]:
                    content["metadata"] = await _extract_metadata(soup)

                # Generate metadata
                metadata = {
                    "url": url,
                    "status_code": response.status,
                    "content_type": response.headers.get("content-type", ""),
                    "content_length": len(html_content),
                    "scraped_at": datetime.now().isoformat(),
                    "user_agent": user_agent,
                    "depth": depth,
                    "follow_redirects": follow_redirects,
                }

                return content, metadata

    except Exception as e:
        logger.error(f"Scraping failed for URL {url}: {str(e)}")
        raise


async def scrape_multiple_urls(
    urls: List[str],
    content_type: str = "all",
    depth: int = 1,
    timeout: int = 30,
    max_concurrent: int = 5,
) -> List[Tuple[str, Dict[str, Any], Dict[str, Any]]]:
    """
    Scrape multiple URLs concurrently.

    Args:
        urls: List of URLs to scrape
        content_type: Type of content to extract
        depth: Depth of scraping
        timeout: Request timeout in seconds
        max_concurrent: Maximum concurrent requests

    Returns:
        List of tuples (url, content, metadata)
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def scrape_with_semaphore(url: str):
        async with semaphore:
            try:
                content, metadata = await scrape_url(url, content_type, depth, timeout)
                return url, content, metadata
            except Exception as e:
                logger.error(f"Failed to scrape {url}: {str(e)}")
                return url, {}, {"error": str(e)}

    tasks = [scrape_with_semaphore(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


async def extract_content(
    html_content: str, extraction_type: str, selectors: Dict[str, str]
) -> Dict[str, Any]:
    """
    Extract specific content from HTML using selectors or default extraction.

    Args:
        html_content: Raw HTML content
        extraction_type: Type of extraction ("text", "images", "links", "metadata")
        selectors: Custom CSS selectors for extraction

    Returns:
        Extracted content dictionary
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")

        if extraction_type == "text":
            return await _extract_text_with_selectors(soup, selectors)
        elif extraction_type == "images":
            return await _extract_images_with_selectors(soup, selectors)
        elif extraction_type == "links":
            return await _extract_links_with_selectors(soup, selectors)
        elif extraction_type == "metadata":
            return await _extract_metadata_with_selectors(soup, selectors)
        else:
            raise ValueError(f"Unsupported extraction type: {extraction_type}")

    except Exception as e:
        logger.error(f"Content extraction failed: {str(e)}")
        raise


async def validate_url(url: str) -> bool:
    """
    Validate if a URL is properly formatted and accessible.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid, False otherwise
    """
    try:
        # Basic URL format validation
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False

        # Check if it's a supported scheme
        if parsed.scheme not in ["http", "https"]:
            return False

        # Basic accessibility check (HEAD request)
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=10) as response:
                return response.status < 400

    except Exception:
        return False


# Helper functions for content extraction
async def _extract_text(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract text content from HTML."""
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text content
    text = soup.get_text()

    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = " ".join(chunk for chunk in chunks if chunk)

    # Extract headings
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        headings.append({"level": tag.name, "text": tag.get_text().strip()})

    # Extract paragraphs
    paragraphs = []
    for p in soup.find_all("p"):
        text_content = p.get_text().strip()
        if text_content:
            paragraphs.append(text_content)

    return {
        "full_text": text,
        "headings": headings,
        "paragraphs": paragraphs,
        "word_count": len(text.split()),
        "character_count": len(text),
    }


async def _extract_images(soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
    """Extract image information from HTML."""
    images = []

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src:
            # Make relative URLs absolute
            if not src.startswith(("http://", "https://")):
                src = urljoin(base_url, src)

            images.append(
                {
                    "src": src,
                    "alt": img.get("alt", ""),
                    "title": img.get("title", ""),
                    "width": img.get("width", ""),
                    "height": img.get("height", ""),
                    "class": img.get("class", []),
                }
            )

    return images


async def _extract_links(soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
    """Extract link information from HTML."""
    links = []

    for link in soup.find_all("a", href=True):
        href = link.get("href")
        if href:
            # Make relative URLs absolute
            if not href.startswith(("http://", "https://")):
                href = urljoin(base_url, href)

            links.append(
                {
                    "href": href,
                    "text": link.get_text().strip(),
                    "title": link.get("title", ""),
                    "rel": link.get("rel", []),
                    "target": link.get("target", ""),
                }
            )

    return links


async def _extract_metadata(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract metadata from HTML."""
    metadata = {}

    # Title
    title_tag = soup.find("title")
    if title_tag:
        metadata["title"] = title_tag.get_text().strip()

    # Meta tags
    for meta in soup.find_all("meta"):
        name = meta.get("name") or meta.get("property")
        content = meta.get("content")
        if name and content:
            metadata[name] = content

    # Open Graph tags
    og_tags = {}
    for meta in soup.find_all("meta", property=re.compile(r"^og:")):
        property_name = meta.get("property", "").replace("og:", "")
        content = meta.get("content")
        if property_name and content:
            og_tags[property_name] = content
    if og_tags:
        metadata["open_graph"] = og_tags

    # Twitter Card tags
    twitter_tags = {}
    for meta in soup.find_all("meta", attrs={"name": re.compile(r"^twitter:")}):
        name = meta.get("name", "").replace("twitter:", "")
        content = meta.get("content")
        if name and content:
            twitter_tags[name] = content
    if twitter_tags:
        metadata["twitter_card"] = twitter_tags

    # Structured data (JSON-LD)
    json_ld = []
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.get_text())
            json_ld.append(data)
        except json.JSONDecodeError:
            continue
    if json_ld:
        metadata["structured_data"] = json_ld

    return metadata


# Helper functions for selector-based extraction
async def _extract_text_with_selectors(
    soup: BeautifulSoup, selectors: Dict[str, str]
) -> Dict[str, Any]:
    """Extract text using custom CSS selectors."""
    extracted = {}

    for key, selector in selectors.items():
        elements = soup.select(selector)
        if elements:
            extracted[key] = [elem.get_text().strip() for elem in elements]
        else:
            extracted[key] = []

    return extracted


async def _extract_images_with_selectors(
    soup: BeautifulSoup, selectors: Dict[str, str]
) -> Dict[str, Any]:
    """Extract images using custom CSS selectors."""
    extracted = {}

    for key, selector in selectors.items():
        elements = soup.select(selector)
        images = []
        for elem in elements:
            if elem.name == "img":
                images.append(
                    {
                        "src": elem.get("src", ""),
                        "alt": elem.get("alt", ""),
                        "title": elem.get("title", ""),
                    }
                )
        extracted[key] = images

    return extracted


async def _extract_links_with_selectors(
    soup: BeautifulSoup, selectors: Dict[str, str]
) -> Dict[str, Any]:
    """Extract links using custom CSS selectors."""
    extracted = {}

    for key, selector in selectors.items():
        elements = soup.select(selector)
        links = []
        for elem in elements:
            if elem.name == "a" and elem.get("href"):
                links.append(
                    {
                        "href": elem.get("href"),
                        "text": elem.get_text().strip(),
                        "title": elem.get("title", ""),
                    }
                )
        extracted[key] = links

    return extracted


async def _extract_metadata_with_selectors(
    soup: BeautifulSoup, selectors: Dict[str, str]
) -> Dict[str, Any]:
    """Extract metadata using custom CSS selectors."""
    extracted = {}

    for key, selector in selectors.items():
        elements = soup.select(selector)
        if elements:
            extracted[key] = [elem.get_text().strip() for elem in elements]
        else:
            extracted[key] = []

    return extracted
