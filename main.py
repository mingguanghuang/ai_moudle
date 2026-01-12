import time
import json
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel
from langchain_core.tracers.stdout import elapsed
from pydantic import BaseModel
from fastapi.responses import FileResponse
from utils.logger import setup_logger
from agent_pro.agent import Agent
from models.models import Models,ALI_TONGYI_DEEPSEEK_V3_2,ALI_TONGYI_DEEPSEEK_V3
from utils.mqtt_client import MQTTClient

app = FastAPI()

class ChatRequest(BaseModel):
    model: str = ALI_TONGYI_DEEPSEEK_V3
    message: str
#前端测试页面,这里你可以自己定义测试页面
@app.get("/")
async def read_index():
    return FileResponse("index.html")

@app.post("/api/chat")
def chat(request: ChatRequest):

    try:
        start = time.time()
        model = request.model
        user_prompt = request.message
        my_agent = Agent(model,user_prompt)
        result = my_agent.agent_run_parse()
        print(result)
        elapse = time.time() - start
        logger.info(f"成功处理请求，耗时{elapse:.2f}秒")
        return {
            "success": True,
            "processing_time": f"{elapse:.2f}s",
            "result": result
        }
    except Exception as e:
        logger.error(f"处理请求时出错: {e}")
        return {
            "success": False,
            "error": str(e)
        }
if __name__ == "__main__":
    setup_logger()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)