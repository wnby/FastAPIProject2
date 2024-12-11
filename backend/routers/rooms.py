# backend/routers/rooms.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import SessionLocal
from ..schemas import Room, ModeEnum, WindSpeedEnum
from ..models import RoomModel
import logging

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/room_info", response_model=List[Room])
def get_room_info(db: Session = Depends(get_db)):
    rooms = db.query(RoomModel).all()
    return rooms

@router.post("/{room_number}/turn_on")
def turn_on(room_number: int, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_number == room_number).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.is_powered_on:
        raise HTTPException(status_code=400, detail="Room is already powered on")
    room.is_powered_on = True
    db.commit()
    return {"message": "Room powered on"}

@router.post("/{room_number}/turn_off")
def turn_off(room_number: int, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_number == room_number).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not room.is_powered_on:
        raise HTTPException(status_code=400, detail="Room is already powered off")
    room.is_powered_on = False
    db.commit()
    return {"message": "Room powered off"}

@router.post("/{room_number}/set_temperature")
def set_temperature(room_number: int, temperature: float, db: Session = Depends(get_db)):
    if temperature < 18 or temperature > 30:
        raise HTTPException(status_code=400, detail="Temperature must be between 18°C and 30°C")
    room = db.query(RoomModel).filter(RoomModel.room_number == room_number).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.target_temperature = temperature
    db.commit()
    return {"message": "Target temperature set"}

@router.post("/{room_number}/set_wind_speed")
def set_wind_speed(room_number: int, wind_speed: WindSpeedEnum, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_number == room_number).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.wind_speed == wind_speed.value:
        raise HTTPException(status_code=400, detail="Wind speed is already set to this value")
    room.wind_speed = wind_speed.value
    db.commit()
    return {"message": "Wind speed set"}

@router.post("/{room_number}/set_mode")
def set_mode(room_number: int, mode: ModeEnum, db: Session = Depends(get_db)):
    room = db.query(RoomModel).filter(RoomModel.room_number == room_number).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.mode == mode.value:
        raise HTTPException(status_code=400, detail="Mode is already set to this value")
    room.mode = mode.value
    db.commit()
    return {"message": "Mode set"}
