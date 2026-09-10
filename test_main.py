import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_extract_tables():
    from bs4 import BeautifulSoup
    from workspace.apis.markdown_extractor.main import parse_html_tables
    html = '<table><tr><th>Col1</th><th>Col2</th></tr><tr><td>Val1</td><td>Val2</td></tr></table>'
    soup = BeautifulSoup(html, 'html.parser')
    parse_html_tables(soup)
    text = soup.get_text()
    assert '| Col1 | Col2 |' in text
    assert '| Val1 | Val2 |' in text
