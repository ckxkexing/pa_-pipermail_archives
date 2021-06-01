# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class FfmpegLibavUserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ffmpeg_threadItem(scrapy.Item):
    url = scrapy.Field()


class ffmpeg_boxItem(scrapy.Item):
    urls = scrapy.Field()

class ffmpeg_contentItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    date = scrapy.Field()
    subject = scrapy.Field()
    content = scrapy.Field()