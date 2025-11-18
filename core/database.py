import traceback
import pymysql
from dbutils.pooled_db import PooledDB
from loguru import logger

pymysql.install_as_MySQLdb()

class DatabaseClient:
    """数据库连接池客户端"""
    
    def __init__(self, config):
        """
        初始化数据库连接池
        
        Args:
            config: 数据库配置字典
        """
        self.__pool = PooledDB(
            creator=pymysql,
            maxconnections=6,
            mincached=2,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            **config
        )
    
    def close(self, conn, cursor):
        """
        关闭数据库连接和游标
        
        Args:
            conn: 数据库连接
            cursor: 数据库游标
        """
        try:
            cursor.close()
            conn.close()
        except Exception as e:
            logger.error(f"关闭数据库连接失败: {e}")
            logger.debug(traceback.format_exc())
    
    def execute_query(self, sql, params=()):
        """
        执行查询操作
        
        Args:
            sql: SQL查询语句
            params: 查询参数
            
        Returns:
            tuple: (结果数量, 查询结果)
        """
        conn = self.__pool.connection()
        cursor = conn.cursor()
        try:
            count = cursor.execute(sql, params)
            result = cursor.fetchall()
            return count, result
        except Exception as e:
            logger.error(f"查询执行失败: {sql}, 参数: {params}, 错误: {e}")
            logger.debug(traceback.format_exc())
            return 0, []
        finally:
            self.close(conn, cursor)
    
    def execute_insert(self, sql, params=()):
        """
        执行插入操作
        
        Args:
            sql: SQL插入语句
            params: 插入参数
            
        Returns:
            int: 插入ID或None
        """
        conn = self.__pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            last_id = cursor.lastrowid
            conn.commit()
            return last_id
        except Exception as e:
            conn.rollback()
            logger.error(f"插入执行失败: {sql}, 参数: {params}, 错误: {e}")
            logger.debug(traceback.format_exc())
            return None
        finally:
            self.close(conn, cursor)
    
    def execute_batch_insert(self, sql, params_list=()):
        """
        执行批量插入操作
        
        Args:
            sql: SQL插入语句
            params_list: 批量插入参数列表
            
        Returns:
            int: 最后插入ID或None
        """
        conn = self.__pool.connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, params_list)
            last_id = cursor.lastrowid
            conn.commit()
            return last_id
        except Exception as e:
            conn.rollback()
            logger.error(f"批量插入执行失败: {sql}, 错误: {e}")
            logger.debug(traceback.format_exc())
            return None
        finally:
            self.close(conn, cursor)