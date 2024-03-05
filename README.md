# CSGO-Skin-Spider

**English Intro**

Hi! The project is a web scraper designed for two cs2 trading platforms in China [Buff](https://buff.163.com/?game=csgo) and [IGXE](https://www.igxe.cn/market/csgo?sort=3)

This is also my final project for Course Python based data analytics, 2022 II, SDU.

This project has following parts:

- ```0 Demo.ipynb``` : Demo for Scraper implemented using requests, you can test this project and its outputs.
- ```0.5 Selenium Spider``` : Scraper imlemented using selenium, which is able to collect 12k data within half hour, but it's pretty easy to get banned。
- ```1 Data Visualization``` : A simple data visualization code, more to add。
- ```2 selenium url collector``` : Scraper implemented using selenium, designed for collecting skin ids。
- ```CSGO_Skin_spider.py``` : Main codes, scraper designed using requests, collecting 20k data within 2 hours, can speed up if with proxies.
- ```./price_data/``` : Folder containing buff's data, I provided 2023.6.2-2023.6.22 's data.
- ```./IGXE_price``` : Folder containing IGXE's data.
- ```Buff_URLs.csv``` 和 ```IGXE_URLs.csv``` : All skin urls.

---

**Chinese Intro**

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

``` Time Series Analysis``` : 目前只做了一些简单的自相关分析，有待数据丰富后进一步完善。
