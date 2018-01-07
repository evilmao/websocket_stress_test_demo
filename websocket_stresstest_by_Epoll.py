#coding:utf-8
'''
-- 简化版本，客户端发送模拟用户不用组给服务端，客户端记录发送成功与否并记录时间
-- 不需要服务端返回的数据！
'''
from ws4py.client import WebSocketBaseClient
from ws4py.manager import WebSocketManager
from ws4py import format_addresses, configure_logger
from  PendingInstantOrder import CreateData
from Balance_Delete_Order import main
from datainfo import user_list,api_url
import json
import time

logger = configure_logger()
m = WebSocketManager()

class EchoClient(WebSocketBaseClient):
    def handshake_ok(self):
        m.add(self)       
        try:
            t = time.time()
            self.send(payload)
            self.send(Instant_Pending)
            t1 =time.time()
            self.close()
                
        except Exception as e:
            print ("Failed!")
            with open("/test-api/websocket-client/return_data/return_login/Login_error.txt",'+a') as f:
                f.write('The {}user login failed!\n'.format(count))
                self.close()

    def closed(self,code,reason):
        print ("closed!")

if __name__ == '__main__':
    import time  
    Instant_Pending = json.dumps(CreateData())    
    count = 0
    try:
        m.start()
        start_time = time.time()
        for i in user_list:
            payload = json.dumps({"Type":7,"Data":i})
            print (type(payload))
            client = EchoClient(api_url)           
            client.connect()
            count+=1
        logger.info("%s clients are connected" % count)

        while True:
            for ws in m.websockets.values():
                if not ws.terminated:
                   dur_time = time.time()-start_time
                   print (dur_time)
                   break
            else:
                break
            time.sleep(3)              
            
    except KeyboardInterrupt:
        m.close_all()
        m.stop()
        m.join()
        
        