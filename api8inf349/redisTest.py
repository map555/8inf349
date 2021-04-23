from redis import Redis
import pickle
class Test():
    def __init__(self,a,b):
        self.a=a
        self.b=b



redis=Redis.from_url("redis://localhost")
#print(redis.get("2"))
#redis.set("1",pickle.dumps(Test(1,2)))
#x=pickle.loads(redis.get("2"))
#print(x)
redis.flushall()