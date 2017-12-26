'''
Created on Dec 25, 2017

@author: gustavo
'''
import redis


class Subscriber(object):
    
    def __init__(self, handlers):
        r = redis.StrictRedis(host='localhost', port=6379)
        self.p = r.pubsub()# See https://github.com/andymccurdy/redis-py/#publish--subscribe
        self.p.subscribe(**handlers)
    
    def run(self):
        self.p.run_in_thread(sleep_time=0.001)


if __name__ == "__main__":
    
    import time
    
    def handler(msg):
        print("handler: %s" % msg)
        
    s = Subscriber({"test_topic": handler})
    s.run()
    
    while True:
        time.sleep(1)