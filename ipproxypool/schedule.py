import time
from multiprocessing import Process
import aiohttp
import asyncio

from ipproxypool.getter import ProxyGetter
from ipproxypool.proxypool import ProxyPool
from ipproxypool.headergetter import get_random_ua_header
from ipproxypool.setting import *

class ProxyValidator():
    '''
    代理校验器
    '''
    def __init__(self):
        self.proxy_pool = ProxyPool()

    async def __validate_single_proxy(self, proxy, session):
        """
        使用异步HTTP校验单个代理ip的可用性
        """
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf-8')
        real_proxy = 'http://' + proxy
        print('开始测试代理ip：', proxy)
        start = time.time()
        try:
            async with session.get(TEST_URL,
                                   proxy=real_proxy,
                                   timeout=VALIDATE_TIMEOUT,
                                   headers=get_random_ua_header()) as response:
                if response.status == 200:
                    print('有效的代理：' + proxy)
                    self.proxy_pool.put(proxy)
        except asyncio.TimeoutError as e:
            print('TimeoutError:', e)
        except aiohttp.client_exceptions.ClientProxyConnectionError as e:
            print('ClientProxyConnectionError:', e)
        except aiohttp.client_exceptions.ClientOSError as e:
            print('ClientOSError:', e)
        except aiohttp.client_exceptions.ServerDisconnectedError as e:
            print('ServerDisconnectedError:', e)
        except aiohttp.client_exceptions.ClientHttpProxyError as e:
            print('ClientHttpProxyError:', e)
        except aiohttp.http_exceptions.BadHttpMessage as e:
            print('BadHttpMessage:', e)
        except aiohttp.client_exceptions.ClientResponseError as e:
            print('ClientResponseError:', e)
        end = time.time()
        print(proxy, '测试完毕！', '消耗时间', end - start, '秒')

    def validate(self, proxies):
        """
        给定需要校验ip的列表
        """
        print('校验器开始校验...')
        start = time.time()
        try:
            async def main(loop):
                async with aiohttp.ClientSession() as session:
                    tasks = [loop.create_task(self.__validate_single_proxy(proxy, session)) for proxy in proxies]
                    await asyncio.wait(tasks)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main(loop))
        except ValueError:
            print('异步校验异常！')
        end = time.time()
        print('校验完毕！', '一共消耗', end - start, '秒')


class PoolChecker():
    """
    代理检查器，用于检查代理池的ip数量是否小于阙值
    """
    def __init__(self):
        self.getter = ProxyGetter(PROXY_SOURCE_LIST)
        self.validator = ProxyValidator()

    def is_over_threshold(self, proxy_pool):
        if proxy_pool.size() >= LOWER_THRESHOLD:
            return True
        else:
            return False

    def check_pool(self, proxy_pool):
        """
        检查代理池容量是否小于阈值，小于则调用代理ip请求器获取新的代理ip，并校验代理ip，能用的则添加到代理池中，直到达到阈值
        :param proxy_pool:  代理ip池
        :return:
        """
        print('代理池检查器开始运行...')
        while not self.is_over_threshold(proxy_pool):
            # 获取代理ip
            proxies = self.getter.get_proxy(1)
            # 校验代理ip
            self.validator.validate(proxies)
            print('当前代理ip数为', proxy_pool.size())
        print('添加完毕!当前代理池中ip数为', proxy_pool.size())


class Schedule():
    """
    调度器：用于调度检查进程和校验进程。
    """
    @staticmethod
    def valid_proxy():
        """
        校验进程：用于检查当前代理池一般的ip是否可用，
        """

        proxy_pool = ProxyPool()
        validator = ProxyValidator()
        while True:
            print('正在校验代理池中的代理ip...')
            # 只检查一半的代理ip
            count = int(0.5 * proxy_pool.size())
            if (count == 0):
                print('当前代理ip池为空，等待添加!')
                time.sleep(int(VALIDATOR_CYCLE_TIME / 2))
                continue
            proxies = proxy_pool.get(count)
            validator.validate(proxies)
            time.sleep(VALIDATOR_CYCLE_TIME)

    @staticmethod
    def check_pool():
        """
        容量检查进程：检查代理池中代理数量是否足够，不够的话新增代理ip
        """
        time.sleep(10)
        proxy_pool = ProxyPool()
        checker = PoolChecker()
        while True:
            if proxy_pool.size() < LOWER_THRESHOLD:
                checker.check_pool(proxy_pool)
            time.sleep(CHECKER_CYCLE_TIME)

    def run(self):
        print('ip代理池正在运行...')
        valid_process = Process(name="validator", target=Schedule.valid_proxy)
        check_process = Process(name="checker", target=Schedule.check_pool)
        valid_process.start()
        check_process.start()

if __name__ == '__main__':
    Schedule().run()
