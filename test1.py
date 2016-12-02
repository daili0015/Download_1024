#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests ##导入requests
import re
import os
import time
from bs4 import BeautifulSoup
from zcy_fun import get_format_filename
from zcy_fun import get_inner_link
from zcy_fun import Process_SubPage

file_path='D:\MyProjectFile\Python\studyproject\Python3\StudyPro1\datebase'#存储的地址
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
           }#初始使用的header
URL_1024='github已自动隐藏该信息'#网站地址中‘日本骑兵’系列，别的系列我没有测试，不保证正确 #刚测试了，‘亚洲无码’也可以，估计所有系列的网页HTML格式是一样的
                                    

start_html = requests.get(URL_1024,  headers=headers)
start_html.encoding='utf-8'
bsObj = BeautifulSoup(start_html.text,'html.parser')
for a in bsObj.find("tbody", {"style":"table-layout:fixed;"}).findAll("a"):
    if ('href' in a.attrs) and ('title' not in a.attrs ) :
        if re.match(r'^htm_data/.+.html', a.attrs['href']):
            a_path = get_format_filename(a.text)
            if not os.path.exists(os.path.join(file_path, a_path)):
                os.makedirs(os.path.join(file_path, a_path))
            os.chdir(file_path+'\\'+a_path)#切换到上面创建的文件夹
            f = open(a_path+'.txt', 'w')# r只读，w可写，a追加
            f.write(get_inner_link(a.attrs['href']))
            f.close()
            Process_SubPage(file_path+'\\'+a_path, a.attrs['href'])#处理子页面，包括下载图片，种子
            print(get_inner_link(a.attrs['href']))
            print(a_path+'：处理完毕')
            # time.sleep(0.5)#设置等待还是会被服务器封禁
