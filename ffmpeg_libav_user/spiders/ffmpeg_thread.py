import scrapy
import json
import random
from fake_useragent import UserAgent

from ffmpeg_libav_user.items import ffmpeg_threadItem

# 这是第一步，获取每个年月的url
# 需要在settings.py中设置‘目的集合’ 一般为 ‘_thread’
# scrapy crawl ffmpeg_thread

class Ffmpeg1Spider(scrapy.Spider):
    name = 'ffmpeg_thread'
    allowed_domains = ['http://ffmpeg.org']
    ua = UserAgent()
    cur_page = 1
    begin_url = 'http://ffmpeg.org/pipermail/libav-user/'

    def start_requests(self):
        yield scrapy.Request(self.begin_url, callback = self.parse_url, headers = {
                    "User-Agent" :  self.ua.random,
                    'Accept-Language': 'en',
                    })

    def parse_url(self, response):
        print("*" * 20)
        for u in response.css('tr')[1:]:
            item = ffmpeg_threadItem()
            item['url'] = self.begin_url + u.css('td')[1].css('a::attr(href)').extract()[0]
            yield item
            # mail_link.append(begin_url+link)
        
