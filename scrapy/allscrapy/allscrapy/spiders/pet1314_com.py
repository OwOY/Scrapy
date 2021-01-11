import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    name = "pet1314_com"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["http://www.pet1314.com/"]
    
    def parse(self, response):
        
        categorys = response.xpath("//div[@class='channel']//li/a/span/text()").getall()
        category_urls = response.xpath("//div[@class='channel']//li/a/@href").getall()
        i = 0
        while i < len(categorys):
            for page in range(1,21):
                category_page_url = category_urls[i].replace('.html', f'_{page}.html')
                yield scrapy.Request(f'http://www.pet1314.com{category_page_url}', callback=self.parse_article_urls, meta={"category" : categorys[i]})
            i += 1
    
            
    def parse_article_urls(self, response):

        article_urls = response.xpath("//li[@class='io']//div[@class='title-box']/a/@href").getall()
        for article_url in article_urls:
            yield scrapy.Request(f'{article_url}', callback=self.parse_article_contents, meta={"category" : response.meta['category']})
            
    def parse_article_contents(self, response):
        
        title = response.xpath("//h1[@class='arttitle']/text()").get().strip()
        contents = response.xpath("//div[@class='content']//p/text()|//div[@class='content']//p/img/@src").getall()
        contents = self.content_filter(contents)
        print(f'=================={title}==================\n{response.url}\n{contents}')
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = response.meta['category']
        item["content"] = contents
        #item['time_decline'] = datetime.datetime.utcnow()
        yield item

    
    def content_filter(self, contents):
        
        _contents = []
        for content in contents:
            content = content.strip()
        
            if content != '':
                _contents.append(content)
        
        return _contents
