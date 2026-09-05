import aiohttp
import asyncio
import time

OLLAMA_URL = "http://localhost:11434/api/generate"

async def ask_question(session, question):
    # 定义一个异步函数，用于与Ollama交互
    # 它接受一个会话对象（session）和一个问题（question）作为参数
    # 返回一个字符串，包含问题和回答
    """异步发送单个问题"""
    # 准备我们要发送的“信件内容”（请求体）
    payload = {
        "model": "qwen2.5:7b",
        "prompt": question,
        "stream": False
    }
    try:
        # 发送POST请求，超时时间设为120秒（大模型思考需要时间）
        async with session.post(OLLAMA_URL, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as resp:
            #async with 语句 确保会话在使用后被正确关闭 ,aiohttp.ClientTimeout(total=120) 超时时间设为120秒,as resp 表示将响应赋值给resp变量
            # 等待服务器响应，解析为JSON格式
            result = await resp.json()
            #result 包含Ollama的回信，包括回答、状态码等
            return f"❓ {question}\n🤖 {result.get('response', '无回答')}\n"
            #return 返回包含问题和回答的字符串
            #result.get('response', '无回答') 获取回答，如果回答不存在，返回"无回答"
    except Exception as e:
        # 捕获其他未知错误
        return f"❓ {question}\n❌ 出错: {e}\n"
        #return 返回包含问题和错误信息的字符串
        #e 错误对象，包含错误类型、错误信息等
        #f"❓ {question}\n❌ 出错: {e}" 格式化字符串，将问题和错误信息转换为字符串，包含问题、错误类型和错误信息

async def main(): # 主函数，用于异步发送多个问题
    """异步发送多个问题"""
    questions = ["我叫艾可可", "我的狗叫叮叮", "我叫什么？", "我的狗叫什么？"]
       # 定义要发送的问题列表
    
    start_time = time.time()
    # 创建一个共享的会话
    async with aiohttp.ClientSession() as session:
        # 并发执行所有问题！
        tasks = [ask_question(session, q) for q in questions]
        #for q in questions 遍历问题列表，为每个问题创建一个异步任务
        #ask_question(session, q) 调用异步函数ask_question，将会话对象和问题作为参数
        # 生成一个包含所有问题的异步任务列表
        # 每个任务都是一个异步函数调用，用于与Ollama交互
        # 等待所有任务完成，返回一个包含所有结果的列表
        results = await asyncio.gather(*tasks)
        #await asyncio.gather(*tasks) 等待所有任务完成，返回一个包含所有结果的列表
        #results 包含所有问题的回答或错误信息
        #*tasks 展开任务列表，将每个任务作为参数传递给gather函数,* 表示将任务列表展开为多个参数
    end_time = time.time()
    # 记录结束时间,time.time() 返回当前时间戳，单位为秒
    #end_time - start_time 计算异步总耗时，单位为秒
    
    for res in results:
        print(res)
    print(f"⏱️ 异步总耗时: {end_time - start_time:.2f}秒")

if __name__ == "__main__":
    asyncio.run(main())