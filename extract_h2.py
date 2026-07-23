import re
from typing import List

def extract_h2_headers(content: str) -> List[str]:
    """
    Extracts H2 headers (## Header Name) from an Obsidian template.
    
    Args:
        content (str): The raw text content of the template file.
        
    Returns:
        List[str]: A list of extracted H2 header titles.
    """
    # Regex pattern: 
    # ^       : Start of line
    # ##      : Matches two hash symbols (H2)
    # \s+     : One or more whitespace characters
    # (.+?)   : Non-greedy capture of the header title
    # \s*     : Optional trailing whitespace
    # $       : End of line
    pattern = r'^##\s+(.+?)\s*$'
    
    # Use re.MULTILINE to allow ^ and $ to match the start/end of each line
    headers = re.findall(pattern, content, re.MULTILINE)
    
    return headers

# --- Verification Tests ---
if __name__ == "__main__":
    test_cases = [
        {
            "name": "Standard H2s",
            "content": "## Notes\nSome text\n## Formulas\nMore text",
            "expected": ["Notes", "Formulas"]
        },
        {
            "name": "Mixed Headers",
            "content": "# H1\n## H2-1\n### H3\n## H2-2",
            "expected": ["H2-1", "H2-2"]
        },
        {
            "name": "Obsidian Frontmatter",
            "content": "---\ntags: test\n---\n## Section 1\nContent\n## Section 2",
            "expected": ["Section 1", "Section 2"]
        },
        {
            "name": "Whitespace and trailing",
            "content": "##   Padded Header   \n## Clean Header",
            "expected": ["Padded Header", "Clean Header"]
        },
        {
            "name": "No H2s",
            "content": "# Only H1\n### Only H3",
            "expected": []
        }
    ]

    for case in test_cases:
        result = extract_h2_headers(case["content"])
        assert result == case["expected"], f"Test {case['name']} failed: expected {case['expected']}, got {result}"
    
    print("All verification tests passed!")
