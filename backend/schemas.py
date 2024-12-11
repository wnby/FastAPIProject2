# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime
from .enums import ModeEnum, WindSpeedEnum  # 确保正确导入枚举

class Room(BaseModel):
    room_number: int
    is_powered_on: bool
    current_temperature: float
    target_temperature: float
    mode: ModeEnum
    wind_speed: WindSpeedEnum
    cost_rate: float
    otem: float
    gtem: float
    ntem: float
    open_status: int
    wtime: int
    otime: int
    retime: int
    speed: int
    w: float  # 累积费用

    class Config:
        from_attributes = True  # 替换 orm_mode

class Guest(BaseModel):
    id: int
    name: str
    id_number: str
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # 替换 orm_mode

class Booking(BaseModel):
    id: int
    room_number: int
    guest_id: int
    checkin_time: datetime
    checkout_time: Optional[datetime]
    total_cost: float
    status: str  # "checked_in","checked_out"

    room: Room
    guest: Guest

    class Config:
        from_attributes = True  # 替换 orm_mode

# 请求体模型
class BookingCreate(BaseModel):
    room_number: int
    guest_id: int

class GuestCreate(BaseModel):
    name: str
    id_number: str
    phone: Optional[str] = None
