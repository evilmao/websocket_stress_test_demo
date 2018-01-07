#!/usr/bin/env python
#coding:utf-8

'''
    Version:V1.2
    1.Websocket客户端用来连接web service,获取请求网站信息;
    2.使用websocket模块建立连接，json模块序列化参数
    3.threadpool控制线程数
    4.windows环境下进行测试
'''
#导入相关模块
import websocket
from websocket import create_connection
from PendingInstantOrder import CreateData
from Balance_Delete_Order import BalanceOrder
from datainfo import user_list,api_url
import threading
import threadpool  
import time
import json
import sys

def ws_client(data):
    try:
        ws = create_connection(api_url)
        t1 = time.time()
        ws.send(json.dumps(data))
        ws.send(Instant_Pending_data) #即时订单
        ws.send('{"Type":128}')
        t2=time.time()
        with open("send_successfully.txt",'+a') as f:
             f.write("usetime:{}\n".format(str(t2-t1)))   
        print ("successfully")

    except Exception as e:
        with open ('log.txt','a+') as f:
            f.write("login failed \n")
        
'''主程序入口'''
if __name__ == "__main__":
    AccountList = user_list   #Simulate the number of account！
    #Instant_Pending = CreateData()
    Instant_Pending_data = json.dumps(CreateData()[0],separators=(',',':'))
    #Balance_order_data = BalanceOrder()
  
    pool = threadpool.ThreadPool(20) 
    requests = threadpool.makeRequests(ws_client,AccountList )
    start_time = time.time()    
     
    [pool.putRequest(req) for req in requests] 
    pool.wait() 
    dur_time = time.time()-start_time
    print (dur_time)   
    
    print ("finished!")
           

    
            
    

            




