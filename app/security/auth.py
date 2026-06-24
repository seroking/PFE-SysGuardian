import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


def hash_password(password: str):
    encoded_pw = password.encode("utf-8")
    hashed = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, stored_hash: str):
    encoded_pw = password.encode("utf-8")
    encoded_hash = stored_hash.encode("utf-8")

    return bcrypt.checkpw(encoded_pw, encoded_hash)


def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None 