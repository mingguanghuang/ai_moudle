from config.load_config import ALI_TONGYI_API_KEY
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import inspect
from langchain_community.embeddings import DashScopeEmbeddings

ALI_TONGYI_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
# ALI_TONGYI_MAX_MODEL = "qwen-max-latest" #我的免费额度到期了，别用这个，用下面的（不然要扣钱的）
ALI_TONGYI_DEEPSEEK_R1 = "deepseek-r1"
ALI_TONGYI_DEEPSEEK_V3 = "deepseek-v3"
ALI_TONGYI_QWEN_PLUS = "qwen-plus"
ALI_TONGYI_DEEPSEEK_V3_2 = "deepseek-v3.2"
ALI_TONGYI_EMBEDDING_MODEL = "text-embedding-v3"
ALI_TONGYI_RERANK_MODEL = "gte-rerank-v2"



class Models:
    """
    默认阿里百炼模型类，若想使用其它平台模型，请给出api_key和url
    """
    def __init__(self,api_key,url):
        self.api_key = api_key
        self.url = url


    def _get_lc_model_client(self,model,temperature,streaming,verbose=False, debug=False):
        """
            通过LangChain获得指定平台和模型的客户端，设定的默认平台和模型为阿里百炼qwen-plus
            也可以通过传入api_key，base_url，model三个参数来覆盖默认值
            verbose，debug两个参数，分别控制是否输出调试信息，是否输出详细调试信息，默认不打印
        """
        function_name = inspect.currentframe().f_code.co_name
        if verbose:
            print(f"{function_name}-平台：{self.url},模型：{model},温度：{temperature}")
        if debug:
            print(f"{function_name}-平台：{self.url},模型：{model},温度：{temperature},key：{self.api_key}")
        return ChatOpenAI(api_key=self.api_key, base_url=self.url, model=model, temperature=temperature,streaming=streaming,
                          extra_body={"enable_thinking": False})


    def get_ali_model_client(self,model=ALI_TONGYI_DEEPSEEK_V3,streaming=False, temperature=0.7, verbose=False, debug=False):
        """通过LangChain使用阿里大模型DEEPSEEK_V3"""
        return self._get_lc_model_client(model=model, temperature=temperature, verbose=verbose, debug=debug, streaming=streaming)
    @staticmethod
    def get_ali_embeddings():
        """通过LangChain获得一个阿里通义千问嵌入模型的实例。
        这里写成静态方法，因为不确定其它平台是否有文本嵌入模型
        """
        return DashScopeEmbeddings(
            model=ALI_TONGYI_EMBEDDING_MODEL, dashscope_api_key=ALI_TONGYI_API_KEY
        )


    @staticmethod
    def get_normal_client(api_key=ALI_TONGYI_API_KEY, base_url=ALI_TONGYI_URL,
                          verbose=False, debug=False):
        """
        使用原生api获得指定平台的客户端（这里主要实现OpenAI兼容），但未指定具体模型，缺省平台为阿里云百炼
        也可以通过传入api_key，base_url两个参数来覆盖默认值
        verbose，debug两个参数，分别控制是否输出调试信息，是否输出详细调试信息，默认不打印
        """
        function_name = inspect.currentframe().f_code.co_name
        if verbose:
            print(f"{function_name}-平台：{base_url}")
        if debug:
            print(f"{function_name}-平台：{base_url},key：{api_key}")
        return OpenAI(api_key=api_key, base_url=base_url)

