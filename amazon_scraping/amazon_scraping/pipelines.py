# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# After scraping the data from any website we might want to store these data in JSON, sql db, Mongodb etc
# So this pipelines.py file will make sure that these scrped data will handled properly and stored in any DB

class AmazonScrapingPipeline:
    def process_item(self, item, spider):
        return item
