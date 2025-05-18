from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "knaf83r09vhin20939nr0jamsdnv093nitrhg09qfq984hbv4q034tnivne"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    encoded_token = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)

    return encoded_token
