#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests ##导入requests
import re
import random
import time
from bs4 import BeautifulSoup

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
           }
UserAgent_List = [
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
	"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
	"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
	"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
	"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
URL_IP='http://www.youdaili.net/Daili/http/19733.html'#获取IP的网站
URL_test='https://www.baidu.com/'#测试IP是否可用的的网站
num_IP=10#准备采集多少个IP备用
IP_test_timeout=1#测试IP时超过多少秒不响应就舍弃了
count_time=3#下载图片失败时，最多使用几次代理

def IP_Test(IP,URL_test,set_timeout=IP_test_timeout):#测试IP地址是否可用,时间为3秒
	try:
		requests.get(URL_test, headers=headers, proxies={'http': IP[0] }, timeout=set_timeout)
		return True
	except:
		return False
def get_IPlist(URL,test_URl='http://t3.9laik.live/pw/'):#获取可用的IP地址
	IP_list=[]
	start_html = requests.get(URL, headers=headers)
	start_html.encoding = 'utf-8'
	bsObj = BeautifulSoup(start_html.text, 'html.parser')
	for span in bsObj.find("div", {"class": "content"}).findAll("span"):
		span_IP=re.findall(r'\d+.\d+.\d+.\d+:\d+', span.text)
		if IP_Test(span_IP,test_URl):#测试通过
			IP_list.append(span_IP)
			print('测试通过，IP地址为'+str(span_IP))
			if len(IP_list)>num_IP-1: #搜集够N个IP地址就行了
				print('搜集到'+str(len(IP_list))+'个合格的IP地址')
				return IP_list
	return IP_list

IP_list=get_IPlist(URL_IP)
def get_random_IP():#随机获取一个IP
	ind = random.randint(0, len(IP_list)-1)
	return IP_list[ind][0]

def get_image_header():#获取随机的header
	return {'User-Agent': random.choice(UserAgent_List),
             'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             # 'Host': 'pics.dmm.co.jp',
             'Cache-Control': 'no-cache',
             'Upgrade-Insecure-Requests': '1',
             # 'Referer': 'http://f3.1024xv.com/pw/htm_data/22/1611/486610.html'
             }

def download_single_image(image_url,proxy_flag=False,try_time=0):#首先尝试直接下载，一次不成功则尝试使用代理
	if not proxy_flag:#不使用代理
		try:
			image_html = requests.get(image_url, headers=get_image_header(), timeout=20)
			print('图片直接下载成功')
			time.sleep(3)
			return image_html #一次就成功下载！
		except:
			return download_single_image(image_url, proxy_flag=True)#否则调用自己，使用3次IP代理
	else:#使用代理时
		if try_time<count_time:
			try:
				print('尝试第'+str(try_time+1)+'次使用代理下载')
				# IP_address=get_random_IP()[0]
				image_html = requests.get(image_url, headers=get_image_header(), proxies={'http': get_random_IP()},timeout=20)
				print('状态码为'+str(image_html.status_code))
				if image_html.status_code==200:
					print('图片通过IP代理处理成功！')
					return image_html  # 代理成功下载！
				else:
					image_html = download_single_image(image_url, proxy_flag=True, try_time=(try_time + 1))
					return image_html
			except:
				print('IP代理下载失败')
				image_html = download_single_image(image_url, proxy_flag=True, try_time=(try_time+1))  # 否则调用自己，使用3次IP代理
				return image_html
		else:
			print('图片未能下载')
			return None