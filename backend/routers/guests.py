# backend/routers/guests.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..schemas import Guest, GuestCreate  # 从 schemas 导入 Pydantic 模型
from ..models import Guest as GuestModel  # 从 models 导入 ORM 模型，并重命名以避免混淆
import logging

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[Guest])  # 使用 Pydantic 的 Guest
def get_guests(db: Session = Depends(get_db)):
    guests = db.query(GuestModel).all()
    return guests


@router.post("/", response_model=Guest)
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    existing_guest = db.query(GuestModel).filter(GuestModel.id_number == guest.id_number).first()
    if existing_guest:
        raise HTTPException(status_code=400, detail="Guest with this ID number already exists")

    new_guest = GuestModel(
        name=guest.name,
        id_number=guest.id_number,
        phone=guest.phone
    )
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest
