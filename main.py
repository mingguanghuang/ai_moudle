import os
import time
import random
from loguru import logger

from config.config import DB_CONFIG, TIANYANCHA_CONFIG, KNOWLEDGE_BASE_CONFIG, INPUT_CONFIG
from core.database import DatabaseClient
from core.crawler import TianyanCrawler
from core.knowledge_base import KnowledgeBaseClient
from models.company import Company
from utils.logger import setup_logger

def process_company(db_client, kb_client, company_data, dataset_dict, dataset_name):
    """
    处理单个公司数据
    
    Args:
        db_client: 数据库客户端
        kb_client: 知识库客户端
        company_data: 公司原始数据
        dataset_dict: 数据集字典
        dataset_name: 数据集名称
        
    Returns:
        bool: 处理是否成功
    """
    try:
        # 创建公司对象
        company = Company(company_data)
        
        # 保存到数据库
        sql = (
            "INSERT INTO tianyancha_test.company_info"
            "(companyName, legalPersonName, regCapital, regStatus, "
            "creditCode, businessScope, regLocation, phoneList, establishTime) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        
        company_id = db_client.execute_insert(sql, company.to_db_tuple())
        
        if not company_id:
            logger.error(f"插入公司信息失败: {company.name}")
            return False
        
        # 生成知识库文本
        knowledge_text = company.to_knowledge_text()
        logger.info(f"生成知识库文本: {knowledge_text[:50]}...")
        
        # 创建知识库集合
        collection_name = kb_client.generate_collection_name(company.name)
        
        # 确保数据集存在
        if dataset_name not in dataset_dict:
            logger.error(f"数据集不存在: {dataset_name}")
            return False
        
        # 创建文本集合
        success = kb_client.create_text_collection(
            collection_name, 
            dataset_dict[dataset_name]["id"], 
            knowledge_text
        )
        
        return success
    
    except Exception as e:
        logger.error(f"处理公司数据失败: {e}")
        return False

def main():
    """主程序入口"""
    # 设置日志
    setup_logger()
    
    # 从配置文件获取设置
    dataset_name = INPUT_CONFIG.get('default_dataset', 'company_info')
    company_file = INPUT_CONFIG.get('company_file', None)
    single_company = INPUT_CONFIG.get('single_company', None)
    
    # 初始化客户端
    db_client = DatabaseClient(DB_CONFIG)
    crawler = TianyanCrawler(TIANYANCHA_CONFIG)
    kb_client = KnowledgeBaseClient(KNOWLEDGE_BASE_CONFIG)
    
    # 查询或创建数据集
    dataset_dict = kb_client.query_datasets()
    if dataset_name not in dataset_dict:
        logger.info(f"创建数据集: {dataset_name}")
        kb_client.create_dataset(dataset_name)
        # 重新查询数据集
        dataset_dict = kb_client.query_datasets()
    
    # 处理输入
    companies_to_search = []

    if single_company:
        # 使用配置中的单个公司名称
        companies_to_search = [single_company]
    elif company_file and os.path.exists(company_file):
        # 从文件读取公司名称
        try:
            with open(company_file, 'r', encoding='utf-8') as f:
                companies_to_search = [line.strip() for line in f if line.strip()]
                # 只取前10家公司
                companies_to_search = companies_to_search[:10]
                logger.info(f"从文件中读取了{len(companies_to_search)}家公司")
        except Exception as e:
            logger.error(f"读取输入文件失败: {company_file}, 错误: {e}")
            return
    else:
        logger.error("未配置公司名称或文件路径，请检查配置文件")
        return
    
    # 处理每个公司
    for company_name in companies_to_search:
        logger.info(f"开始处理公司: {company_name}")
        
        # 搜索公司信息
        company_list = crawler.search_company(company_name)
        
        if not company_list:
            logger.warning(f"未找到公司信息: {company_name}")
            continue
        
        # 处理第一个搜索结果
        company_data = company_list[0]
        success = process_company(db_client, kb_client, company_data, dataset_dict, dataset_name)
        
        if success:
            logger.info(f"成功处理公司: {company_name}")
        else:
            logger.error(f"处理公司失败: {company_name}")
        
        # 随机延时，避免被封
        delay = random.uniform(1, 5)
        logger.debug(f"等待 {delay:.2f} 秒...")
        time.sleep(delay)

if __name__ == "__main__":
    main()