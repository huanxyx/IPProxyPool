from ipproxypool.ipsource import KuaiProxySource, IhuanProxySource

# Redis相关配置(密码没有则填写None)
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWORD = None
REDIS_KEY_NAME = 'proxies'

# 校验器检查时间周期（秒）
VALIDATOR_CYCLE_TIME = 60*15

# 代理池检查器时间周期（秒）
CHECKER_CYCLE_TIME = 60*20

# 代理池的最低限度
LOWER_THRESHOLD = 100

# 代理ip可用性测试接口
TEST_URL = 'https://www.baidu.com' # 'http://icanhazip.com/'

# 代理ip可用性测试超时时间（秒）
VALIDATE_TIMEOUT = 10

# 当前获取代理IP的代理源
PROXY_SOURCE_LIST = [
    KuaiProxySource(),
    IhuanProxySource(),
]

# 指定获取源的最大页数
PROXY_SOURCE_MAX_PAGE = 10

# 检查器日志存储位置
CHECKER_LOGGING_POS = ''

# 校验器日志存储位置
VALIDATOR_LOGGING_POS = ''

# 指定RESTFUL接口的端口
RESTFUL_PORT = 5000


