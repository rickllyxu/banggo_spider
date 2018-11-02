"""
每天中午12点定时启动爬取并入库。
"""
import requests
import urllib.parse
import re
from bs4 import BeautifulSoup as BS 
import pandas as pd
import time

url_list = ["http://search.banggo.com/search/a_a_a_MC_a_a_a_a_a_a_a_a_97-202s.shtml",
        "http://search.banggo.com/search/a_a_a_MB_a_a_a_a_a_a_a_a_97-202s.shtml"]

FILE = "banggo_database.csv"

def crawler(url):
    response = requests.get(url)
    # print(type(response.content.decode()))
    return response.content.decode()

def get_page_counts(url):
    s = crawler(url)
    pattern = re.compile(r'>1/\d+<')
    match = pattern.search(s)
    if match:
        counts = match.group().strip('<>')
        return int(counts.split('/')[1])
    return 1

def parse_sku_id(s):
    pattern = re.compile(r'/\d+\.')
    match = pattern.search(s)
    if match:
        sku_id = match.group().strip("/.")
        return int(sku_id)
    else:
        print('sku_id parse failed!!!')
        return 10000000

def parse_promotion(s):
    pattern = re.compile(r'\d+折')
    match = pattern.search(s)
    if match:
        promotion = match.group().strip("折")
        if len(promotion) == 1:
            return int(promotion) * 0.1
        return int(promotion) * 0.01
    else:
        return 1.0

def get_product_list(url):
    s = crawler(url)
    soup = BS(s, "lxml")
    product_lists = soup.find_all('li', class_="mbshop_listPdCon")
    result = []
    for product in product_lists:
        product_url = product.a['href']
        sku_id = parse_sku_id(product_url)


        price_tag = product.find_all('span', class_="mbshop_listPdText")[-1]
        price_current = float(price_tag.b.get_text().strip("￥"))

        promotion_node = product.find_all('a', class_="mbshop_listPdCon_tag")
        if len(promotion_node) == 0:
            promotion = 1.0
        else:
            promotion_node = promotion_node[0]
            promotion_url = urllib.parse.unquote(promotion_node['href'])
            tags = promotion_url.split("=")[-1]
            promotion = parse_promotion(tags)
        
        # print(product_url, sku_id, price_current)
        result.append({"a_sku_id": sku_id, "c_price" : price_current * promotion, "b_url": product_url})
    return result

def store_products_data(products_list):
    #   只维护一张表格，这张table第一行是爬取日期
    #   sku_id  price1  price2  ...   price3650
    #   000000  date1   date2   ...   date3650
    #   here is the change of price of a product.
    try:
        file_product_df = pd.read_csv(FILE)
    except pd.errors.EmptyDataError:
        file_product_df = None
    current_product_df = pd.DataFrame(products_list, index=None)
    current_product_df.rename(columns={"c_price": 'd' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}, inplace=True)
    if file_product_df is not None:
        pass
    else:
        file_product_df = pd.DataFrame(columns=['a_sku_id', "b_url"])
    new_product_df = pd.merge(file_product_df, current_product_df, how="outer", on=["a_sku_id", "b_url"], sort=False)
    del file_product_df, current_product_df
    new_product_df.to_csv(FILE, index=None)

def alert():
    pass
    file_df = pd.read_csv(FILE)
    last_price_idx = str(file_df.columns[-2]) 
    now_price_idx = str(file_df.columns[-1])
    

    
if __name__ == "__main__":
    products_list = list()
    for url in url_list:
    
        page_counts = get_page_counts(url)
        # print(page_counts)
        #page_counts = 1
        for i in range(1, page_counts + 1):
            current_url = url + "?currentPage=" + str(i)
            products_list += get_product_list(current_url)  # {"sku_id": int, "price": float}
    store_products_data(products_list)
    #alert()
