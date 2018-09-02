# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode, quote_plus

from ..items import ApeItem

class A51apeSpider(scrapy.Spider):
    name = '51ape'
    allowed_domains = ['51ape.com']
    start_urls = ['http://www.51ape.com/artist/']

    def parse(self, response):
        '''
            获取所有音乐家
        '''
        
        categories = response.xpath('//div[contains(@class, "w610")]')
        for category in categories:
            authors = category.xpath('.//div[contains(@class, "gs_a")]/a/text()').extract()
            
            for author in authors:
                query_url = 'http://www.51ape.com/skin/ape/php/qx_2.php?' + urlencode({'qx': author})
                yield scrapy.Request(query_url,  self.parse_music)
    
    def parse_music(self, response):
        '''
            获取所有音乐家的音乐
        '''
        music_list = response.xpath('//div[contains(@class, "w260")]//a/@href').extract()
        for muisc in music_list:
            yield scrapy.Request(muisc, self.parse_music_detail)

    def parse_music_detail(self, response):
        title = response.xpath('//h1[contains(@class, "f_32")]/text()').extract_first()  #'阿宝 - 你身边的人曾经是我.wav' 
        info= response.xpath('//h3[contains(@class, "c999") and contains(@class, "f_12")]/text()').extract() # ['选自专辑《你身边的人曾经是我》', '1411Kbps', '46.3M', '国语', '2015-05-30']
        download_url = response.xpath('//a[contains(@class, "a_none")]/@href').extract_first() # 'http://pan.baidu.com/s/1sjOELEP'
        download_password = response.xpath('//b[contains(@class, "d_b")]/text()[2]').extract_first() # '密码：q6ac'

        item = ApeItem(title=title, info=info, download_url=download_url, download_password=download_password)
        yield item

