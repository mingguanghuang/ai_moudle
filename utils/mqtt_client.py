import paho.mqtt.client as mqtt
import json
import uuid
from loguru import logger


class MQTTClient:
    """MQTT通信客户端类"""
    
    def __init__(self, broker="mqtt.yyzlab.com.cn", port=1883, topic="huangmingguang"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None
        self.is_connected = False
        
    def connect(self):
        """连接到MQTT服务器"""
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            logger.info(f"MQTT客户端已连接到 {self.broker}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"MQTT连接失败: {e}")
            return False
    
    def _on_connect(self, client, userdata, flags, rc):
        """连接回调函数"""
        if rc == 0:
            self.is_connected = True
            logger.info("MQTT连接成功")
        else:
            self.is_connected = False
            logger.error(f"MQTT连接失败，错误码: {rc}")
    
    def _on_disconnect(self, client, userdata, rc):
        """断开连接回调函数"""
        self.is_connected = False
        if rc != 0:
            logger.warning("MQTT意外断开连接")
        else:
            logger.info("MQTT正常断开连接")
    
    def send_message(self, command, parameters=None, message_id=None):
        """发送MQTT消息"""
        if not self.is_connected:
            if not self.connect():
                return False
        
        try:
            if message_id is None:
                message_id = f"msg_{str(uuid.uuid4())[:8]}"
            
            if parameters is None:
                parameters = {}
            
            message = {
                "command": command,
                "parameters": parameters,
                "message_id": message_id
            }
            
            result = self.client.publish(self.topic, json.dumps(message))
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"MQTT消息发送成功: {message}")
                return True
            else:
                logger.error(f"MQTT消息发送失败，错误码: {result.rc}")
                return False
        except Exception as e:
            logger.error(f"发送MQTT消息时出错: {e}")
            return False
    
    def disconnect(self):
        """断开MQTT连接"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            logger.info("MQTT客户端已断开连接")


mqtt_client = MQTTClient()
mqtt_client_with_topic_chen = MQTTClient(topic="chenkaijie")