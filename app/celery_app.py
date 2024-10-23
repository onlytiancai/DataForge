from celery import Celery
import subprocess
import time

# 配置Celery应用，使用Redis作为消息队列
celery_app = Celery(
    'worker',
    broker='redis://localhost:6379/1',
    backend='redis://localhost:6379/1'
)

@celery_app.task(bind=True)
def run_command(self):
    process = subprocess.Popen(
        ["mysqlsh", "--help"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,  # 捕获标准错误并将其与标准输出合并
        text=True, 
        bufsize=1  # 行缓冲
    )

    ret = ''
    for i, line in enumerate(iter(process.stdout.readline, '')):
        ret += line
        self.update_state(state='PROGRESS', meta={'current': i, 'result': ret})
        time.sleep(0.5)
    
    process.stdout.close()
    process.wait()

    if process.returncode != 0:
        return f"\nCommand exited with return code {process.returncode}"
    else:
        return ret
