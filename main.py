import pdfplumber
from fastapi import FastAPI, UploadFile, File

app = FastAPI()

@app.post("/extract")
async def extract(resume : UploadFile = File(...)):
  text = ""
  with pdfplumber.open(resume.file) as pdf:
    for page in pdf.pages:
      page_text = page.extract_text()
      if page_text:
        text += page_text + "\n"
  return {"text":text.strip()}