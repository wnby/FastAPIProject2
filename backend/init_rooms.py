# backend/init_rooms.py
from sqlalchemy.orm import Session
from .models import RoomModel
from enum import Enum

class ModeEnum(str, Enum):
    COOLING = "Cooling"
    HEATING = "Heating"

def init_rooms(db: Session):
    room_numbers = [101, 102, 103, 104, 105]
    existing_rooms = db.query(RoomModel).filter(RoomModel.room_number.in_(room_numbers)).all()
    existing_room_numbers = [room.room_number for room in existing_rooms]

    # 根据C++代码中的初始数据
    initial_data = {
        101: {"otem": 10, "gtem": 22, "ntem": 10, "open_status": 0, "speed": 2, "mode": "Cooling"},
        102: {"otem": 15, "gtem": 22, "ntem": 15, "open_status": 0, "speed": 2, "mode": "Cooling"},
        103: {"otem": 18, "gtem": 22, "ntem": 18, "open_status": 0, "speed": 2, "mode": "Cooling"},
        104: {"otem": 12, "gtem": 22, "ntem": 12, "open_status": 0, "speed": 2, "mode": "Cooling"},
        105: {"otem": 14, "gtem": 22, "ntem": 14, "open_status": 0, "speed": 2, "mode": "Cooling"},
    }

    for room_number in room_numbers:
        if room_number not in existing_room_numbers:
            data = initial_data.get(room_number, {})
            room = RoomModel(
                room_number=room_number,
                is_powered_on=False,
                current_temperature=data.get("ntem", 25.0),
                target_temperature=data.get("gtem", 25.0),
                mode=data.get("mode", "Cooling"),
                wind_speed="Medium",  # 初始风速中
                cost_rate=1.0,  # 根据需求调整
                otem=data.get("otem", 25.0),
                gtem=data.get("gtem", 25.0),
                ntem=data.get("ntem", 25.0),
                open_status=data.get("open_status", 0),
                wtime=0,
                otime=0,
                retime=0,
                speed=data.get("speed", 2),
                w=0.0
            )
            db.add(room)
    db.commit()
