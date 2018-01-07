#coding:utf-8

__doc__ = """
此模块用来获取登陆账户的订单信息，为Balance_order和Delete Pending_order操作生订单参数
使用：ws4py模块
原理：  
     'Balance_order = {"Type":3,"Data":{"MaxDeviation":50,"TransactionType":"76","OrderId":None,"Price":None}}'   
     'Delete_Pending_order = {'Type': 3, 'Data': {'OrderId':None, 'TransactionType': '77'}} '  
                                                                                 
    1.多账户登陆(Login)----客户端接收信息(Receive Data)---->获取Type1(订单详情)----提取Command 和Symbol；
    2.根据Command, Symbol将订单分类存入各个列表中；
    3.接收客户端信息Type0， 根据Command =1 or 0,Symbol值获取 Price建对应的值
    4.分别遍历订单列表，将对应Command,Symbol下的Price为每个OrderId追加Price键值对。生成单个blance_order
    5.将blance_order追加到blance_order_list中。 
    6.删除挂单操作：根据返回Type1中Command值，如果值在（2，3，4）中，即获取挂单单号。

改进：实际情况中，平仓价格为即时价格，考虑到延迟，接收-->处理-->发送.逻辑处理，有一定的时间查，故此
      Price字段取值后与真实交易情况存在误差。
"""
from ws4py.client.threadedclient import WebSocketClient
from datainfo import user_list, api_url, send_data, balance_order_data, pending_orderId_data
from tqdm import tqdm
import json
import sys
import time

order_list1 = []
order_list0 = []
Pending_Order = []
Price0 = ''
Price1 = ''
T = ''

class EchoClient(WebSocketClient):
    '''The Class EchoClient inherit from parent WebSocketClient,
    include three method. 
    - "opened" method aims to request to connect websocket server side;then
    request to login 
    - "closed" method is used to trigger an error then to close the connection between
    client and server.
    - "received_message" method is used to receive the message from server side,and to 
    the data process.
    ''' 
    def opened(self):
        for user in user_list:
            self.send(json.dumps(user))
    
               
    def closed(self, code, reason):
        print ("Closed...")
        
        
    def received_message(self,m): 
        global Price0
        global Price1
        global order_list1
        global order_list0
        global Pending_Order    
        result = json.loads(str(m))
      
        if T == "BO":
            if result["Type"] == 1:  #from Type1 source data to get OrderId
                for n in result["Data"]:       
                    if n["Command"] == 1 and n["Symbol"] == "SILVER":
                        order_list0.append(n["OrderId"])
                    elif n["Command"] == 0 and n["Symbol"] == "SILVER":
                        order_list1.append(n["OrderId"])
                    elif n["Command"] == 1 and n["Symbol"] == "GOLD":
                        pass
                    elif n["Command"] == 0 and n["Symbol"] == "GOLD":
                        pass
        
            elif (bool(Price1) == False or bool(Price0)==False):             
                if result["Type"] == 0: #from Type0 source data to get Price (Instant price)              
                    for n in result['Data']:
                        if n['Symbol'] == "SILVER":
                            Price_1 = n['Bid']
                            Price_0 = n['Ask'] 
                            while Price_0:
                                Price0 = Price0.join(str(Price_0))
                                break   
                            while  Price_1:
                                Price1= Price1.join(str(Price_1))
                                break
                            self.close()
        
        
        elif T == "DP":
            if result["Type"] == 1: 
                for n in result["Data"]:                
                    if n["Command"] in (2,3,4): # get to Pending_OrderId
                        print ("2,3,4")
                        Pending_Order.append(n["OrderId"])
                        self.close()                        


def main():
    '''
    - be used to start application.
    - connected server side
    - from receiving message to collect OrderId,encapsulated into independent dictionary . then storage a list.
    - generate the blance_order_list
    - return blance_order_list
    '''
    balance_order_list =[]
    Pending_Order_list = []
    global T
    T = input(str("Chose Trade Type:[DP-(Delete pending_order)/BO-(Blance_order)]"))
    
    if T == "BO":  # chose Balance_order operation
        print ("Collecting balance order....Pls wait moment!")
        try:
            ws = EchoClient(api_url)
            ws.connect()
            ws.run_forever()
            
        except KeyboardInterrupt:
           ws.close()

        if order_list0 or order_list1:
            print (order_list1)
            for id0 in order_list0:
                balance_order = balance_order_data
                balance_order["Data"]["OrderId"] = id0     
                balance_order["Data"]["Price"] = Price0
                balance_order_list.append(balance_order)
             
            for id1 in order_list1:
                #blance_order = {"Type":3,"Data":{"MaxDeviation":50,"TransactionType":"76"}}
                balance_order["Data"]["OrderId"] = id1
                balance_order["Data"]["Price"] = Price1
                balance_order_list.append(balance_order)
            
            for balance_order in tqdm(balance_order_list): # processing bar display
                time.sleep(0.0005)
                
            print ("finished....")
            return balance_order_list
        else:
            print ("The Balance OrderId is Empty!")
    
    elif T == "DP": #Chose Delete_pending_order operation
        print ("Collecting Pending_Orderlist....Pls wait moment!")
        try:
            ws = EchoClient(api_url)
            ws.connect()
            ws.run_forever()
        except KeyboardInterrupt:
           ws.close()

        if Pending_Order:
            for i in tqdm(Pending_Order): # processing bar display
                time.sleep(0.02)
                
            for pn in Pending_Order:
                pending_orderId = pending_orderId_data
                pending_orderId["Data"]["OrderId"] = pn
                Pending_Order_list.append(pending_orderId)
                
            return Pending_Order_list        
        else:
            print ("The Pending OrderId is Empty!")
        
    else:
        print ("INPUT WRONG KEYWORD")

   
if __name__ == "__main__":
    print(main())
    
        