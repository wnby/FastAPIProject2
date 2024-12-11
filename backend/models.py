# backend/models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class RoomModel(Base):
    __tablename__ = "rooms"
    room_number = Column(Integer, primary_key=True, index=True)
    is_powered_on = Column(Boolean, default=False)
    current_temperature = Column(Float, default=25.0)
    target_temperature = Column(Float, default=25.0)
    mode = Column(String, default="Cooling")  # "Cooling" or "Heating"
    wind_speed = Column(String, default="Medium")  # "Low","Medium","High"
    cost_rate = Column(Float, default=1.0)
    otem = Column(Float, default=25.0)
    gtem = Column(Float, default=25.0)
    ntem = Column(Float, default=25.0)
    open_status = Column(Integer, default=0)  # Renamed from 'open' to 'open_status'
    wtime = Column(Integer, default=0)
    otime = Column(Integer, default=0)
    retime = Column(Integer, default=0)
    speed = Column(Integer, default=2)  # 对应风速档次 1=Low,2=Medium,3=High
    w = Column(Float, default=0.0)  # 累积费用

    bookings = relationship("Booking", back_populates="room")

class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    id_number = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    bookings = relationship("Booking", back_populates="guest")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(Integer, ForeignKey("rooms.room_number"))
    guest_id = Column(Integer, ForeignKey("guests.id"))
    checkin_time = Column(DateTime, default=datetime.utcnow)
    checkout_time = Column(DateTime, nullable=True)
    total_cost = Column(Float, default=0.0)
    status = Column(String, default="checked_in")  # "checked_in","checked_out"

    room = relationship("RoomModel", back_populates="bookings")
    guest = relationship("Guest", back_populates="bookings")
