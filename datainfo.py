#coding：utf-8

'''
    1.用来存储数据压力测试账号，处理数据的函数
'''
accountdata = [
                {"Login":100148519,"Password":"MYF911"},
            ]

user_list = [ {"Type":7,"Data":user} for user in accountdata]

send_data = {
                'IO':
                     {"Type":3,"Data":{"TransactionType":75,"MaxDeviation":10,"Volume":1}},
                'PO':
                    {"Type":3,"Data":{"TransactionType":75,"Volume":1,"ExpiryType":0,"Expiration":"1970-1-1"}}
            }
balance_order_data = {"Type":3,"Data":{"MaxDeviation":50,"TransactionType":"76"}} #平仓基础参数
pending_orderId_data = {"Type":3,"Data":{ "TransactionType":"77"}} #删除挂单基础参数
api_url = 'wss://testapi:8001'



if __name__ == '__main__':
    print (user_list)
