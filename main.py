import pdfplumber
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from skills import compare_skills
from database import SessionLocal, Analysis, User
from auth import hash_password, verify_password, create_access_token, verify_access_token

app = FastAPI(title="AI Resume Analyzer")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  username = verify_access_token(token)
  if not username:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
  user = db.query(User).filter(User.username == username).first()
  if not user:
    raise HTTPException(status_code=401, detail="User not found")
  return user

@app.post("/signup")
def signup(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  existing_user = db.query(User).filter(User.username == form_data.username).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="Username already registered")

  hashed_pwd = hash_password(form_data.password)
  new_user = User(username=form_data.username, hashed_password=hashed_pwd)
  db.add(new_user)
  db.commit()
  return {"message": "User created successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(User).filter(User.username == form_data.username).first()
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(status_code=400, detail="Incorrect username or password")

  access_token = create_access_token(data={"sub": user.username})
  return {"access_token": access_token, "token_type": "bearer"}

@app.post("/extract")
async def extract(resume: UploadFile = File(...)):
  return {"text": read_pdf(resume.file)}

@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
