from datetime import datetime, timedelta
from jose import JWTError ,jwt          # python-jose is used to encode/decode JWTs

SECRET_KEY  = 'this_app_secret_jey'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data:dict,expire_delta:timedelta | None =None):
    """
    Creates a JWT access token.
    - `data`: information to encode inside the token (like username, id, etc.)
    - `expires_delta`: how long the token should be valid
    """
    
    data_to_encode = data.copy()

    expire = datetime.now() + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    data_to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(data_to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt



def verify_token(token:str):

    """
    Verifies a JWT token.
    - Decodes it using the secret key.
    - Returns the payload (data) if valid.
    - Returns None if invalid or expired.
    """
        

    try:
        payload  = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
