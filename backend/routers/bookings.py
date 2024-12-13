# backend/routers/bookings.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..schemas import Booking, BookingCreate  # Pydantic模型
from ..models import Booking as BookingModel, RoomModel, Guest  # ORM模型
from datetime import datetime
import logging

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[Booking])
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(BookingModel).all()  # 使用ORM模型
    return bookings

@router.post("/", response_model=Booking)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_number == booking.room_number).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.is_powered_on:
        raise HTTPException(status_code=400, detail="Room is already occupied")

    guest = db.query(Guest).filter(Guest.id == booking.guest_id).first()
    if not guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    new_booking = BookingModel(
        room_number=booking.room_number,
        guest_id=booking.guest_id,
        status="checked_in",
        booking_time=datetime.utcnow()  # 假设有booking_time字段
    )
    room.is_powered_on = True
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.post("/{booking_id}/checkout", response_model=Booking)
def checkout_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()  # 使用ORM模型
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "checked_out":
        raise HTTPException(status_code=400, detail="Booking is already checked out")

    booking.status = "checked_out"
    booking.checkout_time = datetime.utcnow()
    # 计算总费用（示例逻辑，需根据实际需求调整）
    booking.total_cost += 10.0  # 示例：每次退房增加10元

    room = db.query(RoomModel).filter(RoomModel.room_number == booking.room_number).first()
    room.is_powered_on = False

    db.commit()
    db.refresh(booking)
    return booking
