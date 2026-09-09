# 🌐 Clean Web Markdown Extractor API

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![RapidAPI Hub](https://img.shields.io/badge/RapidAPI-Live-0052CC.svg)](https://rapidapi.com/Okumotinho/api/clean-web-markdown-extractor)

> High-performance micro-API converting noisy web pages into clean, token-efficient, LLM-ready Markdown.

---

## ⚡ Why Clean Web Markdown Extractor?

When building AI agents, RAG pipelines, or web scrapers, raw HTML clutters your context window with scripts, advertisements, tracking tags, and style sheets. This wastes tokens, slows down inference, and introduces hallucinations.

**Clean Web Markdown Extractor** solves this by:
- 🧹 Stripping `<script>`, `<style>`, `<nav>`, `<footer>`, and advertisement containers.
- 📄 Preserving semantic markdown hierarchy (`#`, `##`, `*`, `[links]`).
- ⚡ Sub-second response time optimized for high-throughput concurrency.
- 💰 Token efficiency: reduces HTML token footprint by up to **85%**.

---

## 🚀 Quick Start & Usage Examples

### 1. cURL
```bash
curl -X GET "https://clean-web-markdown-extractor.onrender.com/extract?url=https://example.com" \
  -H "Accept: application/json"
```

### 2. Python (Requests)
```python
import requests

url = "https://clean-web-markdown-extractor.onrender.com/extract"
params = {"url": "https://news.ycombinator.com"}

response = requests.get(url, params=params)
data = response.json()

print(f"Title: {data['title']}")
print(f"Word Count: {data['word_count']}")
print("\n--- Markdown Content ---\n")
print(data["markdown"])
```

### 3. JavaScript / TypeScript (Node.js & Browser)
```javascript
const response = await fetch("https://clean-web-markdown-extractor.onrender.com/extract?url=" + encodeURIComponent("https://example.com"));
const data = await response.json();

console.log("Title:", data.title);
console.log("Tokens Saved! Word count:", data.word_count);
console.log(data.markdown);
```

---

## 📡 API Reference

### `GET /extract`
Extracts and converts a webpage into clean markdown.

**Query Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `url` | string | **Yes** | Fully qualified target webpage URL (e.g., `https://example.com`) |

**Sample Response (`200 OK`):**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples in documents.",
  "word_count": 12
}
```

### `GET /health` & `GET /ping`
Liveness and readiness health check probe.

**Sample Response (`200 OK`):**
```json
{
  "status": "ok",
  "service": "markdown_extractor"
}
```

---

## 💻 Local Development & Self-Hosting

### Run Locally with Uvicorn
```bash
# Clone the repository
git clone https://github.com/Okumotinho/clean-web-markdown-extractor.git
cd clean-web-markdown-extractor

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn main:app --reload --port 8000
```
Interactive Swagger API docs will be available at: `http://localhost:8000/docs`.

### Run via Docker
```bash
docker build -t markdown-extractor .
docker run -p 8000:8000 markdown-extractor
```

### Run Tests
```bash
pytest test_main.py
```

---

## 📦 RapidAPI Integration

This service is published and monetized on the RapidAPI Marketplace:
👉 **[Access on RapidAPI Hub](https://rapidapi.com/Okumotinho/api/clean-web-markdown-extractor)**

---

## 📄 License
MIT License © 2026 Thiago Okumoto
