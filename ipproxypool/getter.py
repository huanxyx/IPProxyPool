
import requests
import time

from ipproxypool.headergetter import get_random_ua_header
from ipproxypool.setting import *

class ProxyGetter(object):
    """
    代理ip请求器
    """
    def __init__(self, proxy_source_list):
        """
        初始化代理ip源
        :param proxy_source_list:  代理ip源
        """
        if len(proxy_source_list) == 0:
            raise Exception('没有代理ip的来源')
        self.proxy_source_list = proxy_source_list[:]

    def get_proxy(self, page_num):
        """
        获取指定页数的代理ip。
        注意：是每个代理ip源的page_num页
        :param page_num:   指定页数
        :return:    代理ip
        """

        # content_list 存储着 (请求得到的页面，IP代理源)
        content_list = []
        for _ in range(page_num):
            for proxy_source in self.proxy_source_list:
                content = self.__get_page_content(proxy_source)
                if content != None:
                    content_list.append(content)

            # 用于避免爬取同一个网站太过频繁
            if len(self.proxy_source_list) == 1:
                time.sleep(1)

        return self.__parse_all_content(content_list)

    def __parse_all_content(self, content_list):
        """
        解析所有获得的页面，并获取代理ip
        :param content_list:    (请求得到的页面，IP代理源)
        :return:    一个set集合，用来避免重复的数据
        """
        proxy_list = set()
        if content_list != None:
            for content, proxy_source in content_list:
                temp_list = proxy_source.parse_content(content)
                proxy_list.update(temp_list)
        return proxy_list

    def __get_page_content(self, proxy_source):
        """
        抓取当前源一页数据
        :param proxy_source: 代理源
        :return:    (当前源请求得到的页面，IP代理源)
        """
        if proxy_source.cur_page() > PROXY_SOURCE_MAX_PAGE:
            proxy_source.reset_page()
        url = proxy_source.get_url()
        header = get_random_ua_header()
        print('正在从' + url + '获取代理ip...')
        with requests.get(url, headers=header) as response:
            if response.status_code == 200:
                print('从' + url + '获取完毕。')
                proxy_source.next_page()
                return response.text, proxy_source
            else:
                print('从' + url + '获取失败。')



if __name__ == '__main__':
    from ipproxypool.ipsource import KuaiProxySource, IhuanProxySource
    getter = ProxyGetter([KuaiProxySource(), IhuanProxySource()])
    proxies = getter.get_proxy(5)
    print(proxies)
    print(len(proxies))




