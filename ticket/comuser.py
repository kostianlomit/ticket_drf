import redis


with redis.Redis() as redis_client:
    print("RANDOM num IS", redis_client.brpop("list"))