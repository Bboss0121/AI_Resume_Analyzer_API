from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt

SECRET_KEY = "super-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
  # bcrypt requires bytes
  pwd_bytes = password.encode("utf-8")
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(pwd_bytes, salt)
  return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
  pwd_bytes = plain_password.encode("utf-8")
  hashed_bytes = hashed_password.encode("utf-8")
  return bcrypt.checkpw(pwd_bytes, hashed_bytes)


def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      return None
    return username
  except JWTError:
    return None
