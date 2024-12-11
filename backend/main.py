# backend/main.py
from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from .init_rooms import init_rooms
from .routers import rooms, bookings, guests, websocket
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .scheduler import simulate_step
from fastapi.middleware.cors import CORSMiddleware
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 配置CORS
origins = ["*"]  # 生产环境建议限制为特定域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化房间数据
def startup_event():
    db = SessionLocal()
    try:
        init_rooms(db)
        logger.info("房间初始化完成。")
    except Exception as e:
        logger.exception(f"房间初始化失败: {e}")
    finally:
        db.close()

app.add_event_handler("startup", startup_event)

# 包含所有路由
app.include_router(rooms.router, prefix="/api/rooms", tags=["Rooms"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(guests.router, prefix="/api/guests", tags=["Guests"])
app.include_router(websocket.router, prefix="/api", tags=["WebSocket"])

# 调度器设置
scheduler = AsyncIOScheduler()
step_counter = 1  # 全局步数计数器

@app.on_event("startup")
async def start_scheduler():
    global step_counter
    scheduler.add_job(
        simulate_step_wrapper,
        'interval',
        seconds=10,  # 调度间隔，根据需求调整
        id='simulate_step_job',
        replace_existing=True
    )
    scheduler.start()
    logger.info("APScheduler AsyncIOScheduler 已启动。")

async def simulate_step_wrapper():
    global step_counter
    db = SessionLocal()
    try:
        await simulate_step(step_counter, db)
    finally:
        db.close()

    step_counter += 1
    if step_counter > 27:  # 假设步数最大为27，您可以根据需求调整
        step_counter = 1  # 重置步数

@app.get("/")
def root():
    return {"message": "Welcome to the Hotel Management API"}
