from datetime import datetime, timedelta
from jose import jwt
from interfaces.api.security.security import ALGORITHM, SECRET_KEY

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

token = create_access_token({"user": "admin"})

print(token)

