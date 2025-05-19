from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.schemas import TokenData  # Ensure TokenData is defined in app.schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "knaf83r09vhin20939nr0jamsdnv093nitrhg09qfq984hbv4q034tnivne"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.utcnow() + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})

    encoded_token = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)

    return encoded_token


def verify_access_token(token: str, credentials_exception):
    try:
        data_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        new_id: str = str(data_payload.get("user_id"))
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=new_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"can't validate user token", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
