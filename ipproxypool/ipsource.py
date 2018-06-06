from bs4 import BeautifulSoup

'''
    两个代理源（幻代理，快代理）
'''

class ProxyIPSource(object):
    '''
    代理IP源的实现模板：
    '''
    def __init__(self):
        self.page = 1
        self.url = ''

    '''
    获取当前访问页面的url
    '''
    def get_url(self):
        return self.url.format(page=self.page)

    '''
    换到下一页
    '''
    def next_page(self):
        self.page += 1

    """
    获取当前页号
    """
    def cur_page(self):

        return self.page

    '''
    重置页数
    '''
    def reset_page(self):
        self.page = 1

    '''
    解析获取页面中的代理ip，不同的代理ip源有不同的解析方式
    '''
    def parse_content(self, content):
        return []


class IhuanProxySource(ProxyIPSource):
    '''
        幻代理
    '''

    def __init__(self):
        self.page = 1
        self.url = 'https://ip.ihuan.me/?page={page}&address=5Lit5Zu9'

    def parse_content(self, content):
        soup = BeautifulSoup(content, 'lxml')
        soup_items = soup.select("tbody > tr")

        items = []
        for soup_item in soup_items:
            ip = soup_item.find('a').get_text()
            port = soup_item.find_all('td')[1].get_text()
            items.append(ip + ":" + port)
        return items


class KuaiProxySource(ProxyIPSource):
    '''
        快代理
    '''

    def __init__(self):
        self.page = 1
        self.url = 'https://www.kuaidaili.com/free/inha/{page}/'

    def parse_content(self, content):
        soup = BeautifulSoup(content, 'lxml')
        items_soup = soup.select('tbody > tr')

        items = []
        for item_soup in items_soup:
            ip = item_soup.find('td', attrs={"data-title":"IP"}).get_text()
            port = item_soup.find('td', attrs={'data-title':'PORT'}).get_text()
            items.append(ip + ":" + port)
        return items

