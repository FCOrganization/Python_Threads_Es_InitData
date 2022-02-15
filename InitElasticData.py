from datetime import datetime
from elasticsearch import Elasticsearch
import threading
import time
import uuid

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        elastic_data_init(self.threadID, self.name, self.counter)
 
 
def elastic_data_init(threadID, name, counter):
    c=0
    for num in range(0,counter):
        id=uuid.uuid1()
        doc = {
            'id': id,
            'author': '一个神奇的作者，编号是'+str(c),
            'bookName':'神奇的书名，编号是'+str(c),
            'updateTime': datetime.now(),
            'content':'这就是神奇的正文内容，编号是'+str(c)
        }
        res = es.index(index="book-info", id=id, body=doc)
        c+=1
        print(threadID, name, counter,c),

singlethread_data_num=1000
thread_num=10
thread_list = []

def init_thread():    
    
    for t in range(0,thread_num):
        thread_list.append(myThread(t,"Thread-"+str(t),singlethread_data_num))

def start():
    init_thread()

    for t in thread_list:
        t.start()
 

start()



es.indices.refresh(index="book-info")