from loguru import logger

from pydantic import BaseModel, Field
from typing import Dict, Any
import json


# # 1. 定义输出数据模型
# class AgentResponse(BaseModel):
#     """Agent结构化响应模型"""
#     tool: str
#     result: str
#     next_action: str
#     suggestion: str


# 2. 创建输出解析器
class AgentOutputParser:
    def __init__(self):
        # self.response_model = AgentResponse
        pass
    @staticmethod
    def parse(raw_output: Dict[str, Any]) -> str:
        """
        解析Agent的原始输出
        """
        try:
            # 如果output是字符串，先解析为字典
            if isinstance(raw_output.get('output'), str):
                output_dict = json.loads(raw_output['output'])
            else:
                output_dict = raw_output.get('output', {})
            logger.info(f"转化后的output为：{output_dict}")
            # 使用Pydantic模型验证和转换
            return output_dict

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {e}")
            raise

        except Exception as e:
            logger.error(f"输出解析失败: {e}")
            raise