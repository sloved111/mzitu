# -*- encoding:utf-8 -*-
import os
import time
import requests
from bs4 import BeautifulSoup

class Mzitu(object):

	def first_url(self,url):
		exists = os.path.exists('F:/mzitu/xinggan')
		if exists:
			os.chdir('F:/mzitu/xinggan')
		else:
			os.makedirs('F:/mzitu/xinggan')
			os.chdir('F:/mzitu/xinggan')
		for s in list(range(1,18)):
			all_url = url +'/'+str(s) #拼接URL
			res = self.request(all_url)
			soup = BeautifulSoup(res.text,'lxml').find('ul',id="pins").select('li > a')
			for title in soup:
				href = title['href'] #每一页的套图地址
				# print(href) #测试时使用
				self.maxpage(href)

	def maxpage(self,href): #具体套图
		res = self.request(href)
		soup = BeautifulSoup(res.text,'lxml')
		max_page = soup.find('div', class_='pagenavi').find_all('span')[-2].get_text() #获取套图最后一页
		for page in list(range(1, int(max_page) + 1)):
			page_url = href + '/' + str(page) # 套图的每一页url
			# print(page_url) #测试时使用
			self.img(page_url)

	def img(self,page_url):
		res = self.request(page_url)
		img_url = BeautifulSoup(res.text, 'lxml')
		content = img_url.find('div', class_='main-image').find('img')['src'] #图片
		name = content[-9:-4]
		# print (name,content) #测试时用
		self.save_img(content,name)

	def save_img(self,content,name): #保存图片到本地
		res = self.request(content)
		with open(name+'.jpg','ab') as f:
			f.write(res.content)
			print ('保存成功')
			time.sleep(0.1)

	def request(self,url):
		headers = {'user-agent':'Mozilla/5.0'}
		content = requests.get(url,headers=headers)
		return content

m = Mzitu()
m.first_url('http://www.mzitu.com/xinggan')		