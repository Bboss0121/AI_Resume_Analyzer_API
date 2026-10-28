from fastapi.testclient import TestClient
from database import Base, SessionLocal, User, engine
from main import app
from skills import compare_skills
from similarity import text_similarity

client = TestClient(app)


def setup_module(module):
  # Clean up database tables for testing
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)


def test_similarity_basic():
  # Test TF-IDF similarity calculation
  score = text_similarity("python developer", "python developer")
  assert score == 100.0

  score_low = text_similarity("python", "cooking recipe")
  assert score_low < 20.0


def test_compare_skills():
  resume = "I know Python, FastAPI, and Docker."
  job = "We are looking for Python and FastAPI."
  result = compare_skills(resume, job)

  assert result["score"] > 0
  assert "python" in result["matched"]
  assert "fastapi" in result["matched"]


def test_signup_and_login():
  # Clean user if exists
  db = SessionLocal()
  db.query(User).filter(User.username == "teststudent").delete()
  db.commit()
  db.close()

  # 1. Signup
  response = client.post(
      "/signup",
      data={"username": "teststudent", "password": "mypassword123"}
  )
  assert response.status_code == 200
  assert response.json()["message"] == "User created successfully"

  # 2. Login
  response = client.post(
      "/login",
      data={"username": "teststudent", "password": "mypassword123"}
  )
  assert response.status_code == 200
  data = response.json()
  assert "access_token" in data
  assert data["token_type"] == "bearer"


def test_analyze_unauthorized():
  # Trying to analyze without a token should fail with 401
  response = client.post(
      "/analyze",
      data={"job_description": "Looking for Python"}
  )
  assert response.status_code == 401
