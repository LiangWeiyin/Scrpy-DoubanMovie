# -*- coding: utf-8 -*-
from ..items import DbScrapyItem
import scrapy
from bs4 import BeautifulSoup
import json
import re
import random
import string         
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={index}&genres=%E5%89%A7%E6%83%85'.format(index=i) for i in range(9420, 9961, 20)]

    def start_requests(self):
        for url in self.start_urls:
            bid = "".join(random.sample(string.ascii_letters + string.digits, 11))
            
            cookies = {
                'bid': bid,
            }
            yield scrapy.Request(url=url, cookies=cookies)

    def parse(self, response):
        data = json.loads(response.text)['data']
        for i in data:
            url = i['url']
            yield scrapy.Request(url=url, callback=self.getMovieData)
    
    def getMovieData(self, response):
        item = DbScrapyItem()
        soup = BeautifulSoup(response.text, 'lxml')

        big_title = soup.find_all(name='h1')[0]
        title = big_title.span.text
        year = big_title.find_all(attrs={'class': 'year'})[0].text.strip('()')

        temp = soup.find_all(name='div', attrs={'id':'info'})[0].text
        director = re.findall(r"导演:\s.+", temp)[0][4:].split('/')
        tags = re.findall(r"类型:\s.+", temp)[0][4:].split('/')
        try:
            actors = re.findall(r"主演:\s.+", temp)[0][4:].split('/')[:4] #取前四个演员
        except:
            actors = None
        try:
            country = re.findall(r"制片国家/地区:\s.+", temp)[0][9:].split('/')
        except:
            country = None

        temp_rating = soup.find_all(name='div', attrs={'class': 'rating_self clearfix', 'typeof': 'v:Rating'})[0].text
        _x = re.findall(r'[0-9|\.]+', temp_rating)
        rating = _x[0]
        rating_people = _x[1]


        try:
            summary = soup.find_all(name='span', attrs={'class': 'all hidden'})[0].text
            summary = re.sub(r'[\s]', '', summary)
        except:
            summary = soup.find_all(name='span', attrs={'property': 'v:summary'})[0].text
            summary = re.sub(r'[\s]', '', summary)
        
        item['title'] = title
        item['year'] = year
        item['director'] = director
        item['actors'] = actors
        item['tags'] = tags
        item['rating'] = rating
        item['rating_people'] = rating_people
        item['country'] = country
        item['summary'] = summary
        yield item