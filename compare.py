# 引入同步请求库（邮递员）
import requests
# 引入异步请求库（异步版邮递员）
import aiohttp
# 引入异步事件循环启动器
import asyncio
# 引入计时器
import time

# 定义Ollama的API地址
OLLAMA_URL = "http://localhost:11434/api/generate"

# 准备一组问题，用来测试同步和异步的速度差异
questions = [
    "1+1等于几？",
    "Python是谁发明的？",
    "给我讲个笑话",
    "北京今天天气怎么样？",
    "用一句话解释什么是人工智能",
]


# ========== 同步版本 ==========
def sync_ask(question):
    """同步发送单个问题（等它回答完才能做别的事）"""
    payload = {
        "model": "qwen2.5:7b",
        "prompt": question,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return f"❓ {question}\n🤖 {result.get('response', '无回答')}\n"
    except Exception as e:
        return f"❓ {question}\n❌ 出错: {e}\n"


def sync_benchmark():
    """同步版基准测试：一个一个等"""
    print("=" * 50)
    print("⏳ 同步版本开始（一个一个等）...")
    print("=" * 50)

    start_time = time.time()

    # 同步方式：循环逐个发送，每个问完才发下一个
    for q in questions:
        print(sync_ask(q))

    end_time = time.time()
    print(f"⏱️ 同步总耗时: {end_time - start_time:.2f}秒")
    print()


# ========== 异步版本 ==========
async def async_ask(session, question):
    """异步发送单个问题（等的时候可以去干别的事）"""
    payload = {
        "model": "qwen2.5:7b",
        "prompt": question,
        "stream": False
    }
    try:
        # 异步上下文管理器，自动处理连接的打开和关闭
        async with session.post(
            OLLAMA_URL,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=120)
        ) as resp:
            result = await resp.json()
            return f"❓ {question}\n🤖 {result.get('response', '无回答')}\n"
    except Exception as e:
        return f"❓ {question}\n❌ 出错: {e}\n"


async def async_benchmark():
    """异步版基准测试：一起发，谁先回来先打印谁"""
    print("=" * 50)
    print("⚡ 异步版本开始（一起发）...")
    print("=" * 50)

    start_time = time.time()

    # 创建一个共享的会话
    async with aiohttp.ClientSession() as session:
        # 并发执行所有问题！asyncio.gather 会把所有协程打包在一起同时跑
        tasks = [async_ask(session, q) for q in questions]
        results = await asyncio.gather(*tasks)

    end_time = time.time()

    # 按顺序打印结果
    for res in results:
        print(res)

    print(f"⏱️ 异步总耗时: {end_time - start_time:.2f}秒")
    print()


# ========== 主程序 ==========
if __name__ == "__main__":
    # 先跑同步版本
    sync_benchmark()

    # 等2秒，让Ollama喘口气
    print("⏳ 休息2秒后开始异步版本...")
    time.sleep(2)

    # 再跑异步版本
    asyncio.run(async_benchmark())

    print("=" * 50)
    print("🎉 对比完成！看看异步比同步快了多少倍？")
    print("=" * 50)