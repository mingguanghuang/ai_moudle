import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 输入文件配置
INPUT_CONFIG =   {
    'default_dataset': 'company_info',  # 默认数据集名称
    'company_file': os.getenv('INPUT_FILE_PATH'),  # 公司名称文件路径
    'single_company': None  # 单个公司名称，如果设置了此项，将忽略文件路径
}

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'tianyancha_test'),
    'charset': 'utf8mb4'
}

# 天眼查API配置
TIANYANCHA_CONFIG = {
    'user_agent': os.getenv('TIANYANCHA_USER_AGENT', ''),
    'cookie': os.getenv('TIANYANCHA_COOKIE', '')
}

# 知识库API配置
KNOWLEDGE_BASE_CONFIG = {
    'api_base_url': os.getenv('API_BASE_URL', 'http://localhost:3000/api'),
    'api_key': os.getenv('API_KEY', '')
}