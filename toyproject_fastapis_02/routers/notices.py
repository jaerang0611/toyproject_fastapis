import bcrypt
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models
from ..database import get_db
from pydantic import BaseModel

router = APIRouter()

class NoticeBase(BaseModel):
    title: str
    content: str
    nickname: str

class NoticeCreate(NoticeBase):
    password: str

class NoticeUpdate(NoticeBase):
    password: str

from datetime import datetime

class NoticeInDB(NoticeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/", response_model=NoticeInDB)
def create_notice(notice: NoticeCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(notice.password)
        db_notice = models.Notice(
            title=notice.title,
            content=notice.content,
            nickname=notice.nickname,
            password_hash=hashed_password
        )
        db.add(db_notice)
        db.commit()
        db.refresh(db_notice)
        return db_notice
    except Exception as e:
        logging.error(f"Error creating notice: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/", response_model=List[NoticeInDB])
def read_notices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    notices = db.query(models.Notice).order_by(models.Notice.created_at.desc()).offset(skip).limit(limit).all()
    return notices

@router.get("/{notice_id}", response_model=NoticeInDB)
def read_notice(notice_id: int, db: Session = Depends(get_db)):
    db_notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")
    return db_notice

@router.put("/{notice_id}", response_model=NoticeInDB)
def update_notice(notice_id: int, notice: NoticeUpdate, db: Session = Depends(get_db)):
    db_notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")

    if not verify_password(notice.password, db_notice.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    db_notice.title = notice.title
    db_notice.content = notice.content
    db_notice.nickname = notice.nickname
    db.commit()
    db.refresh(db_notice)
    return db_notice

class NoticeDelete(BaseModel):
    password: str
@router.delete("/{notice_id}", response_model=NoticeInDB)
def delete_notice(notice_id: int, notice: NoticeDelete, db: Session = Depends(get_db)):
    db_notice = db.query(models.Notice).filter(models.Notice.id == notice_id).first()
    if db_notice is None:
        raise HTTPException(status_code=404, detail="Notice not found")

    if not verify_password(notice.password, db_notice.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

    db.delete(db_notice)
    db.commit()
    return db_notice
