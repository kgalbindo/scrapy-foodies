# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodItem(scrapy.Item):
    article_id = scrapy.Field()
    article_title = scrapy.Field()
    article_link = scrapy.Field()
    article_tag = scrapy.Field()
    article_date = scrapy.Field()
    article_writer = scrapy.Field()
    
    scraped_date = scrapy.Field()
    venue_name = scrapy.Field()
    review_score = scrapy.Field()
    review_pros = scrapy.Field()
    review_cons = scrapy.Field()

    recommended_dish = scrapy.Field()
    opening_hours = scrapy.Field()
    address = scrapy.Field()
    source = scrapy.Field()