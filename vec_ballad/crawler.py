import scrapy
import os
import json
import requests
import re
import os
from scrapy.crawler import CrawlerProcess

class NetEaseSongListSpider(scrapy.Spider):

	name = "netease_song_list_spider"

	def __init__(self, root):
		self.root = root
		self.file = open(os.path.join(self.root, 'config/song_list.json'), 'w', encoding='utf-8');
		self.singers = []
		self.urls = []
		with open(os.path.join(self.root, 'config/singers.txt'), 'r') as f:
			for s in f.readlines():
				self.singers.append(s.strip())
		for singer in self.singers:
			self.urls.append('https://music.163.com/artist?id='+singer)

	def start_requests(self):
		for url in self.urls:
			print("crawling url: {}".format(url))
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		#提取歌单列表
		response = response.css("div.f-cb")[0].css("textarea::text").extract_first()
		dicts = json.loads(response)
		song_list = {}
		song_list['artist'] = dicts[0]['artists'][0]['name']
		song_list['id'] = dicts[0]['artists'][0]['id']
		song_list['song'] = {'name':[], 'id':[]}
		for element in dicts:
			song_list['song']['name'].append(element['name'])
			song_list['song']['id'].append(element['id'])
		json.dump(song_list, self.file)
		self.file.write('\n')
		#及时将内容写入文件，否则可能会出现少许延迟
		self.file.flush()
		os.fsync(self.file)

	def __del__(self):
		self.file.close()

class NetEaseLyricsSpider(object):

	def __init__(self, root):
		self.data = []
		self.singers = []
		self.songs = []
		self.urls = []
		self.root = root
		with open(os.path.join(self.root, 'config/song_list.json'), 'r', encoding='utf-8') as f:
			for line in f.readlines():
				self.data.append(json.loads(line))

	def get_requests(self):
		if not os.path.isdir(os.path.join(self.root, 'songs')):
			os.mkdir(os.path.join(self.root, 'songs'))
		for d in self.data:
			if not os.path.isdir(os.path.join(self.root, 'songs/{}'.format(d['artist']))):
				os.mkdir(os.path.join(self.root, 'songs/{}'.format(d['artist'])))
			for s, i in zip(d['song']['name'], d['song']['id']):
				print('crawling {}: {}'.format(d['artist'], s))
				filename = os.path.join(self.root, 'songs/{}/{}.txt'.format(d['artist'], s.replace('/','\\')))
				url = 'http://music.163.com/api/song/lyric?id='+str(i) + '&lv=1&kv=1&tv=-1'
				yield requests.get(url).text, filename

	def parse(self):
		for r, filename in self.get_requests():
			lyric = json.loads(r)
			try:
				lrc = lyric['lrc']['lyric']
				pat = re.compile(r'\[.*\]|\(.*?\)|\（.*?\）')
				lrc = re.sub(pat,"",lrc)
				pat = re.compile(r'(.*)(：|:)(.*\n)')
				lrc = re.sub(pat,"\n",lrc)
				pat = re.compile('[^\u4e00-\u9fa5^\n^ ]')
				lrc = re.sub(pat,"",lrc)
				pat = re.compile(r' {2,}')
				lrc = re.sub(pat,"",lrc)
				pat = re.compile(r'(\n){2,}')
				lrc = re.sub(pat,"\n",lrc)
				lrc = lrc.strip()
				if lrc != '':
					with open (filename, 'w', encoding='utf-8') as f:
						f.write(lrc)
			except KeyError as e:
				pass


if __name__ == '__main__':
	process = CrawlerProcess({
	    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	})
	process.crawl(NetEaseSongListSpider(root='../'))
	process.start()

	spider = NetEaseLyricsSpider(root='../')
	spider.parse() 