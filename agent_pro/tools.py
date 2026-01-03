from langchain.tools import tool
import json
import uuid

from loguru import logger
from utils.mqtt_client import mqtt_client, MQTTClient
import datetime
import requests
import json


class Tools:
    def __init__(self):
        pass

    @staticmethod
    @tool
    def control_led(led_id: int = 1, action: str = "on") -> str:
        """LED灯控制: 打开或关闭设备的LED灯。
        
        Args:
            led_id: LED灯身份标识，可选值为"1"、"2"、"3"等数字,"1"表示LED灯1，"2"表示LED灯2，"3"表示LED灯3等等根据实际情况来
            action: 操作类型，"on"表示打开，"off"表示关闭
        """
        try:
            
            # 确定命令
            if action.lower() == "on":
                command = "LED_ON"
                parameters = {"led_id": led_id}
                message_id = "msg_005"
            else:
                command = "LED_OFF"
                parameters = {"led_id": led_id}
                message_id = "msg_006"
            
            # 发送MQTT消息
                
            success = mqtt_client.send_message(
                    command=command,
                    parameters=parameters,
                    message_id=message_id
                )
                
            if not success:
                return f"控制led_{led_id}失败"

            else:
                return f"控制led_{led_id}成功"
                
        except Exception as e:
            return f"LED控制出错: {str(e)}"

    @staticmethod
    @tool
    def control_buzzer(action: str = "on") -> str:
        """蜂鸣器控制: 打开或关闭当前设备的蜂鸣器开关。
        
        Args:
            action: 操作类型，"on"表示打开，"off"表示关闭
        """
        try:
            # 确定命令
            if action.lower() == "on":
                command = "BEEPER_ON"
                message_id = "msg_001"
                params = {}

            else:
                command = "BEEPER_OFF"
                message_id = "msg_002"
                params = {}
            
            # 发送MQTT消息

            success = mqtt_client.send_message(
                command=command,
                parameters=params,
                message_id=message_id
            )
            
            if success:
                return f"蜂鸣器已{action}"
            else:
                return "蜂鸣器控制失败"
                
        except Exception as e:
            return f"蜂鸣器控制出错: {str(e)}"

    @staticmethod
    @tool
    def control_fan(action: str = "on") -> str:
        """风扇控制: 打开或关闭当前设备的风扇开关。
        
        Args:
            action: 操作类型，"on"表示打开，"off"表示关闭
        """
        try:
            # 确定命令
            if action.lower() == "on":
                command = "FAN_ON"
                message_id = "msg_003"
                params = {"speed": 200}
            else:
                command = "FAN_OFF"
                message_id = "msg_004"
                params = {}
            
            # 发送MQTT消息
            success = mqtt_client.send_message(
                command=command,
                parameters=params,
                message_id=message_id
            )
            
            if success:
                return f"风扇已{action}"

            else:
                return "风扇控制失败"
                
        except Exception as e:
            return f"风扇控制出错: {str(e)}"

    @staticmethod
    @tool
    def shutdown_voice_system() -> str:
        """语音系统关闭: 关闭当前的语音设备。"""
        try:
            # 发送MQTT消息
            message_id = "message_voice"
            success = mqtt_client.send_message(
                command="VOICE_SHUTDOWN",
                parameters={},
                message_id=message_id
            )
            
            if success:
                return "语音系统已关闭"
            else:
                return "语音系统关闭失败"
                
        except Exception as e:
            return f"语音系统关闭出错: {str(e)}"

    @staticmethod
    @tool
    def display_text(content: int|str) -> str:
        """数字、字符显示: 显示数字或字符。
        
        Args:
            content: 要显示的内容（数字或字符）
        """
        try:
            # 发送MQTT消息
            if type(content) == int:
                message_id = "message_007"
                params = {"display_num": content}
            else:
                message_id = "message_008"
                params = {"display_str": content}
            success = mqtt_client.send_message(
                command="DISPLAY_CONTROL",
                parameters=params,
                message_id=message_id
            )
            
            if success:
                return f"已显示内容: {content}"
            else:
                return "显示内容失败"
                
        except Exception as e:
            return f"显示内容出错: {str(e)}"

    # @staticmethod
    # @tool
    # def google_search(query: str) -> str:
    #     """搜索谷歌，输入搜索内容，返回搜索结果"""
    #     # 这里需要配置你的谷歌搜索API，暂时返回模拟结果
    #     try:
    #         # 实际应用中需要替换为真实的搜索API
    #         return f"模拟谷歌搜索结果：{query}"
    #     except Exception as e:
    #         return f"搜索出错: {str(e)}"
    #
    # @staticmethod
    # @tool
    # def get_current_time() -> str:
    #     """获取当前时间，返回当前时间"""
    #     current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     return f"当前时间是：{current_time}"
    #
    # @staticmethod
    # @tool
    # def get_weather(city: str) -> str:
    #     """获取天气，输入城市名称，返回天气信息"""
    #     # 这里需要配置真实的天气API，暂时返回模拟结果
    #     try:
    #         return f"模拟天气信息：{city} 当前天气晴朗，温度25°C"
    #     except Exception as e:
    #         return f"获取天气信息出错: {str(e)}"
    #
    # @staticmethod
    # @tool
    # def get_news(keyword: str = "") -> str:
    #     """获取新闻，输入关键词，返回新闻"""
    #     # 模拟新闻获取
    #     try:
    #         if keyword:
    #             return f"模拟新闻：关于{keyword}的相关新闻"
    #         else:
    #             return "模拟新闻：今日新闻摘要"
    #     except Exception as e:
    #         return f"获取新闻出错: {str(e)}"
    #
    # @staticmethod
    # @tool
    # def get_stock_info(stock_code: str) -> str:
    #     """获取股票信息，输入股票代码，返回股票信息"""
    #     try:
    #         return f"模拟股票信息：{stock_code} 股票详情信息"
    #     except Exception as e:
    #         return f"获取股票信息出错: {str(e)}"
    #
    # @staticmethod
    # @tool
    # def get_stock_price(stock_code: str) -> str:
    #     """获取股票价格，输入股票代码，返回股票价格"""
    #     try:
    #         return f"模拟股票价格：{stock_code} 当前价格为 25.68 元"
    #     except Exception as e:
    #         return f"获取股票价格出错: {str(e)}"