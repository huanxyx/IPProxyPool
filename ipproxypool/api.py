from flask import Flask

from ipproxypool.proxypool import ProxyPool
"""
RESTFUL接口
"""

app = Flask(__name__)

@app.route('/')
def index():
    return "<h2>提供免费代理！</h2>" \
           "<ul>" \
           "<li>/get：获取代理ip</li>" \
           "<li>/count：获取的代理ip的数量</li>" \
           "</ul>"

@app.route('/get')
def get_proxy():
    """
    获取代理数
    """
    proxy_pool = ProxyPool()
    proxy = proxy_pool.pop()
    return proxy

@app.route('/count')
def get_counts():
    """
    获取代理ip数
    """
    proxy_pool = ProxyPool()
    return str(proxy_pool.size())

if __name__ == "__main__":
    app.run()


