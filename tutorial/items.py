# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    
    # name = scrapy.Field()
    Title = scrapy.Field()
    Classify = scrapy.Field()
    ReceivedTime = scrapy.Field()
    AcceptTime = scrapy.Field()
    referencesNumber = scrapy.Field()
    funderBy = scrapy.Field()
    AutorNumber = scrapy.Field()
    Country = scrapy.Field()
    University = scrapy.Field()
    Institute = scrapy.Field()
    