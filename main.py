from urllib.request import urlopen
from bs4 import BeautifulSoup as bf
import re
import pandas as pd
import os
import time
import random
import urllib.request

# def parser_html(url):
#     # sleep = random.random() * 2
#     # print("***sleep***{}s***".format(sleep))
#     # time.sleep(sleep)
#     html = urlopen(url)
#     obj = bf(html.read(), 'html.parser')
#     return obj


def parser_html(url):
    sleep = random.random() * 2
    print("***sleep***{}s***".format(sleep))
    time.sleep(sleep)
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/51.0.2704.63 Safari/537.36'
    }
    req = urllib.request.Request(url=url, headers=headers)
    res = urllib.request.urlopen(req)
    obj = bf(res.read(), 'html.parser')
    return obj


def init():
    if os.path.exists("applePrice.xlsx"):
        os.remove("applePrice.xlsx")


def wr_excel(data, name, n):
    df = pd.DataFrame(columns=name, data=data)
    df.to_excel(n + ".xlsx", index=False)


if __name__ == "__main__":
    name = ['Date', 'Price']
    content_title = []
    content_all = []
    init()
    obj = parser_html(
        "https://jiage.cngold.org/shuiguo/pingguo/list_3160_all.html")
    header = obj.find_all('div', class_="history_news")
    for _i, h in enumerate(header):
        title = h.select(".history_news_title")[0].string
        if '2016' not in title:
            continue
        print("获取" + title)
        content_title.append(title)
        ahref = h.find_all('a')
        content_year = []
        # 获取所有日期的链接
        a_len = len(ahref)
        for _j, a in enumerate(ahref):
            content_date = []
            # 获取一个日期
            date = a['href'].split('/')[-2]
            if "2016-07-22" in date:
                continue
            content_date.append(date)
            # print(date)
            # 获取该日期的html
            a_obj = parser_html(a['href'])
            # 找到对应的苹果价格链接
            a_obj_href = a_obj.find_all('a',
                                        string=re.compile('今日苹果'))[-1]['href']
            # 获取当日苹果价格的html
            a_obj_href_obj = parser_html(a_obj_href)
            # 获取表格
            price_table = a_obj_href_obj.select('table')[0]
            price = price_table.find_all('tr')[3].select(
                'td')[1].string.replace('\n', '')
            content_date.append(price)
            print("({}/{}):{}".format(_j, a_len, content_date))
            content_year.append(content_date)
        wr_excel(content_year, name, content_title[_i])
        content_all.append(content_year)
    # with pd.ExcelWriter('applePrice.xlsx') as writer:  # doctest: +SKIP
    #     for _id, y in enumerate(content_all):
    #         df = pd.DataFrame(columns=name, data=y)
    #         df.to_excel(writer, sheet_name=content_title[_id], index=False)