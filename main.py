import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from skills import compare_skills
from database import SessionLocal, Analysis

app = FastAPI(title="AI Resume Analyzer")

def read_pdf(file) -> str:
  with pdfplumber.open(file) as pdf:
    text = "\n".join(page.extract_text(x_tolerance=1) or "" for page in pdf.pages)
  return text.strip()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/extract")
async def extract(resume: UploadFile = File(...)):
  return {"text": read_pdf(resume.file)}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
  if resume.content_type != "application/pdf":
    raise HTTPException(status_code=400, detail="Please upload a PDF file")

  resume_text = read_pdf(resume.file)
  if not resume_text:
    raise HTTPException(status_code=422, detail="Could not read any text from this PDF")

  result = compare_skills(resume_text, job_description)

  # Save analysis to database
  db_analysis = Analysis(
      job_description=job_description,
      skill_score=result["skill_score"],
      semantic_score=result["semantic_score"],
      final_score=result["score"]
  )
  db.add(db_analysis)
  db.commit()

  return result

# Mount the static directory at the root URL ("/") so index.html loads automatically
app.mount("/", StaticFiles(directory="static", html=True), name="static")
