import time
from loguru import logger

class Company:
    """公司数据模型"""
    
    def __init__(self, data):
        """
        初始化公司数据
        
        Args:
            data: 公司原始数据字典
        """
        self.name = self._clean_text(data.get('name', ''))
        self.legal_person_name = data.get('legalPersonName', '')
        self.establish_time_raw = data.get('estiblishTime', '')
        self.reg_capital = data.get('regCapital', '')
        self.reg_status = data.get('regStatus', '')
        self.credit_code = data.get('creditCode', '')
        self.business_scope = data.get('businessScope', '')
        self.reg_location = self._clean_text(data.get('regLocation', ''))
        self.phone_list = ','.join(data.get('phoneList', []))
        
        # 处理时间格式
        try:
            if self.establish_time_raw:
                time_str = self.establish_time_raw[:-2]  # 移除末尾的.0
                self.establish_time_obj = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                self.establish_time = time.strftime('%Y-%m-%d %H:%M:%S', self.establish_time_obj)
            else:
                self.establish_time_obj = None
                self.establish_time = None
        except Exception as e:
            logger.error(f"时间格式处理失败: {self.establish_time_raw}, 错误: {e}")
            self.establish_time_obj = None
            self.establish_time = None
    
    def _clean_text(self, text):
        """清理文本中的HTML标签"""
        return text.replace('<em>', '').replace('</em>', '')
    
    def to_db_tuple(self):
        """转换为数据库插入元组"""
        return (
            self.name,
            self.legal_person_name,
            self.reg_capital,
            self.reg_status,
            self.credit_code,
            self.business_scope,
            self.reg_location,
            self.phone_list,
            self.establish_time
        )
    
    def to_knowledge_text(self):
        """转换为知识库文本描述"""
        if not self.establish_time_obj:
            return f"{self.name}，位于{self.reg_location}，其法人为{self.legal_person_name}，其注册资金为{self.reg_capital}，其统一社会信用代码为：{self.credit_code}，其经营状态为{self.reg_status}，其联系方式为：{self.phone_list}，其经营范围包括{self.business_scope}"
            
        return (
            f"{self.name}成立于{self.establish_time_obj.tm_year}年"
            f"{self.establish_time_obj.tm_mon}月{self.establish_time_obj.tm_mday}日，"
            f"位于{self.reg_location}，其法人为{self.legal_person_name}，"
            f"其注册资金为{self.reg_capital}，其统一社会信用代码为：{self.credit_code}，"
            f"其经营状态为{self.reg_status}，其联系方式为：{self.phone_list}，"
            f"其经营范围包括{self.business_scope}"
        )