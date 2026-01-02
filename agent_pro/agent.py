
from langchain.agents import Tool

from langchain.memory import ConversationBufferWindowMemory

from models.models import Models, ALI_TONGYI_URL, ALI_TONGYI_API_KEY, ALI_TONGYI_DEEPSEEK_V3, ALI_TONGYI_DEEPSEEK_V3_2
from utils.Redis import RedisUsing
from langchain.agents import AgentExecutor,  create_tool_calling_agent

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, \
    HumanMessagePromptTemplate
from langchain_openai import ChatOpenAI
from agent_pro.tools import Tools
from utils.out_put_format import AgentOutputParser


class Agent:
    def __init__(self,model_name,user_prompt):
        self.model_name = model_name
        self.user_prompt = user_prompt
        self.historyMessage = RedisUsing(session_id="agent_session")

    def __agent_init(self):
        '''
        初始化模型
        :return:返回模型客户端
        '''
        model_client = Models(ALI_TONGYI_API_KEY,ALI_TONGYI_URL).get_ali_model_client(self.model_name,streaming=True)
        #格式化提示词
        base_template = ChatPromptTemplate.from_messages([
            ("system", """你是一名优秀的人工智能助手,你可以根据用户给出的命令进行远程设备的控制，并做出如下动作:
        1.根据用户命令{input}识别指令关键词,调用相应的控制设备的工具，并将工具调用的结果返回给我。
        2.结合前两段对话历史{chat_history_before}预测下一次指令行为，并给出建议。

        你可以调用的工具有:
        1. LED灯控制: 打开或关闭设备的LED灯（有很多个），可根据用户的命令描述来决定具体LED灯的开关。
        2. 蜂鸣器控制: 打开或关闭设备的蜂鸣器开关。
        3. 风扇控制: 打开或关闭设备的风扇开关。
        4. 语音系统关闭: 关闭语音设备。
        5. 数字、字符显示: 显示数字或字符。

        要求:
        1.使用中文回答。
        2.使用以下json格式返回结果:
        {{
            "tool": "调用工具名称",
            "result": "工具调用结果"
            "next_action": "下一次指令行为预测"
            "suggestion": "建议"
        }}。
        3.返回消息示例:
        {{ 
            "tool": "风扇控制"，
            "result": "已为您关闭风扇"，
            "next_action": "用户可能需要打开风扇或进行其他设备控制操作"，
            "suggestion": "建议您：1. 如需打开风扇，请发送'打开风扇'指令 2. 如需控制其他设备，请发送相应指令"
        }}
        """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        custom_history = self.historyMessage.get_history()

        # 使用 .partial() 方法将 chat_history_before 变量提前绑定到模板上
        chat_template = base_template.partial(chat_history_before=custom_history)
        # 定义工具
        tools = [
            Tool(
                name="LED灯控制",
                func=Tools.control_led,
                description="""LED灯控制: 打开或关闭设备的LED灯。
                Args:
                    led_id: LED灯身份标识，可选值为"1"、"2"、"3"等数字,"1"表示LED灯1，"2"表示LED灯2，"3"表示LED灯3,等等根据实际情况来
                    action: 操作类型，"on"表示打开，"off"表示关闭"""
            ),
            Tool(
                name="蜂鸣器控制",
                func=Tools.control_buzzer,
                description="""蜂鸣器控制: 打开或关闭设备的蜂鸣器开关。
                Args:
                    action: 操作类型，"on"表示打开，"off"表示关闭"""
            ),
            Tool(
                name="风扇控制",
                func=Tools.control_fan,
                description="""风扇控制: 打开或关闭设备的风扇开关。
                Args:
                    action: 操作类型，"on"表示打开，"off"表示关闭"""
            ),
            Tool(
                name="语音系统关闭",
                func=Tools.shutdown_voice_system,
                description="""关闭语音设备。"""
            ),
            Tool(
                name="数字、字符显示",
                func=Tools.display_text,
                description="""数字、字符显示: 显示数字或字符。
                Args:
                    content: 要显示的内容（数字或字符）"""
            )
        ]
        # 设置记忆
        memory = ConversationBufferWindowMemory(
            k=3,
            human_prefix="用户",
            ai_prefix="小神龙",
            memory_key="chat_history",
            return_messages=True,
            chat_memory=self.historyMessage.history
        )

        # 创建agent
        agent = create_tool_calling_agent(
            model_client,
            tools=tools,
            prompt=chat_template,
        )
        # 创建agent执行器
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True
        )

        return agent_executor

    def agent_run_parse(self):
        # 获取原始输出
        raw_output = self.__agent_init().invoke({"input": self.user_prompt})

        # 使用解析器处理输出
        parsed_output = AgentOutputParser.parse(raw_output)
        return parsed_output

    def agent_run(self):
        #原始输出
        return self.__agent_init().invoke({"input": self.user_prompt})
# 调试用例
# if __name__ == "__main__":
#     my_agent = Agent(ALI_TONGYI_DEEPSEEK_V3_2,"当前时间")
#     # my_agent.historyMessage.clear_history()
#     print(my_agent.agent_run_parse())
#     print(my_agent.agent_run())
#     print("历史记录数：", len(my_agent.historyMessage.get_history()))