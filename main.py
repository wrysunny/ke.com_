#!/usr/bin/env python3
#!-*- coding:utf-8 -*-
import requests
import sqlite3
from lxml import etree


_author_ = 'Wrysunny'
_info_ = '贝壳 爬虫 demo'

addr_url = '.fang.ke.com/loupan/pg' # pg{1-33}
user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
citylist = [['changzhou',33],['wx',65],['xz',34],['yc',20],['yixing',13],['dongtai',7]] # 常州、无锡、徐州、盐城、宜兴、东台


def get_page(city,page_id):
	num = 0
	print('*'*25 + city + '*'*25)
	for i in range(1,page_id+1,1): # 33 page
		page_url = 'https://' + city + addr_url + '%s'%str(i)
		result = requests.get(url=page_url,headers=user_agent,timeout=10).content
		selector = etree.HTML(result)
		for i_d in range(1,11,1):
			num += 1
			names = selector.xpath(f'/html[1]/body[1]/div[5]/ul[2]/li[{i_d}]/div/div[1]/a/text()')
			names = ''.join(names).encode('raw_unicode_escape').decode('unicode_escape')
			status = selector.xpath(f'/html[1]/body[1]/div[5]/ul[2]/li[{i_d}]/div[1]/div[1]/span[1]/text()')
			status = ''.join(status).encode('raw_unicode_escape').decode('unicode_escape')
			types = selector.xpath(f'/html[1]/body[1]/div[5]/ul[2]/li[{i_d}]/div/div[1]/span[2]/text()')
			types = ''.join(types).encode('raw_unicode_escape').decode('unicode_escape')
			address = selector.xpath(f'/html[1]/body[1]/div[5]/ul[2]/li[{i_d}]/div/a[1]/text()')
			address = ''.join(address).encode('raw_unicode_escape').decode('unicode_escape')
			address = address.strip()
			infos = []
			for x in range(1,5,1):
				info = selector.xpath(f'/html[1]/body[1]/div[5]/ul[2]/li[{i_d}]/div/a[2]/span[{x}]/text()')
				info = ''.join(info).encode('raw_unicode_escape').decode('unicode_escape')
				infos.append(info)
			infos = ''.join(infos)
			per = selector.xpath(f'/html[1]/body[1]/div[5]/ul[2]/li[{i_d}]/div/div[4]/div/span/text()')
			per = ''.join(per).encode('raw_unicode_escape').decode('unicode_escape')
			print(f'第{i}页: 第{i_d}个 ') # 名称：{names} 状态：{status} 类型：{types} 地址：{address} 信息：{infos} 价格:{per}')
			with open(f'./{city}_info.txt','a+',encoding='utf-8') as f:
				f.write(f"{num}|{names}|{status}|{types}|{address}|{infos}|{per}\n")
			#print(f'{num}|{names}|{status}|{types}|{address}|{infos}|{per}')
	print(f'总共{num}个结果.')

if __name__ == '__main__':
	for y in range(len(citylist)):
		city = citylist[y][0]
		page_id = citylist[y][1]
		#print(city,page_id)
		get_page(city,page_id)
