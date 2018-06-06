
import redis
from ipproxypool.setting import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT, REDIS_KEY_NAME

class ProxyPool():
    """
    代理IP池：本质上是对Redis的操作
    """

    def __init__(self):
        """
        创建跟Redis的连接对象
        """
        if REDIS_PASSWORD:
            self.__db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        else:
            self.__db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def put(self, proxy):
        """
        在代理队列的头部放入代理
        :param proxy:       需要放入的代理
        :return:
        """
        self.__db.rpush(REDIS_KEY_NAME, proxy)

    def pop(self):
        """
        从代理队列的尾部取出一个代理
        :return:    取出的代理
        """
        try:
            # 从末尾取出一个代理ip
            return self.__db.rpop(REDIS_KEY_NAME).decode('utf-8')
        except:
            raise PoolEmptyError

    def get(self, count=1):
        """
        从代理队列的尾部取出count个代理
        :param count:   指定的数量
        :return:    返回代理的列表
        """
        # 从左部取出指定个代理ip
        proxies = self.__db.lrange(REDIS_KEY_NAME, 0, count-1)
        # 从队列中删除左部指定个代理ip
        self.__db.ltrim(REDIS_KEY_NAME, count, -1)
        return set(proxies)

    def size(self):
        """
        返回代理队列中代理的数量
        :return:    代理的数量
        """
        # 队列的长度
        return self.__db.llen(REDIS_KEY_NAME)

    def clear(self):
        """
        清空代理队列
        :return:
        """
        self.__db.delete(REDIS_KEY_NAME)


class PoolEmptyError(Exception):
    """
    代理池为空异常
    """
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy pool is empty')

if __name__ == '__main__':
    p = ProxyPool()
    print(p.size())
    print(p.pop())
    print(p.pop())
    print(p.size())
