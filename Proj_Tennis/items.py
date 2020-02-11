# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjTennisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    f_name = scrapy.Field()
    l_name = scrapy.Field()
    age = scrapy.Field()
    yr_pro = scrapy.Field()
    wt = scrapy.Field()
    ht = scrapy.Field()
    birthplace = scrapy.Field()
    rank_2020 = scrapy.Field()
    rank_career = scrapy.Field()
    win_career = scrapy.Field()
    loss_career = scrapy.Field()
    titles_career = scrapy.Field()
    prize_career = scrapy.Field()
