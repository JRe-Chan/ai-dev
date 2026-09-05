import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"

def smart_chat():
    print("🚀 欢迎使用 Smart Chat CLI！")
    model = input("请输入模型名称 (默认 qwen2.5:7b): ") or "qwen2.5:7b"
    temp = float(input("请输入Temperature(人类思维深度) 0.0-1.0 (默认 0.7): ") or "0.7")
    
    history = [{"role": "system", "content": "你是一个聪明、友善的AI助手。"}]
    
    print(f"\n✅ 已配置: 模型={model}, Temperature={temp}")
    print("💡 提示: 输入 'quit' 退出, 输入 'clear' 清空历史\n")
    
    while True:
        user_input = input("👤 你: ")
        if user_input.lower() == "quit":
            print("👋 拜拜！")
            break
        if user_input.lower() == "clear":
            history = [history[0]] # 保留system prompt
            print("🧹 历史已清空！")
            continue
            
        history.append({"role": "user", "content": user_input})
        payload = {
            "model": model, 
            "messages": history, 
            "stream": True, 
            "options": {"temperature": temp}
        }
        
        print("🤖 Ollama: ", end="", flush=True) #flush=True 确保立即打印
        full_response = "" #full_response 用于存储完整的响应
        try:
            resp = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
            resp.raise_for_status()
            #resp.raise_for_status() 会抛出异常，如果响应状态码是4xx, 5xx
            for line in resp.iter_lines(): # 遍历响应的每一行
                if line: # 确保行不是空的
                    chunk = json.loads(line) # 解析行中的JSON
                    # 从JSON中提取"response"字段，如果不存在则返回空字符串
                    token = chunk.get("message", {}).get("content", "")
                    print(token, end="", flush=True) #flush=True 确保立即打印
                    full_response += token # 累加响应到full_response中
            print() # 换行
            history.append({"role": "assistant", "content": full_response})
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            history.pop()

if __name__ == "__main__":
    smart_chat()