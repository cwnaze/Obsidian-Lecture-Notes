import os
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pathlib import Path
import shutil
import uuid
from extraction import ExtractionLogic

app = FastAPI()

# Configure upload directory
UPLOAD_DIR = Path("/tmp/obsidian_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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
    Background task to extract text from the uploaded file.
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
        # In a real app, we would save this text to a database or notify the user via WebSocket/Webhook
        
    except Exception as e:
        print(f"Error processing file {original_filename}: {str(e)}")
    finally:
        # Cleanup: Remove the temporary file after processing
        if file_path.exists():
            file_path.unlink()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
