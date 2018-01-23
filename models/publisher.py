'''
Created on Jan 18, 2018

@author: gustavo
'''
import redis


class Publisher(object):
    
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379)
    
    def publish(self, topic, data):
        self.r.publish(topic, data)
