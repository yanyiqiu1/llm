import httpx
import json

# 创建禁用 SSL 验证的 HTTP 客户端
http_client = httpx.Client(verify=False)

try:
    # 调用您的 BMW DeepSeek V3 API
    response = http_client.post(
        "https://aistudio.bmwbrill.cn/function-service/v1/chat/completions",
        headers={
            "Authorization": "Bearer ACCESSCODE(0062B7916FE5440BBFBC262CE18B3493)",
            "Content-Type": "application/json",
        },
        json={
            "model": "DeepSeek-V3",
            "messages": [{"role": "user", "content": "你好"}],
            "max_tokens": 100,
        },
        timeout=10.0,
    )

    print("HTTP 状态码:", response.status_code)
    print("\n完整响应:")
    response_data = response.json()
    print(json.dumps(response_data, indent=2, ensure_ascii=False))

    # 验证关键字段
    print("\n=== 格式验证 ===")
    if "choices" in response_data:
        print("✓ choices 字段存在")
        if response_data["choices"] and len(response_data["choices"]) > 0:
            print("✓ choices 数组不为空")
            if "message" in response_data["choices"][0]:
                print("✓ message 字段存在")
                if "content" in response_data["choices"][0]["message"]:
                    print("✓ content 字段存在")
                    print(
                        f"  内容: {response_data['choices'][0]['message']['content']}"
                    )
                else:
                    print("✗ content 字段缺失")
            else:
                print("✗ message 字段缺失")
        else:
            print("✗ choices 数组为空")
    else:
        print("✗ choices 字段不存在")
        print("实际返回的字段:", list(response_data.keys()))

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()
