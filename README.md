---

---

## <center> XSwebsocket 压测程序文档说明

### 测试对象

-  XS 交易平台

-  API接口地址：<wss://testtradeapi2.xs9999.com:4431/trade>

-  测试行为：

   >  1.Login(登录)
   >
   >  2.Instant_Trade(即时交易)
   >
   >  3.Pending_Trade(挂单)
   >
   >  4.Balance_Trade(平仓)
   >
   >  5.Delete_Pending_Trade(删除挂单)

### 环境

*  程序运行环境：Centos7(Linux 建议) / Win10 
*  配置： 2G/RAM , Core(1) i5-7600 CPU @ 3.50GHz

### 编程开发语言 

*  Python3.5
*  模块：ws4py (python websocket-client 封装的第三方库)
*  自定义模块PendingInstantOrder 和 Balance_Delete_Order
*  面向对象+模块化编程

### 实现原理

*  基于python3 第三方模块ws4py.client 下的WebSocketBaseClient 类，生成客户端实例 client， 使用ws4py.manager下的WebSocketManager类

   构建epoll 异步I/O模型，实现并发下的异步操作；

*  以管理员权限 在MT4 Manager平台注册100个测试用户，设置统一的passwd(方便操作)，并分别注资10,000$.

*  客户端数目： 将100个测试用户循环10次,以列表的格式存储在内存中生成1000个测试账户。

*  并发实现：使用epoll模型下的WebSocketManager模块，循环生成

*  数据分析 

   >  1. `Login`:  每次请求发送用户参数并标记开始的时间戳`t1`，根据从接收服务端返回的数据中提取出Type8的数据类型与否，判断Login行为是否成功（发送--->接收），每接收到1次`Type8`标记成功1次写入本地文件，并记录下结束时间戳`t2`，计算单次请求时间` t2-t1`，写入本地文件；1000组用户请求完成后，自动退出程序; 根据Type8条目数 n1/1000*100% 得到成功率；根据平均时间获得平均请求时间； 连续执行三次测试，最后取平均值作为最后的压测结果。
   >
   >  2. `Instant_Trade :`（生成即时订单交易参数)--->(Login)--->(Send 即时交易参数)--->(receive Type1). 首先利用PendingInstantOrder模块根据用户选择`Symbol，Command`的值确定即时Price价格，将获得的价格插入到新的请求参数中，同用户登录数据一起发送至服务端，根据是否返回的Type1数据类型且Command=0/1判断`Instant_Trade`成功与否。请求时间参考行为1（Login），测试3次，取平均值。
   >
   >     `方案2` : 执行发送数据后，单独运行模块` Balance_Delete_Order.main()`选择`BO(Balance_Order)`获得100组用户的所有即时订单信息，根据订单`OrderId`数目，获取成功率。(优点：更接近真实值，缺点，分部操作)
   >
   >  3. Pending_Trade：原理同行为2(Instant_Trade)，根据是否返回的Type1数据类型且Command=2/3/4判断`Instant_Trade`成功与否。
   >
   >     `方案2`：同行为2中方案类似，用户选择DP(Delete_Pending_order),获得100组用户的所有挂单操作信息，根据订单`OrderId`目，获取成功率。
   >
   >  4. `Balance_Trade: `  (获取Pending_order_list)--->(Login)--->(send Pending_order-)-->(获取Pending_order_list) . 运行模块 Balance_Delete_Order.main() 获取挂单列表，登录用户操作发送参数，请求完毕后，退出程序，再次获得Balance_order,根据，根据订单`OrderId`数目，获取成功率。
   >
   >  5. `Delete_Trade`: 原理同行为4

   ​

### 测试参数

*  成功率
*  平均响应时间

### 流程图

![](http://ww1.sinaimg.cn/large/8599e4cfly1fkfiah6tc2j20qk0fwgmk.jpg)