# backend/scheduler.py
import logging
from .models import RoomModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .schemas import Room, ModeEnum, WindSpeedEnum
import asyncio
from .routers.websocket import manager
import json
from .config import scheduler_settings

logger = logging.getLogger(__name__)

# 常量定义
COOLING_DELTA_LOW = scheduler_settings.cooling_delta_low
COOLING_DELTA_MEDIUM = scheduler_settings.cooling_delta_medium
COOLING_DELTA_HIGH = scheduler_settings.cooling_delta_high
DEFAULT_DELTA = scheduler_settings.default_delta
TEMP_REGRESSION_RATE = scheduler_settings.temp_regression_rate

# 风速对应的速度值
SPEED_MAPPING = {
    1: 0.333,
    2: 0.5,
    3: 1.0
}

# 全局变量模拟C++中的数组索引从1开始
ROOM_COUNT = 5

def chaozuoni(step: int, rooms: dict):
    """
    根据步数执行不同的操作，模拟C++中的chaozuoni函数。
    """
    # 根据用户提供的C++代码，将每个步骤的操作转换为Python逻辑
    if step == 1:
        rooms[101].is_powered_on = True
    elif step == 2:
        rooms[102].is_powered_on = True
        rooms[101].gtem = 24
    elif step == 3:
        rooms[103].is_powered_on = True
    elif step == 4:
        rooms[102].gtem = 25
        rooms[104].is_powered_on = True
        rooms[105].is_powered_on = True
    elif step == 5:
        rooms[103].gtem = 25
        rooms[105].speed = 3
    elif step == 6:
        rooms[101].speed = 3
    elif step == 7:
        pass
    elif step == 8:
        rooms[105].gtem = 24
    elif step == 9:
        pass
    elif step == 10:
        rooms[101].gtem = 25
        rooms[104].gtem = 25
        rooms[104].speed = 3
    elif step == 11:
        pass
    elif step == 12:
        rooms[105].speed = 2
    elif step == 13:
        rooms[102].speed = 3
    elif step == 14:
        pass
    elif step == 15:
        rooms[101].is_powered_on = False
        rooms[103].speed = 1
    elif step == 16:
        pass
    elif step == 17:
        rooms[105].is_powered_on = False
    elif step == 18:
        rooms[103].speed = 3
    elif step == 19:
        rooms[101].is_powered_on = True
        rooms[104].gtem = 25
        rooms[104].speed = 2
    elif step == 20:
        pass
    elif step == 21:
        rooms[102].gtem = 25
        rooms[102].speed = 2
        rooms[105].is_powered_on = True
    elif step == 22:
        pass
    elif step == 23:
        pass
    elif step == 24:
        pass
    elif step == 25:
        rooms[101].is_powered_on = False
        rooms[103].is_powered_on = False
        rooms[105].is_powered_on = False
    elif step == 26:
        rooms[102].is_powered_on = False
        rooms[104].is_powered_on = False
    elif step == 27:
        pass
    else:
        pass

async def simulate_step(step: int, db: Session):
    """
    模拟调度步骤，调整每个房间的温度和费用。
    """
    try:
        # 查询所有房间
        rooms = db.query(RoomModel).all()
        rooms_dict = {room.room_number: room for room in rooms}

        # 执行chaozuoni操作
        chaozuoni(step, rooms_dict)

        # 模拟C++逻辑中的变量
        option = {room.room_number: 0 for room in rooms}
        wait = {room.room_number: 0 for room in rooms}
        re = {room.room_number: 0 for room in rooms}
        optionnet = 0
        waitnet = 0

        # 根据C++逻辑处理开关机和等待队列
        for room_number, room in rooms_dict.items():
            if room.is_powered_on and not (option[room_number] or wait[room_number]):
                if optionnet < 3:
                    option[room_number] = 1
                    optionnet += 1
                else:
                    wait[room_number] = 1

        # 更新温度和费用
        for room_number, room in rooms_dict.items():
            if room.is_powered_on:
                delta = SPEED_MAPPING.get(room.speed, DEFAULT_DELTA)
                if room.mode == ModeEnum.COOLING and room.current_temperature > room.target_temperature:
                    temp_change = min(delta, room.current_temperature - room.target_temperature)
                    room.current_temperature -= temp_change
                    room.w += room.cost_rate * temp_change
                elif room.mode == ModeEnum.HEATING and room.current_temperature < room.target_temperature:
                    temp_change = min(delta, room.target_temperature - room.current_temperature)
                    room.current_temperature += temp_change
                    room.w += room.cost_rate * temp_change
            else:
                # 温度回归
                if room.current_temperature > room.otem:
                    room.current_temperature = max(room.current_temperature - TEMP_REGRESSION_RATE, room.otem)
                elif room.current_temperature < room.otem:
                    room.current_temperature = min(room.current_temperature + TEMP_REGRESSION_RATE, room.otem)

        db.commit()

        # 获取最新的房间数据并广播
        updated_rooms = db.query(RoomModel).all()
        rooms_data = [Room.from_orm(room).dict() for room in updated_rooms]
        await manager.broadcast(json.dumps(rooms_data))
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error during simulate_step {step}: {e}")
    except Exception as e:
        db.rollback()
        logger.exception(f"Unexpected error during simulate_step {step}: {e}")
