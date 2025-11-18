import random
import string

def generate_random_code(length=4):
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
        
    Returns:
        str: 随机字符串
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))