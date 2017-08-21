from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import scrapy
from example.items import AppleItem

class AppleCrawler(CrawlSpider):
    name = 'apple'
    start_urls = ["http://www.appledaily.com.tw/realtimenews/section/new/"]
    rules = [
        Rule(LinkExtractor(allow=('/realtimenews/section/new/.*$')), callback='parse_list', follow=True)
    ]
    def parse_list(self,response):
        domain = 'http://www.appledaily.com.tw'
        res = BeautifulSoup(response.body)
        for news in res.select('.rtddt'):
            yield scrapy.Request(domain + news.select('a')[0]['href'], self.parse_detail)
    def parse_detail(self,response):
        res = BeautifulSoup(response.body)
        appleitem = AppleItem()
        appleitem['title'] = res.select('#h1')[0].text
        appleitem['content'] = res.select('.trans')[0].text
        appleitem['time'] = res.select('.gggs time')[0].text
        return appleitem
