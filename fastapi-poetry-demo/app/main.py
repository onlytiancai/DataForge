from os import path

from fastapi import FastAPI
import uvicorn
import redis.asyncio as redis

from starlette.middleware.cors import CORSMiddleware

from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
import logging

# 设置 Tortoise-ORM 的日志级别为 DEBUG
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("tortoise").setLevel(logging.DEBUG)

from app.configs.app import get_app_settings
from app.configs.db import get_db_settings

from app.routers import include_router

app_settings = get_app_settings()
db_settings = get_db_settings()


# 初始化服务端应用
def create_app():
    # 创建fastapi
    _app = FastAPI(
        title=app_settings.APP_TITLE,
        description=app_settings.APP_DESCRIPTION
    )

    # 添加CORS中间件
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # 导入路由
    include_router(_app)

    # 注册Tortoise ORM
    register_tortoise(
        _app,
        generate_schemas=True,
        add_exception_handlers = False,
        config={
            "connections": {
                "default": db_settings.DATABASE_DSN,
            },
            "apps": {"models": {"models": ["app.models"]}},
            "use_tz": False,
            "timezone": app_settings.TIME_ZONE,
        }
    )

    return _app


app = create_app()