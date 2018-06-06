from ipproxypool.schedule import Schedule
from ipproxypool.api import app
from ipproxypool.setting import RESTFUL_PORT

def main():
    print('调度器开启！')
    schedule = Schedule()
    schedule.run()
    print('Restful接口开启！')
    app.run(port=RESTFUL_PORT)

if __name__ == '__main__':
    main()