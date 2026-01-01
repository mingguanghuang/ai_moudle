import os
from dotenv import load_dotenv

load_dotenv()
def get_env(key):
    """
    获取环境变量
    :key: env文件中变量名称
    :return: 环境变量值
    """
    return os.environ.get(key)

ALI_TONGYI_API_KEY = get_env("ALI_API_KEY")
RAGFLOW_API_KEY = get_env("RAGFLOW_API_KEY")