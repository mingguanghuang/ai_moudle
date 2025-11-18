# 天眼慧聚 - 企业信息采集与知识库系统
## 项目简介
天眼慧聚是一个基于Python开发的企业信息采集与知识库构建系统。该系统可以自动从天眼查网站爬取公司信息，将数据存储到MySQL数据库中，并同时构建企业知识库，方便后续查询和分析。

## 功能特点
- 自动爬取天眼查网站上的公司信息
- 数据自动存储到MySQL数据库
- 自动构建企业知识库
- 灵活的配置系统
- 完善的日志记录

## 环境配置

```
conda create -n db python=3.10
conda activate db

# 安装依赖
pip install -r requirements.txt

# 修改.env配置
```

## 目录结构

```
fastgpt_tianyancha/
├── .env                  # 环境变量配置文件
├── config/               # 配置模块
│   └── config.py         # 配置加载和处理
├── core/                 # 核心功能模块
│   ├── crawler.py        # 爬虫模块
│   ├── database.py       # 数据库操作模块
│   └── knowledge_base.py # 知识库操作模块
├── input/                # 输入文件目录
│   └── companies.txt     # 公司名称列表
├── logs/                 # 日志目录
├── main.py               # 主程序入口
├── models/               # 数据模型
│   └── company.py        # 公司数据模型
├── requirements.txt      # 依赖包列表
└── utils/                # 工具函数
    ├── helpers.py        # 辅助函数
    └── logger.py         # 日志配置
```

## 使用方法
1. 准备公司名称列表
在 input/companies.txt 文件中，每行输入一个公司名称

2. 运行程序

   ```
   python main.py
   ```

3. 查看结果
程序运行后，会将爬取的公司信息存储到MySQL数据库中，并构建知识库。可以通过查看日志文件了解程序运行情况。

## 注意事项
1. Cookie更新 ：天眼查网站可能会定期更新Cookie验证机制，如遇到爬取失败，请更新 .env 文件中的Cookie信息。
2. 请求频率 ：系统默认在每次请求之间随机等待1-5秒，以避免被网站封禁。请勿修改此设置，除非您明确知道后果。
3. 数据库表结构 ：使用前请确保MySQL数据库中已创建相应的表结构。
4. 知识库API ：确保知识库API服务正常运行，并配置正确的API密钥。

## 数据库表结构
系统使用的数据库表结构如下：

```sql
DROP TABLE IF EXISTS `company_info`;
CREATE TABLE `company_info`
(
    `id`              bigint(15) unsigned NOT NULL AUTO_INCREMENT comment '自增id',
    `companyName`     varchar(50)       DEFAULT '' COMMENT '公司名称',
    `legalPersonName` varchar(10)       DEFAULT '' COMMENT '公司法人',
    `regCapital`      varchar(50)       DEFAULT '' COMMENT '公司注册资金',
    `regStatus`       varchar(5)        DEFAULT '' COMMENT '公司经营状态',
    `creditCode`      varchar(100)      DEFAULT '' COMMENT '公司统一社会信用代码',
    `businessScope`   TEXT comment '公司经营范围',
    `regLocation`     varchar(1000)     DEFAULT '' comment '公司注册地址',
    `phoneList`       varchar(100)      DEFAULT '' comment '公司联系方式',
    `establishTime`   datetime          DEFAULT null COMMENT '公司建立时间',
    `is_deleted`      tinyint unsigned NOT NULL DEFAULT 0 comment '是否逻辑删除 1删除，0不删除',
    `gmt_create`      datetime not NULL DEFAULT CURRENT_TIMESTAMP comment '数据创建时间',
    `gmt_modified`    datetime not NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP comment '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='公司信息表';
```

