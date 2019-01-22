# -*- coding: utf-8 -*-
import scrapy
import re
import json
import os
import sys
from scrapy.spiders import Rule, CrawlSpider
from bellascraper.items import ProductItem, CustomerItem, ReviewItem


class SephoraSpider(scrapy.Spider):
    name = 'sephora'
    allowed_domains = ['sephora.com', 'api.bazaarvoice.com']
    
    
    #currently only extract fixed category
    start_urls = ["https://www.sephora.com/shop/face-serum"]
    
    def __init__(self):
        self._p_keys = ['p_ID', 'p_Name', 'p_Brand', 'p_link', 'p_price', 
                        'p_category', 'p_image', 'p_stars', 'p_nReviews',
                        'p_description']
        self._c_keys = ['c_name', 'c_eyecolor', 'c_haircolor', 'c_skintone', 
                        'c_skintype', 'c_skinconcerns', 'c_age']
        self._r_keys = ['r_star', 'r_text', 'r_title', 'r_time', 'r_product', 
                        'r_reviewer']

    def parse(self, response):
        """Extract number of products under current category and get number of 
        pages.
        product_per_page:sephora only allows scraping the first 12 products
        on one page.
        """
        category = 'face-serum'
        product_per_page = 60
        n_product = response.xpath(
                '//span[@data-at="number_of_products"]/text()').extract_first()
        n_product = int(re.findall(r'\d+', n_product)[0])
        n_page = n_product // product_per_page + int(n_product % product_per_page != 0)
        for p in range(1, n_page+1):
            page_link = 'https://www.sephora.com/shop/%s?pageSize=%d&'\
                        'currentPage=%d' % (category, product_per_page, p)
            sys.stdout.write('Products on page %s \n' % p)
            yield scrapy.Request(url=page_link, 
                                 callback=self.parse_category_pages)
            
    def parse_category_pages(self, response):
        """Extract product info and links to all products on one page.
        """
        #scrapy item keys
        data = response.xpath('//script[@type="application/ld+json"]')[1].extract()
        products = re.findall('>\[(.*)\]<', data)[0].split('},{')
        #links = re.findall('"url":"(https://\S+-P\d+)"', products)
        #prices = re.findall('"price":"(\S+)","availability"', products)
       # brands = re.findall('"brand":"(\S+)","url":', products)
        #names = re.findall('"Product","name":"([^"]+)","category"', products)
        #skus = re.findall('sku":"(\d+)"},', products)
        #categories = re.findall('"category":"([^"]+)","@context"' ,products)
        #images_url = 'https://www.sephora.com/productimages/sku/'\
        #              's%s-main-grid.jpg' % sku
        
        #links = response.xpath(
        #          '//div[@class="css-12egk0t"]/a[@class="css-ix8km1"]/@href'
        #          ).extract() 
        limit = 1
        for i, p in enumerate(products):
            if i == 0:
                p += '}'
            elif i == (len(products) - 1):
                p = '{' + p
            else:
                p = '{' + p + '}'
            jsonp = json.loads(p)
            link =  jsonp['url']
            ID = re.findall("https://\S+-(P\d+)", link)[0]
            try:
                price = jsonp['offers']['price']
            except:
                price = jsonp['offers']['lowPrice']
            brand = jsonp['brand']
            name = jsonp['name']
            image = jsonp['image']
            category = jsonp['category']
            values = [ID, name, brand, link, price, category, image, None, None] 
            sys.stdout.write(link)
            f = open('./data/product_list.tsv', 'a')
            f.write('%s\n' % ID)
            f.close()
            p_item = ProductItem()
            for k, v in zip(self._p_keys, values):
                p_item[k] = v 
            #review_link = 'http://reviews.sephora.com/8723abredes/P429201/'\
            #'reviews.htm?format=embedded'
            review_link = 'https://api.bazaarvoice.com/data/reviews.json?'\
            'Filter=ProductId%%3A%s&Sort=Helpfulness%%3Adesc&Limit=%s&'\
            'Offset=%s&Include=Products%%2CComments&Stats=Reviews&'\
            'passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4' % (ID, limit, 0)
            yield scrapy.Request(url=review_link, 
                                 callback=self.parse_review_pages,
                                 meta=p_item)
            
                
        #for i, l in enumerate(links):
            #ID = re.findall("https://\S+-(P\d+)", l)[0]
           # sys.stdout.write(l)
           # f = open('./data/product_list.tsv', 'a')
           # f.write('%s\n' % ID)
           # f.close()
           # values = [ID, names[i], brands[i], l, prices[i], categories[i], 
           #           skus[i], None, None]
           # p_item = ProductItem()
           # for k, v in zip(self._p_keys, values):
           #     p_item[k] = v 
            

    def parse_review_pages(self, response):
        """Extract reviews, reviewer info from API.
        """
        data=json.loads(response.text)
        p_item = response.meta
        p_ID = p_item['p_ID']
        try:
            product_info = data['Includes']['Products'][p_ID]
            p_item['p_stars'] = product_info['ReviewStatistics']['AverageOverallRating']
            p_item['p_nReviews'] = product_info['TotalReviewCount']
            p_item['p_description'] = product_info['Description'] 
        except:
            p_item['p_stars'] = None
            p_item['p_nReviews'] = 0
            p_item['p_description'] = None
           
        if not os.path.isfile('./data/product.tsv'):
            f = open('./data/product.tsv', 'w+')
            f.write('\t'.join(self._p_keys) + '\n')
            f.close()
        p_row = ''
        for k in self._p_keys:
             if p_item[k] is None:
                p_row += 'NA\t'
             else:
                p_row += '%s\t' % p_item[k] 
        p_row = p_row.strip()    
        f = open('./data/product.tsv', 'a')
        f.write('%s\n' % p_row)
        f.close()
        
        limit = min(int(p_item['p_nReviews']), 100)
        n_offset = p_item['p_nReviews'] // 100 + int(p_item['p_nReviews'] % 100 != 0)
        sys.stdout.write('%s reviews for product %s \n' % (p_item['p_nReviews'], 
                                                           p_ID))
        for i in range(n_offset):
            review_page = 'https://api.bazaarvoice.com/data/reviews.json?'\
            'Filter=ProductId%%3A%s&Sort=Helpfulness%%3Adesc&Limit=%s&'\
            'Offset=%s&Include=Products%%2CComments&Stats=Reviews&'\
            'passkey=rwbw526r2e7spptqd2qzbkp7&apiversion=5.4' % (p_ID, limit, i)
            
            sys.stdout.write('Reviews on page %s for product %s \n' % (i, p_ID))
            yield scrapy.Request(url=review_page, 
                                 callback=self.parse_review_details)
                   
    def parse_review_details(self, response):
        """Parse reviews on each page.
        """
        data = json.loads(response.text)
        reviews = data['Results']
        if not os.path.isfile('./data/customer.tsv'):
            f = open('./data/customer.tsv', 'w+')
            f.write('\t'.join(self._c_keys) + '\n')
            f.close()
            
        if not os.path.isfile('./data/review.tsv'):
            f = open('./data/review.tsv', 'w+')
            f.write('\t'.join(self._r_keys) + '\n')
            f.close()
        i = 0
        for review in reviews:
            #sys.stdout.write('Review no.%s \n' % i)
            try:
                c_name = review['UserNickname']
            except:
                c_name = None   
            try:
                c_eyecolor = review['ContextDataValues']['eyeColor']['Value']
            except:
                c_eyecolor = None
            try:
                c_haircolor = review['ContextDataValues']['hairColor']['Value']
            except:
                c_haircolor = None
            try:
                c_skintone = review['ContextDataValues']['skinTone']['Value']
            except:
                c_skintone = None
            try:
                c_skintype = review['ContextDataValues']['skinType']['Value']
            except:
                c_skintype = None
            try:
                c_skinconcerns = review['ContextDataValues']['skinConcerns']['Value']
            except:
                c_skinconcerns = None
            try:
                c_age = review['ContextDataValues']['age']['Value']
            except:
                c_age = None
            c_item = CustomerItem()
            c_values = [c_name, c_eyecolor, c_haircolor, c_skintone, c_skintype, 
                        c_skinconcerns, c_age]
            c_row = ''
            for k,v in zip(self._c_keys, c_values):
                c_item[k] = v
            c_row = '\t'.join(['NA' if v is None else str(v) for v in c_values])
            f = open('./data/customer.tsv', 'a')
            f.write('%s\n' % c_row)
            f.close()
            
            try:
                r_star = review['Rating']
            except:
                r_star = None
            try:
                text = review['ReviewText']
                text = text.replace('\t', ' ').replace('\n', ' ')
                r_text = text.replace('\r', ' ').replace('"', '').strip()
            except:
                r_text = None
            try:
                text = review['Title']
                text = text.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ').strip()
                r_title = text
            except:
                r_title = None
            try:
                r_time = review['LastModeratedTime']
            except:
                r_time = None
            try:
                r_product = review['ProductId']
            except:
                r_product = None
            r_item = ReviewItem()    
            r_values = [r_star, r_text, r_title, r_time, r_product, c_name]
            for k,v in zip(self._r_keys, r_values):
                r_item[k] = v
            r_row = '\t'.join(['NA' if v is None else str(v) for v in r_values])
            f = open('./data/review.tsv', 'a')
            f.write('%s\n' % r_row)
            f.close()
            
            i += 1
            yield