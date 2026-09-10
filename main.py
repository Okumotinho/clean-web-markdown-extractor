from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import urllib.request
import re
from bs4 import BeautifulSoup

app = FastAPI(
    title="Clean Web Markdown Extractor API",
    description="Transforms noisy HTML into clean, token-efficient Markdown.",
    version="1.1.0"
)

class MarkdownResponse(BaseModel):
    url: str
    title: str
    markdown: str
    word_count: int

@app.get("/")
@app.get("/ping")
@app.get("/healthz")
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "markdown_extractor"}

def parse_html_tables(soup: BeautifulSoup) -> None:
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        md_rows = []
        for idx, row in enumerate(rows):
            cols = [c.get_text(strip=True) for c in row.find_all(["th", "td"])]
            if cols:
                md_rows.append("| " + " | ".join(cols) + " |")
                if idx == 0:
                    md_rows.append("| " + " | ".join(["---"] * len(cols)) + " |")
        if md_rows:
            table.replace_with("\n\n" + "\n".join(md_rows) + "\n\n")

@app.get("/extract", response_model=MarkdownResponse)
def extract_markdown(url: str = Query(..., description="Target webpage URL")):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "CleanMarkdownBot/1.1 (FastAPI; +https://rapidapi.com)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {str(e)}")

    soup = BeautifulSoup(html, "html.parser")
    
    # Strip bloat tags
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "aside", "svg", "form"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"

    # Prioritize main content containers if available
    main_content = soup.find("main") or soup.find("article") or soup.body or soup
    
    # Convert tables to markdown before text extraction
    parse_html_tables(main_content)

    body_text = main_content.get_text(separator="\n")
    cleaned_lines = [line.strip() for line in body_text.splitlines() if line.strip()]
    markdown = "\n\n".join(cleaned_lines)
    word_count = len(markdown.split())

    return MarkdownResponse(
        url=url,
        title=title,
        markdown=markdown,
        word_count=word_count
    )
