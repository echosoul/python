#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
自动登录51cto网站签到，领取下载豆和无忧币
by 2017-4-12
'''
import requests
import random
from bs4 import BeautifulSoup

if __name__ == '__main__':
    header = {
        'Referer': 'http://home.51cto.com/index',
        'User-Agent': 'Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML, like Gecko)\
        Chrome / 51.0.2704.79 Safari / 537.36 Edge / 14.14393'
    }

    # 获取_csrf的值
    url_get = 'http://home.51cto.com/index'
    req = requests.session()
    res_get = req.get(url_get, headers=header)
    soup_get = BeautifulSoup(res_get.text, 'lxml')
    csrf = soup_get.findAll('input', {'name': "_csrf"})[0].attrs['value']

    # 构建post参数，登录网站
    data_post = {
        '_csrf': csrf,
        'LoginForm[username]': 'huzunhe1024@126.com',
        'LoginForm[password]': 'xiao@fo&676',
        'LoginForm[remenberMe]': '0',
    }
    url_post = 'http://home.51cto.com/index'
    res_post = req.post(url_post, data=data_post, headers=header)

    # 领取下载豆
    down_url = 'http://down.51cto.com/download.php'
    down_data = {'do': 'getfreecredits', 't': random.random()}
    down_res = req.post(down_url, params=down_data, data=down_data)
    print(down_res.text)

    req.close()
