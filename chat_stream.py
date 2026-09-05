import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5:7b",
    "prompt": "给我讲一个关于程序员的笑话。",
    "stream": True  # ⚠️ 关键：开启流式输出
}

print("🤖 Ollama: ", end="", flush=True) # end="" 防止自动换行，flush=True 强制立刻显示

try:
    # stream=True 会让 requests 以迭代的方式接收数据
    response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
    response.raise_for_status()
    
    # 逐行读取响应
    for line in response.iter_lines():
        if line:
            # 每一行都是一个JSON字符串，我们需要解析它
            chunk = json.loads(line)
            # 打印出这一小块内容，不换行
            print(chunk.get("response", ""), end="", flush=True)
            
    print() # 全部输出完后，最后换一次行
            
except Exception as e:
    print(f"\n❌ 出错啦：{e}")