#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

'''
下载蜻蜓FM专辑的所有音频, by 2017-4-13
'''

import os
import urllib.request
from bs4 import BeautifulSoup
import json

if __name__ == '__main__':
    channel_url = 'http://www.qingting.fm/channels/149704'
    channel_num = channel_url.split(r'/')[-1]
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    }
    req = urllib.request.Request(channel_url, headers=header)
    res = urllib.request.urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')
    page_count = soup.find('ul', {'class': 'pagination'}).findAll(
        'a', {'data-reactid': True})
    page_count = int(page_count[-2].text)
    print('该专辑共有 %s 页' % page_count)

    path = os.path.join(r'C:\qingting', channel_num)
    if not os.path.exists(path):
        os.mkdir(path)

    for n in range(1, page_count + 1):
        print('开始下载第 %d 页的音频' % n)
        referer_n = channel_url + r'/' + str(n)
        header_n = {
            'Referer': referer_n,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        }
        url_n = 'http://i.qingting.fm/wapi/channels/' + \
            channel_num + r'/programs/page/' + str(n) + r'/pagesize/10'
        req_n = urllib.request.Request(url_n, headers=header_n)
        res_n = urllib.request.urlopen(req_n).read().decode('utf-8')
        sounds = json.loads(res_n)

        for s in sounds['data']:
            filename = s.get('name')
            filepath = 'http://od.qingting.fm/' + s.get('file_path')
            urllib.request.urlretrieve(
                filepath, os.path.join(path, filename) + r'.m4a')
            print('第 %d 页：%s.m4a 下载完成' % (n, filename))
        print('第 %d 页下载完毕' % n)
    print('专辑 %s 下载完成' % channel_num)
