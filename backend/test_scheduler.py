# tests/test_scheduler.py
import pytest
from fastapi.testclient import TestClient
from .main import app
from .database import SessionLocal
from .models import RoomModel
import time

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_rooms():
    # 初始化测试数据
    db = SessionLocal()
    rooms = db.query(RoomModel).all()
    for room in rooms:
        room.open = 0  # 重置 open 计数
    db.commit()
    db.close()

def test_simulate_step(setup_rooms):
    # 获取房间信息前的 open 值
    response_before = client.get("/api/room_info")
    assert response_before.status_code == 200
    rooms_before = response_before.json()
    open_before = {room["roomNumber"]: room["open"] for room in rooms_before}
    time.sleep(12)  # 等待超过调度间隔，确保 simulate_step 被调用

    # 获取房间信息后的 open 值
    response_after = client.get("/api/room_info")
    assert response_after.status_code == 200
    rooms_after = response_after.json()
    open_after = {room["roomNumber"]: room["open"] for room in rooms_after}

    # 检查 open 值是否增加
    for room_number in open_before:
        assert open_after[room_number] == open_before[room_number] + 1, f"Room {room_number} open count did not increase as expected."
