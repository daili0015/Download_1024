#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from proxytest import download_single_image
import requests
import re
import os
import time

web_domain = 'http://r3.gcsitl.website/pw/'#这一部分加上子页面的href就是子页面的网址
headers = {
	'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
	'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	'Accept-Encoding': 'gzip',
	}

def get_format_filename(input_filename): #文件夹的名字不能含有的特殊符号，windows下的限定
	for s in ['?', '*', '<', '>', '\★', '！']:
		while s in input_filename:
			input_filename = input_filename.strip().replace(s, '')
	return input_filename

def get_inner_link(URL_part2, URL_part1=web_domain):  # 返回子页面的URL
	return URL_part1 + URL_part2

def Process_SubPage(save_path, img_url):
	start_html = requests.get(get_inner_link(img_url), headers=headers)#只要不是访问图片，一般都不会被封禁，不用换header和IP
	start_html.encoding = 'utf-8'
	bsObj = BeautifulSoup(start_html.text, 'html.parser')
	print('子页面读取完毕，开始尝试处理图片')
	img_ind = 1  # 下标
	for a_img in bsObj.find("div", {"id": "read_tpc"}).findAll("img"):#处理图片
		if ('src' in a_img.attrs):
			print('图片URL为' + a_img.attrs['src'])
			image = download_single_image(a_img.attrs['src'])
			time.sleep(0.3)#停止

			if image and len(image.content)>20000:  # 如果不是为空，则说明下载到了,另外图片如果太小，说明图片数据错误（全黑的），一般都是网站上这个图确实没数据
				os.chdir(save_path)
				f = open(str(img_ind) + '.jpg', 'ab')
				print('下载得到图片！保存图片'+str(img_ind)+'大小为'+str(len(image.content)))
				f.write(image.content)
				f.close()
			img_ind += 1
