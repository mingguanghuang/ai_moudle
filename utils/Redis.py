
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, BaseMessage
import redis

REDIS_URL = "redis://127.0.0.1:6379"


class RedisUsing:
    '''
    定义一个Redis类，用于缓存会话的历史记录
    '''
    def __init__(self, session_id: str):
        self.session_id = session_id
        # 初始化Redis客户端
        self.redis_client = redis.Redis.from_url(REDIS_URL)

        # 初始化聊天历史记录
        self.history = RedisChatMessageHistory(
            session_id=self.session_id,
            url=REDIS_URL
        )

    # Redis连接服务
    def connect(self) -> None:
        if not self.redis_client.ping():
            self.redis_client = redis.Redis.from_url(REDIS_URL)

    # 关闭Redis服务
    def disconnect(self) -> None:
        if self.redis_client:
            self.redis_client.close()

    # 添加用户历史消息
    def add_user_message(self, content: str) -> None:
        self.connect()
        message = HumanMessage(content=content)
        self.history.add_message(message)

    # 添加AI历史消息
    def add_ai_message(self, content: str) -> None:
        self.connect()
        message = AIMessage(content=content)
        self.history.add_message(message)

    # 获取历史消息
    def get_history(self) -> list[BaseMessage]:
        self.connect()
        if len(self.history.messages) < 4:
            return self.history.messages
        else:
            return self.history.messages[-4:]

    # 清除历史消息
    def clear_history(self) -> None:
        self.connect()
        self.history.clear()

    # 删除最早的历史消息，暂未实现
    def delete_earliest_history(self) -> None:
        self.connect()