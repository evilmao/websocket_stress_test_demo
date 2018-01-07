#!/usr/bin/env python
#coding:utf-8

__doc__ = """
The  module through two functions to get the Instant price.

Initially the rationale was to:
- After Login a account,when a customer need to continue make a instant 
  Order.It is logical to get the price data by the server-side then to
  insert the Order_type data. Also can test many time only one account !
  
- the function of the  function-name of "main" is created the Instant_order_list and Pending_order_list  
- the function-name of "on_message" is a method attribute of websocket class,
  through receive the message from Server side to get the instant price.
"""
import websocket
from datainfo import user_list, api_url, send_data
import json
import sys

Price1 = '' 
def on_message(ws, message):
    global Price1

    result = json.loads(message) # receive message from server side then to serialization
    if (bool(Price1) == False): 
        if result['Type'] == 0:
            for Type_0 in result['Data']:
                if (Type_0['Symbol'] == Symbol):
                    if Command == 0: # buy operation
                        Price = Type_0['Ask'] # use 'Ask' value from Type0 source data
                        while Price:
                            Price1 = Price1.join(str(Price))
                            ws.close()
                            break    
                    elif Command == 1 or Command == 2: # Sell operation
                        Price = Type_0['Bid']  # use "Bid" value from Type0 source data
                        while Price:
                            Price1 = Price1.join(str(Price))
                            ws.close()
                            break


def CreateData():
    Instant_order_list = []
    Pending_order_list = []
    global Symbol,Command,T
    
    websocket.enableTrace(True)                # Test Server WebSocket URL
    ws = websocket.WebSocketApp(api_url)
    T = str(input("Order Type [IO--instant order /PO-- pending order]:"))
    data = send_data[T]
    
    try:
        flag = 0
        while flag < 3:
             Command = int(input("pls input 'Command'[0/1/2]:")) 
             if Command == 1 or Command == 0:
                 while flag <3:
                     Symbol= input(str("Pls select Symbol:['GOLD/SILVER']"))
                     if Symbol == "GOLD" or Symbol == "SILVER":
                         ws.on_message = on_message
                         ws.run_forever()
                         
                         #print (str('%.3f'%(float(Price1)-0.070)))
                         data['Data']['Command'] = Command
                         data['Data']['Symbol'] = Symbol
                         data['Data']['Price'] = Price1
                                      
                         Instant_order_list.append(data)   
                         return Instant_order_list 
                         break
                     else:
                         flag+=1
                         print ("***WARNING!*** Input wrong type!")
                 break
                          
             elif Command == 2: # Pending_order parameter created
                 while flag <3:
                     Symbol= input(str("Pls select Symbol:['GOLD/SILVER']"))
                     if Symbol == "GOLD" or Symbol == "SILVER":
                         ws.on_message = on_message
                         ws.run_forever()
                         
                         data['Data']['Command'] = Command
                         data['Data']['Symbol'] = Symbol
                         data['Data']['Price'] = str('%.3f'%(float(Price1)-0.070))
                         data['Data']["TakeProfit"] = Price1
                         data['Data']["StopLoss"] = str('%.3f'%(float(Price1)-0.130))
                         
                         Pending_order_list.append(data)
                         return Pending_order_list
                         break
                     else:
                         flag+=1
                         print ("Seems to input wrong numer,retry!")
                 break

    except Exception as e:
        raise 


'''---------------测试模块入口--------------------'''
if __name__ == "__main__":
    print(CreateData())
    
    



