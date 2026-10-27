import pdfplumber
from skills import compare_skills
from skills import find_skills

with pdfplumber.open("Bhanu_9014830551_resume.pdf") as pdf:
  resume_text = "\n".join(page.extract_text(x_tolerance = 1) or "" for page in pdf.pages)


job_text = """
We are looking for an AI/ML Engineer with strong Python skills.
Experience with FastAPI or Flask, SQL, Docker and Git is required.
Knowledge of machine learning, NLP, pandas and scikit-learn.
AWS and REST API experience is a plus.
"""

result = compare_skills(resume_text, job_text)

print("Score:", result["score"])
print("Matched:", result["matched"])
print("Missing:", result["missing"])
print("Extra:", result["extra"])