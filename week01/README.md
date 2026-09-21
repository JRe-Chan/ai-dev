README.md：
# Week01 - FastAPI Chat Service

## 功能
- 非流式对话 POST /chat
- 流式对话 POST /chat (stream=true)
- 健康检查 GET /health

## 运行
1. 复制 `.env.example` 为 `.env` 并填入 API Key
2. `pip install -r requirements.txt`
3. `python main.py`
4. 访问 http://localhost:8000/docs

## 测试
```bash
# 非流式
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"你好"}'

# 流式
curl -N -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"你好","stream":true}'