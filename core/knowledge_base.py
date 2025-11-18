import random
import string
import requests
import traceback
from loguru import logger

class KnowledgeBaseClient:
    """知识库客户端"""
    
    def __init__(self, config):
        """
        初始化知识库客户端
        
        Args:
            config: 知识库配置
        """
        self.api_base_url = config.get('api_base_url')
        self.api_key = config.get('api_key')
        self.headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def generate_collection_name(self, prefix):
        """
        生成唯一的集合名称
        
        Args:
            prefix: 集合名称前缀
            
        Returns:
            str: 唯一集合名称
        """
        random_code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        return f"{prefix}_{random_code}"
    
    def create_dataset(self, dataset_name):
        """
        创建知识库数据集
        
        Args:
            dataset_name: 数据集名称
            
        Returns:
            str: 创建结果消息
        """
        try:
            url = f"{self.api_base_url}/core/dataset/create"
            data = {
                "type": "dataset",
                "name": dataset_name,
                "vectorModel": "text-embedding-v1",
                "agentModel": "qwen-max"
            }
            
            response = requests.post(url=url, json=data, headers=self.headers, verify=False)
            response.raise_for_status()
            
            return f"{dataset_name}创建成功"
        except Exception as e:
            logger.error(f"创建知识库数据集失败: {dataset_name}, 错误: {e}")
            return f"{dataset_name}创建失败: {str(e)}"
    
    def query_datasets(self):
        """
        查询所有知识库数据集
        
        Returns:
            dict: 数据集字典 {name: {id, vectorModel}}
        """
        dataset_dict = {}
        try:
            url = f"{self.api_base_url}/core/dataset/list"
            
            response = requests.post(url=url, headers=self.headers, verify=False)
            response.raise_for_status()
            
            result = response.json()
            
            # 解析数据集
            for data in result.get('data', []):
                dataset_dict[data.get('name')] = {
                    "id": data.get('_id'),
                    "vectorModel": data.get('vectorModel')
                }
                
            return dataset_dict
        except Exception as e:
            logger.error(f"查询知识库数据集失败: {e}")
            logger.debug(traceback.format_exc())
            return dataset_dict
    
    def create_text_collection(self, collection_name, dataset_id, text):
        """
        创建文本集合
        
        Args:
            collection_name: 集合名称
            dataset_id: 数据集ID
            text: 文本内容
            
        Returns:
            bool: 是否创建成功
        """
        try:
            url = f"{self.api_base_url}/core/dataset/collection/create/text"
            data = {
                "text": text,
                "datasetId": dataset_id,
                "name": collection_name,
                "trainingType": "chunk"
            }
            
            response = requests.post(url=url, json=data, headers=self.headers)
            response.raise_for_status()
            
            logger.info(f"创建文本集合成功: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"创建文本集合失败: {collection_name}, 错误: {e}")
            logger.debug(traceback.format_exc())
            return False