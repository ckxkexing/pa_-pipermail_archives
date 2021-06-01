import scrapy
import json
import random
from fake_useragent import UserAgent

from ffmpeg_libav_user.items import ffmpeg_boxItem
import pymongo

# 这是第二步，获取每个年月的话题组合情况
# 需要在settings.py中设置‘目的集合’ 一般为 ‘_box’
# scrapy crawl ffmpeg_box


class Ffmpeg1Spider(scrapy.Spider):
    name = 'ffmpeg_box'
    allowed_domains = ['http://ffmpeg.org']
    ua = UserAgent()
    cur_page = 1
    begin_url = 'http://ffmpeg.org/pipermail/libav-user/'

    def start_requests(self):
        client = pymongo.MongoClient("mongodb://admin:123456@127.0.0.1",27017)
        db = client["mailing_lists"]
        col = db["ffmpeg_libav_user_thread"]

        for item in col.find():
            yield scrapy.Request(item["url"], callback = self.parse_box_content, headers = {
                    "User-Agent" :  self.ua.random,
                    'Accept-Language': 'en',
                    })

    def parse_box_content(self, response):
        mid = response.url.split('/')[-2]
        # fix bug
        # xpath 可以获取 直接子节点<li>。而如果用css，获取的是全部子节点<li>

        for u in response.css('ul')[1].xpath('li'):
            item = ffmpeg_boxItem()
            item["urls"] = []
            for url in u.css('a::attr(href)').extract():
                item["urls"].append(self.begin_url +mid+'/'+ url)
            yield item   
