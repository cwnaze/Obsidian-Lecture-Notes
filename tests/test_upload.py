import pytest
from fastapi.testclient import TestClient
from main import app
import os
from pathlib import Path

client = TestClient(app)

def test_upload_pdf(tmp_path):
    # Create a dummy PDF file
    pdf_content = b"PDF dummy content"
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(pdf_content)

    with open(pdf_file, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["status"] == "uploaded"
    assert "upload_id" in data

def test_upload_pptx(tmp_path):
    # Create a dummy PPTX file
    pptx_content = b"PPTX dummy content"
    pptx_file = tmp_path / "test.pptx"
    pptx_file.write_bytes(pptx_content)

    with open(pptx_file, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.pptx", f, "application/vnd.ms-powerpoint")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.pptx"
    assert data["status"] == "uploaded"
    assert "upload_id" in data

def test_upload_unsupported(tmp_path):
    # Create a dummy text file
    txt_content = b"txt dummy content"
    txt_file = tmp_path / "test.txt"
    txt_file.write_bytes(txt_content)

    with open(txt_file, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.txt", f, "text/plain")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["status"] == "uploaded"
