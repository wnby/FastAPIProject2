# minimal_main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Room(BaseModel):
    roomNumber: int
    isPoweredOn: bool
    currentTemperature: float
    targetTemperature: float
    mode: str
    windSpeed: str
    costRate: float
    otem: float
    gtem: float
    ntem: float
    open: int
    wtime: int
    otime: int
    retime: int
    speed: int
    w: float

class CheckInRequest(BaseModel):
    room_number: int
    guest_name: str
    guest_id_number: str

@app.get("/api/room_info", response_model=List[Room])
def get_room_info():
    # 返回一些示例房间数据
    rooms = [
        Room(
            roomNumber=101,
            isPoweredOn=False,
            currentTemperature=25.0,
            targetTemperature=25.0,
            mode="Cooling",
            windSpeed="Medium",
            costRate=1.0,
            otem=10.0,
            gtem=22.0,
            ntem=10.0,
            open=0,
            wtime=0,
            otime=0,
            retime=0,
            speed=2,
            w=0.0
        ),
        Room(
            roomNumber=102,
            isPoweredOn=True,
            currentTemperature=23.0,
            targetTemperature=23.0,
            mode="Heating",
            windSpeed="High",
            costRate=1.5,
            otem=15.0,
            gtem=20.0,
            ntem=15.0,
            open=1,
            wtime=0,
            otime=0,
            retime=0,
            speed=3,
            w=0.0
        )
    ]
    return rooms

@app.post("/api/checkin")
def checkin(request: CheckInRequest):
    # 返回成功响应
    return {
        "message": "Check-in successful",
        "booking_id": 1,
        "guest_id": 1
    }
