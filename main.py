from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import urllib.request
import re
from bs4 import BeautifulSoup

app = FastAPI(
    title="Clean Web Markdown Extractor API",
    description="Transforms noisy HTML into clean, token-efficient Markdown.",
    version="1.0.0"
)

class MarkdownResponse(BaseModel):
    url: str
    title: str
    markdown: str
    word_count: int

@app.get("/ping")
@app.get("/healthz")
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "markdown_extractor"}

@app.get("/extract", response_model=MarkdownResponse)
def extract_markdown(url: str = Query(..., description="Target webpage URL")):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CleanMarkdownBot/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
    body_text = soup.get_text(separator="\n")
    cleaned_lines = [line.strip() for line in body_text.splitlines() if line.strip()]
    markdown = "\n\n".join(cleaned_lines)
    word_count = len(markdown.split())

    return MarkdownResponse(
        url=url,
        title=title,
        markdown=markdown,
        word_count=word_count
    )
