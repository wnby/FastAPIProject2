# test_scheduler.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock, patch
from backend.models import Base, RoomModel
from backend.scheduler import simulate_step
from backend.config import scheduler_settings
import json

# 创建一个内存数据库引擎
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建所有表
Base.metadata.create_all(bind=engine)

# 定义房间号
ROOM_NUMBERS = [101, 102, 103, 104, 105]

# 定义每个步骤的预期更改
STEP_EXPECTATIONS = {
    1: {"is_powered_on": {101: True}},
    2: {"is_powered_on": {102: True}, "gtem": {101: 24.0}},
    3: {"is_powered_on": {103: True}},
    4: {"is_powered_on": {104: True, 105: True}, "gtem": {102: 25.0}},
    5: {"gtem": {103: 25.0}, "speed": {105: 3}},
    6: {"speed": {101: 3}},
    7: {},  # 无操作
    8: {"gtem": {105: 24.0}},
    9: {},  # 无操作
    10: {"gtem": {101: 25.0, 104: 25.0}, "speed": {104: 3}},
    11: {},  # 无操作
    12: {"speed": {105: 2}},
    13: {"speed": {102: 3}},
    14: {},  # 无操作
    15: {"is_powered_on": {101: False}, "speed": {103: 1}},
    16: {},  # 无操作
    17: {"is_powered_on": {105: False}},
    18: {"speed": {103: 3}},
    19: {"is_powered_on": {101: True}, "gtem": {104: 25.0}, "speed": {104: 2}},
    20: {},  # 无操作
    21: {"gtem": {102: 25.0}, "speed": {102: 2}, "is_powered_on": {105: True}},
    22: {},  # 无操作
    23: {},  # 无操作
    24: {},  # 无操作
    25: {"is_powered_on": {101: False, 103: False, 105: False}},
    26: {"is_powered_on": {102: False, 104: False}},
    27: {},  # 无操作
}

@pytest.fixture(scope="module")
def db():
    """
    创建一个新的数据库会话用于测试。
    """
    db = TestingSessionLocal()
    try:
        # 初始化五个房间
        rooms = [
            RoomModel(
                room_number=101,
                is_powered_on=False,
                current_temperature=25.0,
                target_temperature=22.0,
                gtem=22.0,
                mode="Cooling",
                wind_speed="Medium",
                speed=2,
                cost_rate=1.0,
                w=0.0,
                otem=25.0,
                ntem=25.0,
                open_status=0,
                wtime=0,
                otime=0,
                retime=0,
            ),
            RoomModel(
                room_number=102,
                is_powered_on=False,
                current_temperature=25.0,
                target_temperature=22.0,
                gtem=22.0,
                mode="Cooling",
                wind_speed="Medium",
                speed=2,
                cost_rate=1.0,
                w=0.0,
                otem=25.0,
                ntem=25.0,
                open_status=0,
                wtime=0,
                otime=0,
                retime=0,
            ),
            RoomModel(
                room_number=103,
                is_powered_on=False,
                current_temperature=25.0,
                target_temperature=22.0,
                gtem=22.0,
                mode="Cooling",
                wind_speed="Medium",
                speed=2,
                cost_rate=1.0,
                w=0.0,
                otem=25.0,
                ntem=25.0,
                open_status=0,
                wtime=0,
                otime=0,
                retime=0,
            ),
            RoomModel(
                room_number=104,
                is_powered_on=False,
                current_temperature=25.0,
                target_temperature=22.0,
                gtem=22.0,
                mode="Cooling",
                wind_speed="Medium",
                speed=2,
                cost_rate=1.0,
                w=0.0,
                otem=25.0,
                ntem=25.0,
                open_status=0,
                wtime=0,
                otime=0,
                retime=0,
            ),
            RoomModel(
                room_number=105,
                is_powered_on=False,
                current_temperature=25.0,
                target_temperature=22.0,
                gtem=22.0,
                mode="Cooling",
                wind_speed="Medium",
                speed=2,
                cost_rate=1.0,
                w=0.0,
                otem=25.0,
                ntem=25.0,
                open_status=0,
                wtime=0,
                otime=0,
                retime=0,
            ),
        ]
        db.add_all(rooms)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture
def mock_broadcast():
    with patch("backend.routers.websocket.manager.broadcast", new_callable=AsyncMock) as mock:
        yield mock

@pytest.mark.asyncio
@pytest.mark.parametrize("step", range(1, 28))  # 步骤1至27
async def test_simulate_step(db, mock_broadcast, step):
    """
    参数化测试 simulate_step 函数的不同步骤。
    """
    print(f"\n--- 测试步骤 {step} ---")
    await simulate_step(step, db)

    # 获取预期的更改
    expectations = STEP_EXPECTATIONS.get(step, {})

    for attr, changes in expectations.items():
        for room_number, expected_value in changes.items():
            room = db.query(RoomModel).filter(RoomModel.room_number == room_number).first()
            actual_value = getattr(room, attr)
            assert actual_value == expected_value, (
                f"步骤 {step}：房间 {room_number} 的 {attr} 应为 {expected_value}，实际为 {actual_value}"
            )
            print(f"房间 {room_number} 的 {attr} 已正确设置为 {expected_value}")

    # 验证 broadcast 被调用
    if expectations:
        mock_broadcast.assert_called()

@pytest.mark.asyncio
async def test_temperature_adjustment(db, mock_broadcast):
    """
    测试 simulate_step 函数中温度调整的逻辑。
    """
    print("\n--- 测试温度调整逻辑 ---")

    # 设置房间101的当前温度高于目标温度
    room101 = db.query(RoomModel).filter(RoomModel.room_number == 101).first()
    room101.current_temperature = 24.0  # 高于目标22°C
    db.commit()

    # 执行步骤1，假设对房间101有影响
    await simulate_step(1, db)

    # 重新获取房间101
    room101 = db.query(RoomModel).filter(RoomModel.room_number == 101).first()

    # 目标温度为22°C，当前温度应下降
    assert room101.current_temperature < 24.0, "房间101的当前温度应下降"
    print(f"房间101的当前温度已调整为 {room101.current_temperature}°C")

    # 验证费用计算
    expected_w = scheduler_settings.cost_rate * (24.0 - room101.gtem)  # cost_rate * temp_change
    assert room101.w >= expected_w, "房间101的费用应正确计算"
    print(f"房间101的费用已更新为 {room101.w}")

    # 验证 broadcast 被调用
    mock_broadcast.assert_called()
