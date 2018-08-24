# -*- coding: utf-8 -*-
import scrapy
from nbxts.items import NbxtsItem


class NbxtsspiderSpider(scrapy.Spider):
    name = 'nbxtsSpider'
    allowed_domains = ['www.nbxts.com']
    start_urls = ['http://www.nbxts.com/art-type-id-9-pg-1.html/']

    for image_id in range(9,15):
        for image_page in range(1,60):
            url = 'http://www.nbxts.com/art-type-id-'+str(image_id)+'-pg-'+str(image_page)+'.html'
            start_urls.append(url)
    print(start_urls)

    def parse(self, response):
        imagenames = response.css('.box.list.channel a::text').extract()
        imageurls = response.css('.box.list.channel a::attr(href)').extract()
        for i in range(0,len(imagenames)):
            url = 'http://www.nbxts.com'+imageurls[i]
            print(imagenames[i]+url)
            yield scrapy.Request(url=url,callback=self.parse_image)
    
    def parse_image(self,response):
        item = NbxtsItem()
        image_name = response.css('.cat_pos_l a::text').extract()
        image_urls = response.css('.content img::attr(src)').extract()
        for image_url in image_urls:
            item['image_urls'] = [image_url]
            item['image_name'] = image_name[1]+'/'+image_name[2]
            item['url'] = response.url
            print(item['image_urls'][0]+item['image_name'])
            yield item