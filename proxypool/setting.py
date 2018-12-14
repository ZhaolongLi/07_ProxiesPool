# coding:utf-8

# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码
REDIS_PASSWORD = None

REDIS_KEY = 'proxies'

# 代理的分数值
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# 代理池数量界限
POOL_UPPER_THRESHOLD = 10000

# 测试周期
TESTER_CYCLE = 20

# 获取周期
GETTER_CYCLE = 300

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True


VALID_STATUS_CODES = [200,302]

# 测试API
TEST_URL = 'http://www.baidu.com'

# 最大批测试量
BATCH_TEST_SIZE = 10

# API配置
API_HOST = '127.0.0.1'
API_PORT = 5555

