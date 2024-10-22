import subprocess
from fastapi import FastAPI, HTTPException
from starlette.responses import StreamingResponse
import time

app = FastAPI()

# 生成器函数，用于逐行返回命令的输出
def run_command():
    process = subprocess.Popen(
        ["mysqlsh", "--help"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,  # 捕获标准错误并将其与标准输出合并
        text=True, 
        bufsize=1  # 行缓冲
    )
    
    # 逐行读取并返回命令输出
    for line in iter(process.stdout.readline, ''):        
        yield line
        time.sleep(0.1)
    
    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        yield f"\nCommand exited with return code {process.returncode}"

@app.get("/api/run-mysqlsh-help/")
async def run_mysqlsh_help():
    try:
        return StreamingResponse(run_command(), media_type="text/plain")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="mysqlsh command not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
