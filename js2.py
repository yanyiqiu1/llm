import httpx
import json

http_client = httpx.Client(verify=False)

# 测试格式 1: ACCESSCODE xxxxx
print("测试格式 1: ACCESSCODE xxxxx")
response1 = http_client.post(
    "https://aistudio.bmwbrill.cn/function-service/v1/chat/completions",
    headers={
        "Authorization": "ACCESSCODE 0062B7916FE5440BBFBC262CE18B3493",
        "Content-Type": "application/json",
    },
    json={
        "model": "DeepSeek-V3",
        "messages": [{"role": "user", "content": "你好"}],
        "max_tokens": 100,
    },
    timeout=10.0,
)
print("状态码:", response1.status_code)
print("响应:", json.dumps(response1.json(), indent=2, ensure_ascii=False))

# 测试格式 2: Bearer ACCESSCODE xxxxx
print("\n测试格式 2: Bearer ACCESSCODE xxxxx")
response2 = http_client.post(
    "https://aistudio.bmwbrill.cn/function-service/v1/chat/completions",
    headers={
        "Authorization": "Bearer ACCESSCODE 0062B7916FE5440BBFBC262CE18B3493",
        "Content-Type": "application/json",
    },
    json={
        "model": "DeepSeek-V3",
        "messages": [{"role": "user", "content": "你好"}],
        "max_tokens": 100,
    },
    timeout=10.0,
)
print("状态码:", response2.status_code)
print("响应:", json.dumps(response2.json(), indent=2, ensure_ascii=False))
