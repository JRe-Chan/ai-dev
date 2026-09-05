import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat" 
# 注意：多轮对话推荐使用 /api/chat 接口

# 设定System Prompt，给模型一个“人设”
SYSTEM_PROMPT = "你是一个耐心、幽默的AI编程导师，回答要通俗易懂，多用比喻。"

# 初始化对话历史，把“人设”放进去
history = [
    {"role": "system", "content": SYSTEM_PROMPT}
    #role 角色，system 是系统角色，content 是系统提示
    # 这里把系统提示也加入历史，方便模型记住“人设”
]

print("💬 多轮对话已开启！输入 'quit' 退出。")

while True:
    user_input = input("\n👤 你: ")
    if user_input.lower() == "quit":
        #lower() 把用户输入转换为小写，确保不区分大小写
        print("👋 再见！")
        break
        
    # 把用户的新问题加入历史
    history.append({"role": "user", "content": user_input})
    #role 角色，user 是用户角色，content 是用户输入
    # 这里把用户输入也加入历史，方便模型记住用户的问题
    
    payload = {
        "model": "qwen2.5:7b",
        "messages": history, # 把完整的历史记录发给模型
        "stream": False
        # 关闭流式输出，等它全部想好再一次性返回
    }
    
    try:
        #try 尝试发送POST请求
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        #post请求 发送POST请求，将payload作为JSON体发送到OLLAMA_URL
        # 检查信件是否成功送达（状态码200表示成功）
        response.raise_for_status()
        #raise_for_status() 检查响应状态码是否为200，如果不是200，抛出异常，否则继续执行
        # 解析Ollama的回信
        result = response.json()
        #json() 解析响应体为JSON格式，返回一个字典
        #result 包含Ollama的回信，包括回答、状态码等
        # 获取模型的回复
        assistant_message = result["message"]["content"]
        #result["message"]["content"] 获取模型的回答
        #message 是模型的回复，包含角色、内容等,content 是模型的回答    
        print(f"🤖 Ollama: {assistant_message}")
        
        # 把模型的回复也加入历史，这样下一轮它就能记住了
        history.append({"role": "assistant", "content": assistant_message})
        
    except Exception as e:
        print(f"❌ 出错啦：{e}")
        # 出错了就把刚才加的用户提问删掉，防止污染历史
        history.pop()