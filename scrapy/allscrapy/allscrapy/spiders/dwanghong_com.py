import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "dwanghong_com"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["http://www.dwanghong.com/news/", 'http://www.dwanghong.com/ziliao/']
    def parse(self, response):
        # yield scrapy.Request(f'http://www.dwanghong.com/news/2635.html', callback=self.parse_article_contents)
        last_page = response.xpath('//div[@class="paging"]/a[7]//text()').get()
        page = 1
        if 'news' in response.url:
            while page < int(last_page):   
                yield scrapy.Request(f'http://www.dwanghong.com/news/index_{page}.html', callback=self.parse_article_urls)
                page += 1
        else:
            while page < int(last_page):   
                yield scrapy.Request(f'http://www.dwanghong.com/ziliao/index_{page}.html', callback=self.parse_article_urls)
                page += 1
                        
    def parse_article_urls(self, response):
        
        category_url_list = response.xpath('//div[@class="content-list"]//li/a/@href').getall()
        for category_url in category_url_list:
            yield scrapy.Request(f'http://www.dwanghong.com{category_url}', callback=self.parse_article_contents)
      
    def parse_article_contents(self, response):
        
        title = response.xpath('//div[@class="content-article"]/h1/text()').get()
        if title == None:
            title = response.xpath('//div[@class="intro-content clearfix"]/h1/text()').get()
        contents = response.xpath('//div[@class="article"]/p//descendant::text()|//div[@class="article"]//img/@src').getall()
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
    
    
