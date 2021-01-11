import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "tw5_com"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://www.te5.com/news/"]

    def parse(self, response):
        # yield scrapy.Request(f'https://www.te5.com/news/list_186_65.html', callback=self.parse_article_urls)
        
        page = 1
        while page < 101:   
            yield scrapy.Request(f'https://www.te5.com/news/list_186_{page}.html', callback=self.parse_article_urls)
            page += 1
            
    def parse_article_urls(self, response):
        
        category_url_list = response.xpath('//div[@class="main_content"]//h4/a/@href').getall()
        for category_url in category_url_list:
            
            yield scrapy.Request(f'{category_url}', callback=self.parse_article_contents)
      
    def parse_article_contents(self, response):
        
        print(response.url)
        title = response.xpath('//div[@class="arc_title"]/h1/text()').get()
        if response.xpath('//div[@class="arc_content"]//p/text()').getall() != []:
            contents = response.xpath('//div[@class="arc_content"]//p/text()|//div[@class="arc_content"]//img/@src').getall()
        else:
            contents = response.xpath('//div[@class="arc_content"]/div/text()|//div[@class="arc_content"]//img/@src').getall()
        contents = self.content_filter(contents)
        print(f'=================={title}==================\n{response.url}\n{contents}')
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = '攻略汇总'
        item["content"] = contents
        item['time_decline'] = datetime.datetime.utcnow()
        yield item
        
    def content_filter(self, contents):
        
        _contents = []
        for content in contents:
            
            content = content.strip()
            try:
                content = content.split('報導〕')[1]
            except:
                pass
            
            if content != '':
                _contents.append(content)

        return _contents
    
    
