import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

app = FastAPI(title="AI Chat API", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "你是一个有帮助的AI助手。"
    stream: bool = False

class ChatResponse(BaseModel):
    reply: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

async def _call_api(messages: list, stream: bool = False): # 异步调用 DeepSeek API
    """统一调用 DeepSeek API"""
    client = httpx.AsyncClient() # 异步 HTTP 客户端
    if stream: # 流式响应
        return client.stream(    
            "POST", f"{BASE_URL}/chat/completions", # 流式响应
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},  # 流式响应头
            json={"model": "deepseek-chat", "messages": messages, "stream": True, "temperature": 0.7}, # 流式响应参数
            timeout=60.0 # 超时时间, 单位秒, 60 秒
        )
    else: # 非流式响应
        response = await client.post(    
            f"{BASE_URL}/chat/completions", # 非流式响应，
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}, # 非流式响应头
            json={"model": "deepseek-chat", "messages": messages, "temperature": 0.7, "max_tokens": 1000}, # 非流式响应参数
            timeout=60.0 # 超时时间, 单位秒, 60 秒
        )
        response.raise_for_status() # 检查响应状态码, 如果不是 200, 则抛出异常
        return response.json() # 返回 JSON 数据

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest): # 异步处理请求
    if not API_KEY:  # 检查 API Key 是否配置
        raise HTTPException(status_code=500, detail="API Key 未配置") # 如果未配置, 则抛出异常
    
    messages = [
        {"role": "system", "content": req.system_prompt},  # 系统提示
        {"role": "user", "content": req.message}  # 用户消息
    ]
    
    if req.stream: # 流式响应
        async def generate(): # 流式响应函数
            async with await _call_api(messages, stream=True) as response: # 异步流响应
                response.raise_for_status() # 检查响应状态码, 如果不是 200, 则抛出异常
                async for line in response.aiter_lines(): # 遍历响应行
                    if line.startswith("data: "): # 过滤出 data 行
                        data_str = line[6:] # 去掉 data: 前缀
                        if data_str == "[DONE]": # 处理完成标志
                            yield f"data: {json.dumps({'done': True})}\n\n" # 返回完成标志
                            break
                        try: # 解析 JSON 字符串
                            chunk = json.loads(data_str) # 解析 JSON 字符串
                            if "content" in chunk["choices"][0]["delta"]: # 检查是否有 content 字段
                                content = chunk["choices"][0]["delta"]["content"]  # 提取 content 字段
                                yield f"data: {json.dumps({'token': content}, ensure_ascii=False)}\n\n" # 返回 token
                        except:
                            continue
        return StreamingResponse(generate(), media_type="text/event-stream") # 返回流式响应
    
    else: # 非流式响应
        data = await _call_api(messages, stream=False) # 调用 DeepSeek API, 非流式响应
        return ChatResponse(      
            reply=data["choices"][0]["message"]["content"],  # 提取回复内容
            prompt_tokens=data["usage"]["prompt_tokens"],  # 提取 prompt_tokens
            completion_tokens=data["usage"]["completion_tokens"],  # 提取 completion_tokens
            total_tokens=data["usage"]["total_tokens"]  # 提取 total_tokens
        )

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)