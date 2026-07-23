from pathlib import Path
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VaultWriter:
    """
    Handles writing processed lecture notes to the Obsidian vault.
    The vault is mounted at /app/notes in the container.
    """
    def __init__(self, vault_path: str = "/app/notes", preview: bool = False):
        self.vault_path = Path(vault_path)
        self.preview = preview
        if not self.vault_path.exists() and not self.preview:
            logger.warning(f"Vault path {vault_path} does not exist. Files may not be saved correctly.")

    def write_note(self, filename: str, content: str, tags: list[str] = None) -> bool:
        """
        Writes content to a .md file in the vault.
        Ensures the filename ends with .md.
        Supports tag-based pathing.
        """
        try:
            # Ensure .md extension
            if not filename.endswith(".md"):
                filename += ".md"
            
            # Tag-based pathing: create subdirectories based on tags
            # Example: tags=['CS101', 'Lectures'] -> vault_path/CS101/Lectures/filename.md
            if tags:
                # Remove '#' from tags for cleaner folder names
                folder_path = Path(*[tag.lstrip('#') for tag in tags])
                final_dir = self.vault_path / folder_path
            else:
                final_dir = self.vault_path

            # Sanitize filename to avoid path traversal
            safe_filename = Path(filename).name
            file_path = final_dir / safe_filename
            
            if self.preview:
                logger.info(f"[PREVIEW] Would write note to {file_path}")
                logger.info(f"[PREVIEW] Content: {content[:100]}... (truncated)")
                return True

            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Successfully wrote note to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to write note {filename}: {str(e)}")
            return False

    def save_with_template(self, template_content: str, extracted_text: str, filename: str, tags: list[str] = None) -> bool:
        """
        Combines template and extracted text before writing to the vault.
        Assuming the template has a placeholder like {{content}}.
        """
        final_content = template_content.replace("{{content}}", extracted_text)
        return self.write_note(filename, final_content, tags=tags)
