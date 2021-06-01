# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymongo
from scrapy.utils.project import get_project_settings

class FfmpegLibavUserPipeline:
    def process_item(self, item, spider):
        return item

class threadPipeline:
    def __init__(self):
        settings = get_project_settings()

        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        dbname = settings["MONGODB_DBNAME"]
        collectionname= settings["MONGODB_COLLECTIONNAME"]

        client = pymongo.MongoClient(host = host, port = port,username='admin', password='123456')
        mydb = client[dbname]
        self.collection = mydb[collectionname]

    def process_item(self, item, spider):

        self.collection.insert(dict(item))
        return item
