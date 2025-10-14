from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


from database  import  get_db 
from models import *
from schemas import *
from auth.hashing import hash_pass , verify_pass
from auth.jwt_handler import  create_access_token , verify_token


# router instance to register routes
auth_router = APIRouter()


# reginster endpoints 

@auth_router.post("/register",response_model=ShowUser)
async def register_user(user:UserCreate , db :AsyncSession = Depends(get_db)):
    """
    register user
        check if email exists
        has password
        save user in db
    """

    # Query DB for existing username
    query_ = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing = query_.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code= 400 ,detail="emial already exists")


    # Create new user record  
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_pass(user.password)
    )


    # Add user to DB and commit
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)   # refresh instance to get auto-generated id
    await db.refresh(new_user)  


# login endpoints

@auth_router.post("/login")
async def login_user(user:UserLogin, db:AsyncSession = Depends(get_db)):
    """
    logs in a user
        check if user exist
        verify password with hashed password
        generate token
    """
    query = await db.execute(select(User).where(User.email == user.email))
    db_user = query.scalar_one_or_none()

    if db_user:
        access_token = create_access_token({"sub":db_user.email})
        return{"access_token":access_token, "msg":"login sucessfull"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, details = "Invalid Credentails")
                     