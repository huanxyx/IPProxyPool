# IP代理池
## 说明（依赖）
- requests库
- BeautifulSoup4库
- aiohttp库
- redis库
- flask库

## 相关模块
- run.py：运行
- setting.py：配置文件
    - Redis配置
    - 校验器配置
    - 检查器配置
    - 代理ip获取源配置
    - RESTFUL接口配置
- getter.py：爬虫模块，用来抓取代理源网站的代理
    - ProxyGetter：获取器
- ipsource.py：代理源，用来获取代理的的源对象，可以复写
    - ProxyIPSource：ip代理源的模板（充当接口）
    - ThuanProxySource：幻代理的代理源
    - KuaiProxySource：快代理的代理源
- schedule.py：调度器模块
    - ProxyValidator：代理校验器，异步校验代理ip
    - PoolChecker：代理检查器，用于检查代理池的ip数量是否小于阙值
    - Schedule：调度器，用于调度检查进程和校验进程
- proxypool.py：代理池，本质上是操作redis
- api.py：Http接口，启动一个Web服务器，利用Flask实现，对外提供代理的获取功能。
- headergetter.py：用来获取随机User-Agent头的模块