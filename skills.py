import re
from similarity import text_similarity
SKILLS = {
  "python": ["python"],
  "java": ["java"],
  "javascript": ["javascript", "java script"],
  "html": ["html", "html5"],
  "css": ["css", "css3"],
  "sql": ["sql"],
  "flask": ["flask"],
  "fastapi": ["fastapi", "fast api"],
  "django": ["django"],
  "rest api": ["rest api", "rest apis", "restful api", "restful apis"],
  "git": ["git"],
  "github": ["github", "git hub"],
  "docker": ["docker"],
  "aws": ["aws", "amazon web services"],
  "linux": ["linux"],
  "pandas": ["pandas"],
  "numpy": ["numpy"],
  "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
  "machine learning": ["machine learning"],
  "deep learning": ["deep learning"],
  "nlp": ["nlp", "natural language processing"],
  "computer vision": ["computer vision", "cv"],
  "neural networks": ["neural networks", "neural network", "ann", "artificial neural networks"],
  "cnn": ["cnn", "cnns", "convolutional neural networks"],
  "rnn": ["rnn", "rnns", "recurrent neural networks"],
  "tensorflow": ["tensorflow"],
  "pytorch": ["pytorch"],
  "keras": ["keras"],
  "opencv": ["opencv", "open cv"],
  "yolo": ["yolo", "yolov7", "yolov8"],
  "mcp": ["mcp", "model context protocol"],
  "postgresql": ["postgresql", "postgres"],
  "mysql": ["mysql"],
  "mongodb": ["mongodb", "mongo db"],
  "data structures": ["data structures", "dsa"],
  "algorithms": ["algorithms"],
  "oop": ["oop", "object oriented programming", "object-oriented programming"],
  "pulp": ["pulp"],
  "matplotlib": ["matplotlib"],
  "react": ["react", "reactjs", "react.js"],
  "node.js": ["node.js", "node js", "nodejs"],
  "c++": ["c++"],
  "pytest": ["pytest"],
  "jwt": ["jwt", "json web token"],
}
def find_skills(text):
  text = text.lower()
  found = []
  for skill,aliases in SKILLS.items():
    for alias in aliases:
     pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
     if re.search(pattern,text):
       found.append(skill)
       break
  return found
def compare_skills(resume_text,job_text):
  resume_skills = set(find_skills(resume_text))
  job_skills = set(find_skills(job_text))

  matched = resume_skills & job_skills
  missing = job_skills - resume_skills
  extra = resume_skills - job_skills

  if len(job_skills) == 0:
    skill_score = 0
  else:
     skill_score = round(len(matched) / len(job_skills) * 100)

  sem = text_similarity(resume_text, job_text)

  return {
    "score": round(skill_score * 0.6 + sem * 0.4),
    "semantic_score": sem,
    "skill_score": skill_score,
    "matched": sorted(matched),
    "missing": sorted(missing),
    "extra": sorted(extra),
  }
if __name__ == "__main__":
  job = "We need Python, SQL, Docker, FastAPI and Git."
  resume = "i know python, flask, html"
  print(compare_skills(resume,job))