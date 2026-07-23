import unittest
from pathlib import Path
from vault_writer import VaultWriter
import os

class TestVaultWriter(unittest.TestCase):
    def setUp(self):
        self.test_vault = Path("/tmp/test_vault")
        self.test_vault.mkdir(parents=True, exist_ok=True)
        self.writer = VaultWriter(vault_path=str(self.test_vault))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_vault)

    def test_write_note_basic(self):
        filename = "test_note"
        content = "Hello World"
        success = self.writer.write_note(filename, content)
        
        self.assertTrue(success)
        expected_path = self.test_vault / "test_note.md"
        self.assertTrue(expected_path.exists())
        self.assertEqual(expected_path.read_text(), content)

    def test_write_note_with_extension(self):
        filename = "test_note.md"
        content = "Hello World"
        success = self.writer.write_note(filename, content)
        
        self.assertTrue(success)
        expected_path = self.test_vault / "test_note.md"
        self.assertTrue(expected_path.exists())

    def test_save_with_template(self):
        template = "Note: {{content}}\nDate: 2026"
        text = "This is the extracted text"
        filename = "templated_note"
        
        success = self.writer.save_with_template(template, text, filename)
        
        self.assertTrue(success)
        expected_path = self.test_vault / "templated_note.md"
        self.assertEqual(expected_path.read_text(), "Note: This is the extracted text\nDate: 2026")

    def test_path_traversal_protection(self):
        filename = "../evil_file"
        content = "Hacked"
        success = self.writer.write_note(filename, content)
        
        self.assertTrue(success)
        # Should be written as "evil_file.md" inside the vault, not outside
        self.assertTrue((self.test_vault / "evil_file.md").exists())
        self.assertFalse((self.test_vault.parent / "evil_file.md").exists())

    def test_preview_mode(self):
        preview_writer = VaultWriter(vault_path=str(self.test_vault), preview=True)
        filename = "preview_note"
        content = "Should not be written"
        success = preview_writer.write_note(filename, content)
        
        self.assertTrue(success)
        expected_path = self.test_vault / "preview_note.md"
        self.assertFalse(expected_path.exists())

    def test_tag_based_pathing(self):
        tags = ["#CS101", "Lectures"]
        filename = "lecture1"
        content = "Content of lecture 1"
        success = self.writer.write_note(filename, content, tags=tags)
        
        self.assertTrue(success)
        # Tags should be stripped of # and used as folder path: CS101/Lectures/lecture1.md
        expected_path = self.test_vault / "CS101" / "Lectures" / "lecture1.md"
        self.assertTrue(expected_path.exists())
        self.assertEqual(expected_path.read_text(), content)

    def test_tag_based_pathing_no_tags(self):
        filename = "no_tags_note"
        content = "Content"
        success = self.writer.write_note(filename, content, tags=None)
        
        self.assertTrue(success)
        expected_path = self.test_vault / "no_tags_note.md"
        self.assertTrue(expected_path.exists())

if __name__ == "__main__":
    unittest.main()
