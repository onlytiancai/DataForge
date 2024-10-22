import subprocess
from fastapi import FastAPI, HTTPException
from typing import Union

app = FastAPI()

@app.get("/api/run-mysqlsh-help/")
async def run_mysqlsh_help():
    try:
        # 执行 'mysqlsh --help' 命令
        result = subprocess.run(
            ["mysqlsh", "--help"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # 如果命令执行失败，返回错误信息
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error executing command: {result.stderr}")
        
        # 返回命令输出
        return {"output": result.stdout}
    except FileNotFoundError:
        # 如果系统中没有安装 mysqlsh，返回错误信息
        raise HTTPException(status_code=404, detail="mysqlsh command not found")
    except Exception as e:
        # 处理其他异常
        raise HTTPException(status_code=500, detail=str(e))
