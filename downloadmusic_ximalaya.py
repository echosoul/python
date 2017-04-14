#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

'''
下载喜马拉雅专辑页的所有歌曲。by 2017-4-12
'''

from bs4 import BeautifulSoup
import os
import json
import urllib.request

if __name__ == '__main__':
    album_url = 'http://www.ximalaya.com/15794559/album/289315'  # 薛之谦
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
    }
    req = urllib.request.Request(album_url, headers=header)
    res = urllib.request.urlopen(req)
    soup = BeautifulSoup(res.read().decode('utf-8'), 'lxml')
    sounds = soup.findAll('a', {'class': 'title', 'href': True})

    album = album_url.split(r'/')[-1]
    path = os.path.join(r'C:\ximalaya', album)
    if not os.path.exists(path):
        os.mkdir(path)

    print('start download album %s' % album)
    for s in sounds:
        referer = 'http://www.ximalaya.com' + s.attrs['href']
        header_s = {
            'Referer': referer,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        }
        song_json_url = 'http://www.ximalaya.com/tracks/' + \
            s.attrs['href'].split(r'/')[-1] + r'.json'
        song_req = urllib.request.Request(song_json_url, headers=header_s)
        song_res = urllib.request.urlopen(song_req)
        song_json = json.loads(song_res.read())
        song_url = song_json['play_path']
        song_title = song_json['title']
        print(song_title + ' downloading...')
        urllib.request.urlretrieve(
            song_url, os.path.join(path, song_title + r'.mp3'))
        print(song_title + ' downloaded')
    print('album %s downloaded' % album)
