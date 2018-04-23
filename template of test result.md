

<center>鑫圣金业线上服务器压测数据

测试时间

15/11/2017

环境

- 程序运行环境：Centos7(Linux 建议) / Win10 
- 配置： 2G/RAM , Core(1) i5-7600 CPU @ 3.50GHz

编程开发语言

- Python3.5
- 模块：websocket 
- 自定义模块PendingInstantOrder 和 Balance_Delete_Order
- 面向对象+模块化编程

实现原理

- 基于python3 第三方模块websocket-client 下的，生成客户端实例 client， 使用threading(多线程模块) + threadpool (线程池)
  实现并发下的异步操作；线程池控制单位时间向服务端发送的请求数。
- 以管理员权限 在MT4 Manager平台注册100个测试用户，设置统一的passwd(方便操作)，并分别注资10,000$.
- 客户端数目： 将100个测试用户循环10次,以列表的格式存储在内存中生成1000个测试账户。
- 并发实现：使用threadpool.makeRequests方法将控制并发数，同时向服务器发送请求！初步请求数为300.
- 数据分析 
  1. Login:本次旨在测试交易行为。
  2. Instant_Trade :实行发送/接收数据分离，服务端只需关注是否发送成功。记录每次发送时间值记作单次 请求时间。1000组用户发送完成后。客户端记录请求成功数据即可！根据每秒请求数控制并发数！
  3. 发送--接收时间取自MT4

Test Object

- XS 交易平台
- API接口地址：wss://tradeapitest.xs9999.com:4431/trade
                		wss://tradeapitest.xs9999.com:4441/trade
- 测试行为：
  1.Instant_order(即时交易)

### Test Result

1. 对比结果如下
   

      

## 对比结果如下
![](http://ww1.sinaimg.cn/large/8599e4cfly1fliwcp47ntj20ks09ujru.jpg)


