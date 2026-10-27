import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from skills import compare_skills

app = FastAPI(title="Ai Resume Analyzer")

def read_pdf(file) -> str:
  with pdfplumber.open(file) as pdf:
    text = "\n".join(page.extract_text(x_tolerance=1) or "" for page in pdf.pages)
  return text.strip()

@app.post("/extract")
async def extract(resume: UploadFile = File(...)):
  return {"text": read_pdf(resume.file)}

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), job_description: str = Form(...)):
  if resume.content_type != "application/pdf":
    raise HTTPException(status_code=400, detail="Please upload a PDF file")
  resume_text = read_pdf(resume.file)
  if not resume_text:
    raise HTTPException(status_code=422, detail="Could not read any text from this PDF")
  return compare_skills(resume_text, job_description)

# Mount the static directory at the root URL ("/") so index.html loads automatically
app.mount("/", StaticFiles(directory="static", html=True), name="static")