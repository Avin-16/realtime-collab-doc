import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import UploadedFile
from schemas import UploadedFileResponse

router = APIRouter(prefix = "/upload")

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR,exist_ok=True)


async def upload_doc(
        
    file: UploadFile = File(...),
    uploaded_by: str = Form(...),   # optional metadata field
    db: Session = Depends(get_db)  ):

    #1--validatoin

    allow_extension = [".pdf" , ".txt" , ".png"]
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allow_extension:
        raise HTTPException(status_code= 500 , detail= 'unsupported file type')
    
    content = await file.read()
    max_size= 10 *1000*1000
    if len(content) > max_size:
        raise HTTPException(status_code=500 , detail=" file size should be less than 10MB")
    
    # Reset file pointer
    await file.seek(0)

    #2 --save

    safe_file_name = f"{uuid.uuid4()}{file_ext}"
    upload_path = os.path.join(UPLOAD_DIR,safe_file_name)

    try:
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File write error: {str(e)}")

    file_url = f"/static/uploads/{safe_file_name}"  


    # ---------- 3. DB ENTRY ----------
    db_record = UploadedFile(
        file_name=file.filename,
        content_type=file.content_type,
        size=len(content),
        path=upload_path,
        uploaded_by=uploaded_by,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    # ---------- 4. RESPONSE ----------
    return UploadedFileResponse(
        id=db_record.id,
        file_name=db_record.file_name,
        url=file_url,
        size=db_record.size,
        uploaded_at=db_record.created_at,
    )
