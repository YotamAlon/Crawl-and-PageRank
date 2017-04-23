from scrapy.spiders import Spider
from scrapy.selector import Selector
from basic_crawler.items import BasicCrawlerItem
from scrapy.http import Request
import re
from pymongo import MongoClient

global db
db = MongoClient().db.links
if not db:
	print('Connected to DB')
res = db.delete_many({})
if res.acknowledged:
	print('Clean successfull')
else:
	print('Clean unsuccessfull')

global visited_links
visited_links=[]
class MySpider(Spider):
	name = "basic_crawler"
	allowed_domains = ['math.hmc.edu']
	start_urls = ["https://www.math.hmc.edu/funfacts/"]

	def parse(self, response):
		global db
		global visited_links
		hxs = Selector(response)
		url = response.url
		exist = db.find_one({'link':url})
		if not exist:
			res = db.insert_one({'link':url, 'refs':[]})
			if not res.acknowledged:
				print('Initial insert unsuccesfull')
		
		print('Starting to process url: ' + url + '\n\n')

		links = hxs.xpath('//a/@href').extract()
		link_validator= re.compile("^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

		for toprocess in links:
			if '/funfacts' in toprocess:
			
				if link_validator.match(toprocess):
					link = toprocess
				else:
					link = response.urljoin(toprocess)
					
				if not link in visited_links:
					print('Processing link: ' + link)
					visited_links.append(link)
					dbentry = {'link':link, 'refs':[url]}
					res = db.insert_one(dbentry)
				
					if not res:
						print('Was not able to insert link: ' + link)
					yield Request(link, callback=self.parse)
					
				else:
					dbentry = db.find_one({'link':link})
					if dbentry:
						refs = list(set(dbentry['refs'] + [url]))
						db.update_one({'link':link}, {'$set':{'refs':refs}})
					else:
						print('Was not able to find visited entry: ' + link)
