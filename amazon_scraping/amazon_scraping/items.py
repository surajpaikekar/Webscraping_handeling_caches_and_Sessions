# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


## items to srape from amazon.com website ==>> title, author, price and image link
class AmazonScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    product_title = scrapy.Field()
    product_author = scrapy.Field()
    product_price = scrapy.Field()
    product_imageLink = scrapy.Field()
    
