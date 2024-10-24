
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from celery.result import AsyncResult
from celery_app import celery_app
from celery_app import run_command


app = FastAPI()

class UserInfo(BaseModel):
    roles: List[str] = []
    realName: str

class HttpResponse(BaseModel):
    code: int
    message: str
    data: UserInfo


@app.get("/api/user/info")
async def get_user_info():
    return HttpResponse(
        code=0,
        message="ok",
        data=UserInfo(
            roles=["admin", "user"], 
            realName="John Doe"
        ),
    )

@app.get("/submit-task/")
def submit_task():
    task = run_command.apply_async(args=[])
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.state == 'SUCCESS':
        return {"task_id": task_id, "status": task_result.state, "result": task_result.result}
    elif task_result.state == 'PROGRESS':
        return {
            "task_id": task_id,
            "status": task_result.state,
            "current": task_result.info.get('current', 0),
            "partial_result": task_result.info.get('result')
        }
    else:
        return {"task_id": task_id, "status": task_result.state}
