from typing import Any, List, Optional, Dict
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from openai import OpenAI
import httpx
import os


class BMWDeepSeekLLM(LLM):
    """
    完全自定义的 BMW DeepSeek V3 LLM 实现
    处理特殊的 ACCESSCODE 认证和非标准响应格式
    """

    model: str = "DeepSeek-V3"
    api_key: str = ""
    base_url: str = "https://aistudio.bmwbrill.cn/function-service"
    timeout: int = 10000
    max_tokens: int = 16384

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 从环境变量或 kwargs 获取 API key
        self.api_key = kwargs.get("api_key") or os.environ.get(
            "BMW_DEEPSEEK_API_KEY", ""
        )

        # 创建禁用 SSL 验证的 HTTP 客户端
        http_client = httpx.Client(verify=False)

        # 使用 ACCESSCODE 格式初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=f"ACCESSCODE({self.api_key})",
            base_url=self.base_url,
            timeout=self.timeout / 1000,  # 转换为秒
            http_client=http_client,
        )

    @property
    def _llm_type(self) -> str:
        """返回 LLM 类型标识"""
        return "bmw_deepseek"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        同步调用 BMW DeepSeek API

        Args:
            prompt: 输入提示
            stop: 停止序列
            run_manager: 回调管理器
            **kwargs: 额外参数

        Returns:
            str: 模型响应内容
        """
        # 将 prompt 转换为消息格式
        messages = [{"role": "user", "content": prompt}]

        try:
            # 调用 OpenAI 客户端
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", 0.4),
                stop=stop,
            )

            # 提取响应内容
            if completion.choices and len(completion.choices) > 0:
                return completion.choices[0].message.content
            else:
                raise ValueError("API 返回了空的 choices 字段")

        except Exception as e:
            raise RuntimeError(f"BMW DeepSeek API 调用失败: {str(e)}")

    async def _acall(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        异步调用 BMW DeepSeek API

        Args:
            prompt: 输入提示
            stop: 停止序列
            run_manager: 回调管理器
            **kwargs: 额外参数

        Returns:
            str: 模型响应内容
        """
        # 将 prompt 转换为消息格式
        messages = [{"role": "user", "content": prompt}]

        try:
            # 使用异步客户端调用
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", self.max_tokens),
                temperature=kwargs.get("temperature", 0.4),
                stop=stop,
            )

            # 提取响应内容
            if completion.choices and len(completion.choices) > 0:
                return completion.choices[0].message.content
            else:
                raise ValueError("API 返回了空的 choices 字段")

        except Exception as e:
            raise RuntimeError(f"BMW DeepSeek API 调用失败: {str(e)}")

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """返回识别参数"""
        return {"model": self.model, "base_url": self.base_url, "timeout": self.timeout}
