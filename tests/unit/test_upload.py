import io
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

from PIL import Image

def test_upload_success():
    # Simulate a small valid PNG upload using Pillow
    img_byte_arr = io.BytesIO()
    Image.new('RGB', (100, 100), color='blue').save(img_byte_arr, format='PNG')
    file_content = img_byte_arr.getvalue()
    
    file_data = {"image": ("test.png", io.BytesIO(file_content), "image/png")}
    response = client.post("/api/v1/upload", files=file_data)
    
    assert response.status_code == 200
    json_data = response.json()
    assert "job_id" in json_data
    assert len(json_data["job_id"]) > 0

def test_upload_invalid_extension():
    # Simulate an invalid file format upload (e.g. PDF)
    file_content = b"%PDF-1.4 mock file"
    file_data = {"image": ("test.pdf", io.BytesIO(file_content), "application/pdf")}
    response = client.post("/api/v1/upload", files=file_data)
    
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert "Unsupported file extension" in json_data["message"]

def test_upload_file_too_large():
    # Create mock content exceeding 25MB (26MB)
    too_large_content = b"0" * (26 * 1024 * 1024)
    file_data = {"image": ("large.png", io.BytesIO(too_large_content), "image/png")}
    response = client.post("/api/v1/upload", files=file_data)
    
    assert response.status_code == 400
    json_data = response.json()
    assert json_data["success"] is False
    assert "exceeds maximum allowed size" in json_data["message"]
