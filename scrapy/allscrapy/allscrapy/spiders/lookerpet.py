import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "lookerpets_net"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["http://www.lookerpets.net/category_269.html"]
    
    def parse(self, response):
        
        categorys = response.xpath("//nav[@class='nav']/ul[@class='list']/li/a/text()").getall()[1:]
        category_urls = response.xpath("//nav[@class='nav']/ul[@class='list']/li/a/@href").getall()[1:]
        i = 0
        while i < len(categorys):
            yield scrapy.Request(f'http://www.lookerpets.net{category_urls[i]}', callback=self.parse_article_urls, meta={"category" : categorys[i]})
            i += 1
    
            
    def parse_article_urls(self, response):
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        article_urls = response.xpath("//ul[@class='ui_list']/li//a/@href").getall()
        for article_url in article_urls:
            yield scrapy.Request(f'http://www.lookerpets.net{article_url}', callback=self.parse_article_contents, meta={"category" : response.meta['category']})
        if not next_page == None:
            yield scrapy.Request(f'http://www.lookerpets.net{next_page}', callback=self.parse_article_urls, meta={"category" : response.meta['category']})
            
    def parse_article_contents(self, response):
        
        title = response.xpath("//h1[@class='title']/text()").get().strip()
        contents = response.xpath("//div[@class='detail_content']/p/text()|//div[@class='detail_content']//img/@src").getall()
        
        print(f'=================={title}==================\n{response.url}\n{contents}')
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = response.meta['category']
        item["content"] = contents
        item['time_decline'] = datetime.datetime.utcnow()
        yield item

    
    
