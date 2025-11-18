import random
import time
import json
import urllib.parse
import requests
from lxml import etree
from loguru import logger

from models.company import Company

class TianyanCrawler:
    """天眼查爬虫"""
    
    def __init__(self, config):
        """
        初始化爬虫
        
        Args:
            config: 爬虫配置
        """
        self.user_agent = config.get('user_agent')
        self.cookie = config.get('cookie')
    
    def search_company(self, keyword):
        """
        搜索公司信息
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            list: 公司信息列表
        """
        try:
            # URL编码关键词
            encoded_keyword = urllib.parse.quote(keyword)
            url = f"https://www.tianyancha.com/nsearch?key={encoded_keyword}"
            
            # 设置请求头
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9",
                "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A;Brand\";v=\"8\", \"Chromium\";v=\"129\"",
                "user-agent": self.user_agent,
                "Cookie": self.cookie
            }
            
            # 发送请求
            response = requests.get(url=url, headers=headers)
            
            # 解析HTML
            html = etree.HTML(response.text)
            
            # 提取JSON数据
            json_data = html.xpath('//script[@id="__NEXT_DATA__"]/text()')[0]
            data = json.loads(json_data)
            
            # 提取公司列表
            company_list = data["props"]["pageProps"]["dehydratedState"]["queries"][2]["state"]["data"]['data']["companyList"]
            
            return company_list
            
        except Exception as e:
            logger.error(f"搜索公司信息失败: {keyword}, 错误: {e}")
            return []