这是一个用于某小型电商网站上展示历史价格的插件。

## Motivation

由于常规的比价插件并没有记录该网站的历史价格数据，因此我开发了这个插件，可以爬取价格，并且将历史价格展示到电商网站的物品浏览页上。

## 插件结构

- `spider.py` 是一个爬虫，将爬取电商网站上的商品，并写入 `banggo_database.csv` 中。
- `banggo_monitor/` 是一个chrome extension，需要在开发者模式下安装，它向后端请求历史价格数据。
- `price_query/` 是一个提供Restful服务、与上述chrome extension交互的后端模块。根据上述扩展提供的sku_id，它去查询数据库中的历史价格数据并返回。

## 使用

- 定期启动 `spider.py` 来更新价格数据库。
- 安装 `banggo_monitor`。
- 运行price_query/下的`main.py`，提供Restful服务。

