# 引入我们的“邮递员”
import requests
# 引入json模块，方便我们把字典变成JSON字符串
import json 

# 定义Ollama的API地址
OLLAMA_URL = "http://localhost:11434/api/chat"

# 准备我们要发送的“信件内容”（请求体）
while True:
    user_message = input("请输入：")
    if user_message == "exit":
        break
    payload = {
        "model": "qwen2.5:7b",      # 使用你部署的qwen2.5模型
        "messages": [{"role": "user", "content": user_message}],  # 你的问题
        "stream": False           # 关闭流式输出，等它全部想好再一次性返回
    }
    try:
    # 邮递员出发！发送POST请求，超时时间设为60秒（大模型思考需要时间）
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
    #post请求 发送POST请求，将payload作为JSON体发送到OLLAMA_URL
    # 检查信件是否成功送达（状态码200表示成功）
        response.raise_for_status()
    #raise_for_status() 检查响应状态码是否为200，如果不是200，抛出异常，否则继续执行
    # 解析Ollama的回信
        result = response.json()
    #json() 解析响应体为JSON格式，返回一个字典
    #result 包含Ollama的回信，包括回答、状态码等
    # 打印出大模型的回答
        print("🤖 Ollama回答：", result["message"]["content"],result.get("response", "没有获取到回答"))
    #get() 从字典中获取指定键对应的值，如果键不存在，返回默认值"没有获取到回答"
    #result.get("response") 获取回答，如果回答不存在，返回"没有获取到回答"
    #print() 打印回答，如果回答存在，打印回答，否则打印"没有获取到回答"
    except requests.exceptions.ConnectionError:
    #except requests.exceptions.ConnectionError 捕获连接错误异常
    # 如果连不上，通常是Ollama没启动
        print("❌ 连接失败！请检查Ollama是否正在运行（终端输入 ollama serve）")
    except Exception as e:
    #except Exception as e 捕获其他未知错误
        print(f"❌ 发生未知错误：{e}")
    #print() 打印错误信息，包括错误类型和错误详情
    #e 错误对象，包含错误类型、错误信息等
    #f"❌ 发生未知错误：{e}" 格式化字符串，将错误对象转换为字符串，包含错误类型和错误信息



    



