import re
from pathlib import Path
from typing import List

class ExtractionLogic:
    """
    Handles extraction of text from various formats and 
    parsing of Obsidian templates.
    """
    
    @staticmethod
    def extract_pdf_text(pdf_path: Path) -> str:
        # Implementation will use PyMuPDF
        # For now, a stub that simulates extraction for testing
        return f"Extracted text from PDF: {pdf_path.name}"

    @staticmethod
    def extract_pptx_text(pptx_path: Path) -> str:
        # Implementation will use python-pptx
        return f"Extracted text from PPTX: {pptx_path.name}"

    @staticmethod
    def parse_template_headers(template_content: str) -> List[str]:
        """
        Extracts H2 headers from an Obsidian template.
        Example: ## Notes -> 'Notes'
        """
        pattern = r'^##\s+(.+)$'
        headers = re.findall(pattern, template_content, re.MULTILINE)
        return headers

    @staticmethod
    def map_content_to_headers(content: str, headers: List[str]) -> dict:
        """
        Simplistic mapping of content to headers for testing.
        In production, this will be handled by the LLM.
        """
        return {header: f"Content for {header} based on: {content}" for header in headers}
