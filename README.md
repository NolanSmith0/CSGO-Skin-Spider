# CSGO-Skin-Spider

您好！ 该项目为[网易Buff](https://buff.163.com/?game=csgo)和[IGXE](https://www.igxe.cn/market/csgo?sort=3)CSGO游戏皮肤价格爬虫脚本，由以下部分组成：

- ```0 Demo.ipynb``` : requests爬虫的演示(```CSGO_Skin_spider.py```的简化版)，您可以在本文件中简单体验该项目的功能，查看爬取好的结构数据
- ```0.5 Selenium Spider``` : 使用selenium实现的buff爬虫，运行一次半小时左右，收集一万两千条左右数据，但缺点是极其容易被封号（需要有buff帐号登陆才能爬）。
- ```1 Data Visualization``` : 编写的简单的数据可视化文件并设计了一个简单的市价指数，还有待补充更多。
- ```2 selenium url collector``` : 主体借助selenium实现的buff皮肤url爬取工具，我后来又用它改了改爬igxe的。因为是在ubuntu环境下写的，在其他机器运行时需重新修改webdriver参数。
- ```CSGO_Skin_spider.py``` : 主体程序，每爬取一次获取两万两千多条左右的数据，耗时大概50分钟(有代理ip可以反比例縮短时间)。爬取Buff和IGXE的价格数据
- ```./price_data/``` : 存储爬取的buff数据的文件夹(我提供了6-2到6-22日的价格数据，每天两次)
- ```./IGXE_price``` : 存放IGXE数据的文件夹
- ```Buff_URLs.csv``` 和 ```IGXE_URLs.csv``` : 通过selenium获取的buff和IGXE所有皮肤的url

# 数据分析：
待完成......
