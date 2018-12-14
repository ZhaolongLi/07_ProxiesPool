# coding:utf-8

from proxypool.db import RedisClient


conn = RedisClient()

def set(proxy):
    """
    添加代理
    :param proxy:
    :return:
    """
    result = conn.add(proxy)
    print(proxy)
    print("录入成功" if result else "录入失败")

def scan():
    print("请输入代理，输入exit退出读入")
    while True:
        proxy = input()
        if proxy == 'exit':
            break
        set(proxy)

if __name__ == '__main__':
    scan()
