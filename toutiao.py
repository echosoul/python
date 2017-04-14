#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import re
import json
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


def _create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def _get_query_string(data):
    return urllib.parse.urlencode(data)


def get_article_titles_urls(req):
    res = urllib.request.urlopen(req).read().decode('utf-8')
    d = json.loads(res).get('data')
    if d is None:
        print('数据全部请求完毕')
        return
    titles = [article.get('title') for article in d]
    urls = [article.get('article_url') for article in d]
    return titles, urls


def get_images(save_dir, url):
    req = urllib.request.Request(url, headers=request_headers)
    res = urllib.request.urlopen(req).read().decode('utf-8')
    content = re.findall(
        r'<div class="article-content"><div><p>(.*)</p></div></div>', res)
    if len(content) > 0:
        #print(content)
        items = re.findall(r'<img src="(.*?)"', content[0])
        for it in items:
            save_file = it.split(r'/')[-1] + r'.jpg'
            urllib.request.urlretrieve(it, os.path.join(save_dir, save_file))
            print('保存图片 %s' % save_file)
    else:
        print('当前方法未找到图片')


if __name__ == '__main__':
    offset = 0
    root_dir = _create_dir('C:\jiepai')
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Referer': 'http://www.toutiao.com/search/?keyword=%E5%AD%99%E5%85%81%E7%8F%A0'
    }

    while(offset<=100):
        query_data = {
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
            'format': 'json',
            'keyword': '刘德华',
            'offset': offset
        }
        query_url = 'http://www.toutiao.com/search_content/?' + \
            _get_query_string(query_data)
        article_req = urllib.request.Request(query_url, headers=request_headers)
        [article_titles, article_urls] = get_article_titles_urls(article_req)
        for i in range(len(article_titles)):
            if article_titles[i] is not None and article_urls[i] is not '':
                save_dir = _create_dir(os.path.join(root_dir, article_titles[i]))
                print('创建文件夹 %s' % save_dir)
                get_images(save_dir, article_urls[i])
        offset=offset+20