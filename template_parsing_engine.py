import os
import re
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

class TemplateParsingEngine:
    def __init__(self, templates_dir: str):
        self.templates_dir = Path(templates_dir)

    def list_templates(self) -> List[str]:
        """Lists all markdown templates in the templates directory."""
        if not self.templates_dir.exists():
            return []
        return [f.name for f in self.templates_dir.glob("*.md")]

    def read_template(self, template_name: str) -> str:
        """Reads the content of a specific template file."""
        template_path = self.templates_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template {template_name} not found.")
        return template_path.read_text(encoding="utf-8")

    def extract_h2_headers(self, content: str) -> List[str]:
        """
        Extracts all H2 headers (## Header Name) from the template content.
        """
        # Regex to find lines starting with '## '
        pattern = r"^##\s+(.+)$"
        headers = re.findall(pattern, content, re.MULTILINE)
        return [h.strip() for h in headers]

    def merge_frontmatter_tags(self, template_content: str, user_tags: List[str]) -> str:
        """
        Merges user-provided tags with tags found in the template's frontmatter.
        
        The template frontmatter is used as the base. The user_tags are appended 
        to the tags list.
        """
        # Split content into frontmatter and body
        parts = template_content.split("---", 2)
        if len(parts) < 3:
            # No valid frontmatter found, create a new one with user tags
            new_frontmatter = {"tags": user_tags}
            yaml_fm = yaml.dump(new_frontmatter, sort_keys=False).strip()
            return f"---\n{yaml_fm}\n---\n{template_content}"

        frontmatter_raw = parts[1]
        body = parts[2]

        try:
            fm_data = yaml.safe_load(frontmatter_raw) or {}
        except yaml.YAMLError as e:
            print(f"Error parsing template frontmatter: {e}")
            fm_data = {}

        # Merge tags
        template_tags = fm_data.get("tags", [])
        if isinstance(template_tags, str):
            template_tags = [template_tags]
        elif template_tags is None:
            template_tags = []

        # Combine tags and remove duplicates while preserving order
        combined_tags = list(dict.fromkeys(template_tags + user_tags))
        fm_data["tags"] = combined_tags

        # Re-serialize frontmatter
        yaml_fm = yaml.dump(fm_data, sort_keys=False).strip()
        return f"---\n{yaml_fm}\n---\n{body}"

# For quick verification if run as script
if __name__ == "__main__":
    # Mock setup for testing
    import tempfile
    import shutil

    with tempfile.TemporaryDirectory() as tmpdir:
        templates_path = Path(tmpdir) / "Templates"
        templates_path.mkdir()
        
        test_template = "test_template.md"
        content = "---\ntags: [projects/template]\n---\n## Notes\n## Formulas\n"
        (templates_path / test_template).write_text(content)
        
        engine = TemplateParsingEngine(str(templates_path))
        print(f"Templates: {engine.list_templates()}")
        
        text = engine.read_template(test_template)
        print(f"Extracted Headers: {engine.extract_h2_headers(text)}")
        
        user_tags = ["school/math/mac2313", "module1"]
        merged = engine.merge_frontmatter_tags(text, user_tags)
        print("Merged Content:\n", merged)
