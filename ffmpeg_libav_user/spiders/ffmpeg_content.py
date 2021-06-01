import scrapy
import json
import random
from fake_useragent import UserAgent

from ffmpeg_libav_user.items import ffmpeg_contentItem
import pymongo

# 这是第三步，获取每个话题的具体信息
# 获取完成后，就可以结合box信息用gao.py产生要求的topic+reply结构
# 需要在settings.py中设置‘目的集合’ 一般为‘_content’
# scrapy crawl ffmpeg_content

class Ffmpeg1Spider(scrapy.Spider):
    name = 'ffmpeg_content'
    allowed_domains = ['http://ffmpeg.org']
    ua = UserAgent()
    cur_page = 1
    begin_url = 'http://ffmpeg.org/pipermail/libav-user/'

    def start_requests(self):
        client = pymongo.MongoClient("mongodb://admin:123456@127.0.0.1",27017)
        db = client["mailing_lists"]
        col = db["ffmpeg_libav_user_box"]
        
        for item in col.find():
            for url in item["urls"]:
                yield scrapy.Request(url, callback = self.parse_content, headers = {
                        "User-Agent" :  self.ua.random,
                        'Accept-Language': 'en',
                        })

    def parse_content(self, response):
        print("!" * 20)
        print(self.cur_page)
        self.cur_page += 1
        item = ffmpeg_contentItem()
        item["url"] = response.url
        item["name"] = response.css('body b::text')[0].extract()
        item["subject"] = response.css('body h1::text')[0].extract()
        item["date"] = response.css('body i::text')[0].extract()
        item["content"] =  response.css('body pre')[0].extract()
        item["email"] = response.css('body>a::text')[0].extract()
        yield item