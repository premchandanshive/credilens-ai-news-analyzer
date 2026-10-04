"""
CrediLens — Content Extraction Service
Extracts clean article text and metadata from URLs and uploaded documents.
"""

import io
import re
import httpx
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from backend.app.core.errors import InvalidInputException, PayloadTooLargeException

# Limits
MAX_ARTICLE_CHARS = 50000
MAX_FILE_BYTES = 5 * 1024 * 1024  # 5 MB

async def extract_from_url(url: str, timeout: float = 12.0) -> Dict[str, Any]:
    """
    Fetch and extract article content and metadata from a web URL.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise InvalidInputException("URL must start with http:// or https://")
    
    # SSRF protection: block local/private network ranges
    hostname = parsed.hostname or ""
    if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1") or hostname.startswith("192.168.") or hostname.startswith("10."):
        raise InvalidInputException("Access to local network resources is disallowed.")

    domain = hostname.replace("www.", "")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 CrediLensBot/1.0"
    }

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers=headers) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                raise InvalidInputException(f"Failed to retrieve URL (HTTP {resp.status_code})")
            
            html_content = resp.text
    except httpx.TimeoutException:
        raise InvalidInputException("The URL request timed out. The server may be unreachable.")
    except Exception as e:
        raise InvalidInputException(f"Could not fetch article from URL: {str(e)}")

    # 1. Primary extraction with trafilatura
    extracted_text = None
    extracted_title = None
    extracted_author = None
    extracted_date = None

    try:
        import trafilatura
        extracted_text = trafilatura.extract(html_content, include_comments=False, include_tables=False)
        metadata = trafilatura.extract_metadata(html_content)
        if metadata:
            extracted_title = metadata.title
            extracted_author = metadata.author
            extracted_date = metadata.date
    except Exception as e:
        print(f"[Extraction] Trafilatura extraction note: {e}")

    # 2. Fallback to BeautifulSoup if trafilatura extracted insufficient text
    if not extracted_text or len(extracted_text.strip()) < 50:
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        if not extracted_title and soup.title:
            extracted_title = soup.title.get_text().strip()

        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if len(p.get_text().strip()) > 20]
        extracted_text = "\n\n".join(paragraphs)

    if not extracted_text or len(extracted_text.strip()) < 30:
        raise InvalidInputException("Could not extract meaningful article text from this URL.")

    # Truncate to maximum characters
    final_text = extracted_text.strip()[:MAX_ARTICLE_CHARS]
    final_title = extracted_title or domain or "Article"

    return {
        "title": final_title,
        "text": final_text,
        "author": extracted_author,
        "date": extracted_date,
        "domain": domain
    }

def extract_from_file(filename: str, content_bytes: bytes) -> Dict[str, Any]:
    """
    Extract plain text from uploaded files (.txt, .md, .pdf).
    """
    if len(content_bytes) > MAX_FILE_BYTES:
        raise PayloadTooLargeException("Uploaded file exceeds the 5MB size limit.")

    lower_name = filename.lower()
    
    if lower_name.endswith(".txt") or lower_name.endswith(".md"):
        try:
            text = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                text = content_bytes.decode("latin-1")
            except Exception:
                raise InvalidInputException("Failed to decode text file. Please ensure UTF-8 encoding.")
    elif lower_name.endswith(".pdf"):
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(content_bytes))
            text_pages = [page.extract_text() for page in reader.pages if page.extract_text()]
            text = "\n\n".join(text_pages)
        except Exception:
            # Fallback simple string extraction for text in PDF
            raw_text = content_bytes.decode("ascii", errors="ignore")
            text = re.sub(r'[\x00-\x1f]+', ' ', raw_text)
    else:
        raise InvalidInputException("Unsupported file type. Supported formats: .txt, .md, .pdf")

    cleaned = text.strip()
    if len(cleaned) < 10:
        raise InvalidInputException("Uploaded document contains insufficient readable text.")

    # Derive title from filename or first line
    first_line = cleaned.split("\n")[0].strip()
    title = first_line[:120] if len(first_line) > 10 else filename

    return {
        "title": title,
        "text": cleaned[:MAX_ARTICLE_CHARS]
    }
