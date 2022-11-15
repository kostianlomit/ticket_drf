import time
from string import ascii_letters
import random
import redis

#  Создание ключа
#
redis_client = redis.Redis(host="localhost", port=6379, db=0)
#
# print(redis_client.set(name='test_key', value=10))
#
# print(redis_client.get('test_key'))
# redis_client.close()


# Увеличение значение по ключу
# with redis.Redis() as redis_client:
#     redis_client.set('Kostia', 1)
#
#     while True:
#         redis_client.incrby('Kostia', 10)
#         time.sleep(1)
#
#         print(redis_client.get('Kostia'))


# создание рандомных ключей и итерация по ним
# with redis.Redis() as redis_client:
#        for k in  redis_client.scan_iter('*', count=100):
#            print(k, redis_client.get(k))


with redis.Redis() as redis_client:
    redis_client.lpush('list', random.randint(0, 100))


