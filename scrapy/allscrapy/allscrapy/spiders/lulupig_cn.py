import scrapy
from allscrapy.items import AllscrapyItem
import datetime
from scrapy import FormRequest

class NynewsSpider(scrapy.Spider):
    
    name = "lulupig_cn"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["http://www.lulupig.cn/?cat=8"]
    
    def parse(self, response):
        
        category_url = response.xpath("//div[@id='site-nav-wrap']//div[@class='menu-%e9%a1%b6%e9%83%a8%e8%8f%9c%e5%8d%95-container']//a/@href").getall()
        i = 0
        while i < len(category_url):
            if i != 6:
                # print(category_url[i])
                yield scrapy.Request(f'{category_url[i]}', callback=self.parse_article_urls)
            i+=1
            
        
        
    def parse_article_urls(self, response):
        
        next_page = response.xpath("//div[@class='nav-links']/a[@class='next page-numbers']/@href").getall()
        article_urls = response.xpath("//div[@class='site-content']//article//h2/a/@href").getall()
        for article_url in article_urls:
            yield scrapy.Request(article_url, callback=self.parse_article_contents)
        if next_page != []:   
            yield scrapy.Request(next_page, callback=self.parse_article_urls)
        
    def parse_article_contents(self, response):
        
        title = response.xpath("//h1[@class='entry-title']//text()").get()
        contents = response.xpath("//div[@class='single-content']//img/@src|//div[@class='single-content']//text()").getall()
        category = response.xpath("//div[@class='single-cat']/a/text()").get()
        print(f'==============={category}==={title}==================\n{response.url}')
        _contents = []
        for content in contents:
            content = content.strip()
            if content != '':
                _contents.append(content)
                print(content)
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = category
        item["content"] = _contents
        # item['time_decline'] = datetime.datetime.utcnow()
        yield item