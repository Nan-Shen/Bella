# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_ID = scrapy.Field()
    p_Name = scrapy.Field()
    p_Brand = scrapy.Field()
    p_link = scrapy.Field()
    p_price = scrapy.Field()
    p_stars = scrapy.Field()
    p_nReviews = scrapy.Field()
    p_category = scrapy.Field()
    p_image = scrapy.Field()
    p_description = scrapy.Field()

class CustomerItem(scrapy.Item):
    c_name = scrapy.Field() 
    c_eyecolor = scrapy.Field() 
    c_haircolor = scrapy.Field() 
    c_skintone = scrapy.Field() 
    c_skintype = scrapy.Field() 
    c_skinconcerns = scrapy.Field() 
    c_age = scrapy.Field() 
    
class ReviewItem(scrapy.Item):
    r_star = scrapy.Field() 
    r_text = scrapy.Field() 
    r_title = scrapy.Field() 
    r_time = scrapy.Field() 
    r_product = scrapy.Field() 
    r_reviewer = scrapy.Field() 
    