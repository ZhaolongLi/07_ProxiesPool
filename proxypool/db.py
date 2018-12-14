# coding:utf-8

import redis
import re
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY
from proxypool.setting import MAX_SCORE,MIN_SCORE,INITIAL_SCORE
from random import choice


# 代理存储模块
class RedisClient(object):
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis地址
        :param port: Redis端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host,port=port,password=password,decode_responses=True,db=0)

    def add(self,proxy,score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        # print("add")
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+',proxy):
            print('代理不合规范',proxy,'丢弃')
            return
        if not self.db.zscore(REDIS_KEY,proxy):
            # print('tow')
            # self.db.zadd(REDIS_KEY,score,proxy)
            # self.db.zadd(REDIS_KEY,{proxy:score})
            # print('******************')
            return self.db.zadd(REDIS_KEY,{proxy:score}) # redis3.0有变化，zadd(name,mapping={value:score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            raise PoolEmptyError

    def decrease(self,proxy):
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY,proxy)
        if score and score > MIN_SCORE:
            print('代理',proxy,'当前分数',score,'减1')
            return self.db.zincrby(REDIS_KEY,-1,proxy) #redis3.0有改变 zincrby(name,amount,value)
        else:
            print('代理',proxy,'当前分数',score,'移除')
            return self.db.zrem(REDIS_KEY,proxy)

    def exists(self,proxy):
        """
        判断是否存在
        :param proxy:代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY,proxy) == None

    def max(self,proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理',proxy,'可用，设置为',MAX_SCORE)
        # return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)
        return self.db.zadd(REDIS_KEY,{proxy:MAX_SCORE})

    def count(self):
        """
        获取数量
        :return:数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)

    def batch(self,start,stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY,start,stop-1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680,688)
    print(result)