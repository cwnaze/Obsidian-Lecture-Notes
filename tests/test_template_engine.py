import unittest
from pathlib import Path
import yaml
import shutil
import tempfile
from template_parsing_engine import TemplateParsingEngine

class TestTemplateParsingEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.templates_dir = self.test_dir / "Templates"
        self.templates_dir.mkdir()
        self.engine = TemplateParsingEngine(str(self.templates_dir))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_list_templates(self):
        (self.templates_dir / "temp1.md").write_text("content 1")
        (self.templates_dir / "temp2.md").write_text("content 2")
        (self.templates_dir / "other.txt").write_text("not a template")
        
        templates = self.engine.list_templates()
        self.assertCountEqual(templates, ["temp1.md", "temp2.md"])

    def test_extract_h2_headers(self):
        content = "## Header 1\nSome text\n## Header 2\nMore text\n### H3 Header\n# H1 Header"
        headers = self.engine.extract_h2_headers(content)
        self.assertEqual(headers, ["Header 1", "Header 2"])

    def test_merge_frontmatter_tags_with_existing(self):
        content = "---\ntags: [template_tag1, template_tag2]\n---\n## Notes\n"
        user_tags = ["user_tag1", "user_tag2"]
        merged = self.engine.merge_frontmatter_tags(content, user_tags)
        
        # Extract the tags from the resulting YAML
        parts = merged.split("---", 2)
        fm_data = yaml.safe_load(parts[1])
        self.assertEqual(fm_data["tags"], ["template_tag1", "template_tag2", "user_tag1", "user_tag2"])

    def test_merge_frontmatter_tags_no_existing(self):
        content = "## Notes\n"
        user_tags = ["user_tag1"]
        merged = self.engine.merge_frontmatter_tags(content, user_tags)
        
        parts = merged.split("---", 2)
        fm_data = yaml.safe_load(parts[1])
        self.assertEqual(fm_data["tags"], ["user_tag1"])

    def test_merge_frontmatter_tags_deduplication(self):
        content = "---\ntags: [common_tag, template_tag]\n---\n## Notes\n"
        user_tags = ["common_tag", "user_tag"]
        merged = self.engine.merge_frontmatter_tags(content, user_tags)
        
        parts = merged.split("---", 2)
        fm_data = yaml.safe_load(parts[1])
        self.assertEqual(fm_data["tags"], ["common_tag", "template_tag", "user_tag"])

if __name__ == "__main__":
    unittest.main()
