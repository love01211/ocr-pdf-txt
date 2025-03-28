# coding: utf-8
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from paddleocr import PaddleOCR
import os
import uuid
import shutil
from typing import Optional

app = FastAPI()

# Set up directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize PaddleOCR once (it's better to keep it as a global variable)
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def pdf_to_text(pdf_path: str) -> str:
    """Perform OCR on a PDF file and return extracted text."""
    result = ocr.ocr(pdf_path, cls=True)
    
    text_content = []
    for page in result:
        for line in page:
            if line and len(line) >= 2:  # Ensure valid result
                text_content.append(line[1][0])
    
    return '\n'.join(text_content)

@app.get("/")
async def home(request: Request):
    """Render the upload page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and OCR processing."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    upload_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    output_path = os.path.join(OUTPUT_DIR, f"{file_id}.txt")
    
    try:
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Perform OCR
        text_content = pdf_to_text(upload_path)
        
        # Save text to output file
        with open(output_path, "w", encoding="utf-8") as text_file:
            text_file.write(text_content)
        
        return {"file_id": file_id, "filename": file.filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/download/{file_id}")
async def download_file(file_id: str, original_filename: Optional[str] = None):
    """Download the OCR result as a text file."""
    output_path = os.path.join(OUTPUT_DIR, f"{file_id}.txt")
    
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Use original filename if provided, otherwise use the file_id
    download_filename = f"{original_filename.replace('.pdf', '')}.txt" if original_filename else f"{file_id}.txt"
    
    return FileResponse(
        output_path,
        media_type="text/plain",
        filename=download_filename
    )

# Cleanup function to remove old files (optional)
def cleanup_old_files(directory: str, max_age_seconds: int = 3600):
    """Remove files older than max_age_seconds."""
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
