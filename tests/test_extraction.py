import pytest
from pathlib import Path
from extraction import ExtractionLogic

def test_parse_template_headers_valid():
    template = """---
tags: templates
---
# Course Wrapper
## Notes
Some notes here.
## Formulas
Some formulas here.
## Summary
Some summary.
"""
    headers = ExtractionLogic.parse_template_headers(template)
    assert headers == ["Notes", "Formulas", "Summary"]

def test_parse_template_headers_empty():
    template = "No headers here."
    headers = ExtractionLogic.parse_template_headers(template)
    assert headers == []

def test_parse_template_headers_mixed():
    template = """
# H1 Header
## Valid H2
### Valid H3
## Another H2
    """
    headers = ExtractionLogic.parse_template_headers(template)
    assert headers == ["Valid H2", "Another H2"]

def test_extract_pdf_text_multi_page():
    # Use the generated test_multi_page.pdf
    path = Path("test_multi_page.pdf")
    result = ExtractionLogic.extract_pdf_text(path)
    assert "Page 1 Content" in result
    assert "Page 2 Content" in result

def test_extract_pptx_text_full():
    # Use the generated test_extraction_demo.pptx
    path = Path("test_extraction_demo.pptx")
    result = ExtractionLogic.extract_pptx_text(path)
    
    assert "Welcome to Slide 1" in result
    assert "This is a bullet point in Slide 1" in result
    assert "Extra text box 1" in result
    assert "Notes for Slide 1" in result
    assert "Slide 2 Title" in result
    assert "Extra text box 2" in result
    assert "Notes for Slide 2" in result


def test_map_content_to_headers():
    content = "This is a long lecture transcript about Calculus."
    headers = ["Notes", "Formulas"]
    mapping = ExtractionLogic.map_content_to_headers(content, headers)
    assert "Notes" in mapping
    assert "Formulas" in mapping
    assert "Calculus" in mapping["Notes"]
