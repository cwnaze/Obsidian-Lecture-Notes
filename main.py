import os
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pathlib import Path
import shutil
import uuid
from extraction import ExtractionLogic
from template_parsing_engine import TemplateParsingEngine
from vault_writer import VaultWriter

app = FastAPI()

# Configure upload directory
UPLOAD_DIR = Path("/tmp/obsidian_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Template Directory (using expanduser to resolve ~)
TEMPLATES_DIR = Path("~/Notes/Templates").expanduser()
template_engine = TemplateParsingEngine(str(TEMPLATES_DIR))
vault_writer = VaultWriter(vault_path="/app/notes")

@app.get("/templates")
async def list_templates():
    """
    Lists all available template files in ~/Notes/Templates.
    """
    try:
        templates = template_engine.list_templates()
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")

@app.get("/templates/{template_name}")
async def read_template(template_name: str):
    """
    Reads the content of a specific template file.
    """
    try:
        content = template_engine.read_template(template_name)
        return {"template_name": template_name, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Template not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read template: {str(e)}")

@app.post("/upload")
async def upload_large_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Handles large file uploads by streaming them to disk.
    Uses BackgroundTasks to trigger the extraction process asynchronously.
    """
    try:
        # Create a unique filename to prevent collisions
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        dest_path = UPLOAD_DIR / unique_filename

        # Stream the upload to disk to avoid loading the entire file into memory
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Trigger extraction in the background
        background_tasks.add_task(process_uploaded_file, dest_path, file.filename)

        return {
            "filename": file.filename,
            "upload_id": unique_filename,
            "status": "uploaded",
            "message": "File uploaded successfully and extraction started in background."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

def process_uploaded_file(file_path: Path, original_filename: str):
    """
    Background task to extract text from the uploaded file and save it to the vault.
    """
    try:
        print(f"Processing file: {original_filename} at {file_path}")
        
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            text = ExtractionLogic.extract_pdf_text(file_path)
        elif ext == ".pptx":
            text = ExtractionLogic.extract_pptx_text(file_path)
        elif ext in [".mp3", ".wav", ".m4a", ".ogg", ".flac"]:
            text = ExtractionLogic.extract_audio_text(file_path)
        else:
            text = f"Unsupported file format: {ext}"
            
        print(f"Successfully extracted text for {original_filename}")

        # Save the extracted text to the vault
        # Use the original filename as the note name, ensuring it's .md
        note_filename = Path(original_filename).stem + ".md"
        success = vault_writer.write_note(note_filename, text)
        
        if success:
            print(f"Successfully saved {note_filename} to the vault.")
        else:
            print(f"Failed to save {note_filename} to the vault.")
        
    except Exception as e:
        print(f"Error processing file {original_filename}: {str(e)}")
    finally:
        # Cleanup: Remove the temporary file after processing
        if file_path.exists():
            file_path.unlink()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
