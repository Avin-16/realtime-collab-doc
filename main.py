# app/auth/dependencies.py
from fastapi import FastAPI
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from auth.jwt_handler import SECRET_KEY ,ALGORITHM
from auth.routes import *
from database import get_db,engine
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text

app = FastAPI()
app.include_router(auth_router)



# This tells FastAPI where the token will come from:
# Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Optional: Redis client for logout token blacklist

# Step 8 — Token verification logic
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """
    seps explained:
    1. Extract token from Authorization header
    2. Decode token using SECRET_KEY and algorithm
    3. Extract 'sub' (subject) which is usually the username or user ID
    4. Check Redis if token is blacklisted (optional)
    5. Fetch user from DB to ensure they still exist
    6. Return user data to protected routes
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 1Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract username (the 'sub' claim stores it)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception


    except JWTError:
        # Token is invalid or expired
        raise credentials_exception

    #  Fetch user from database to ensure validity
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    #  Return user model (used in protected routes)
    return user


@app.get("/health/")
async def healthdb():
    try :
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return{ "status":"ok" , "database":"connected"}
    except Exception as e:
        raise HTTPException(status_code=500 , detail="db connection failed : {e}" )