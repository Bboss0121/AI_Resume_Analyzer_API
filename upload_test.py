import requests
url = "http://127.0.0.1:8000/extract"
with open("Bhanu_9014830551_resume.pdf","rb") as f:
  files = {"resume": ("Bhanu_9014830551_resume.pdf",f,"application/pdf")}
  response = requests.post(url,files = files)
print(response.status_code)
print(response.json())