import scrapy
from allscrapy.items import AllscrapyItem
import datetime



class dianjinghuSpider(scrapy.Spider):
    name = "dianjinghu_com"
    # allowed_domains = [""]
    start_urls = ["https://www.dianjinghu.com"]

    def parse(self, response):
    
        # yield scrapy.Request(self.start_urls[0], callback=self.main_parse) 
        for page in range(1,51):
            total_esport = {
                    'lol' : f'https://lol.dianjinghu.com/news/p/all/{page}.html',
                    'pubg':f'http://pubg.dianjinghu.com/news/p/all/{page}.html',
                    'pvp':f'http://pvp.dianjinghu.com/news/p/all/{page}.html',
        }
                            
            for category, category_link in total_esport.items():
                yield scrapy.Request(f"{category_link}", callback=self.parse_article_urls, meta={'category':category}) 
        
    def parse_article_urls(self, response):
        category = response.meta['category']
        
        if category == 'lol':
            link_list = response.xpath("//a[@class='media-lg']/@href").getall()
            link_list = ['https://lol.dianjinghu.com' + link for link in link_list]
            for link in link_list:
                yield scrapy.Request(f"{link}", callback=self.parse_content, meta={'category':category}) 
                
        elif category == 'pubg':
            link_list = response.xpath("//a[@class='media-lg']/@href").getall()
            link_list = ['https://pubg.dianjinghu.com' + link for link in link_list]
            for link in link_list:
                yield scrapy.Request(f"{link}", callback=self.parse_content, meta={'category':category}) 
            
        elif category == 'pvp':
            link_list = response.xpath("//a[@class='media-lg']/@href").getall()
            link_list = ['https://pvp.dianjinghu.com' + link for link in link_list]
            for link in link_list:
                yield scrapy.Request(f"{link}", callback=self.parse_content, meta={'category':category}) 
            
    def parse_content(self, response):
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        category = response.meta['category']
    
        title = response.xpath("//div[@class='c-title']/h1/text()").get()
        contents = response.xpath("//div[@class='new_conts']/p//text()|//div[@class='new_conts']/p/img/@src").getall()
        contents = self.content_filter(contents)

        print(f'{title}\n{contents}')
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = category
        item["content"]  = contents
        yield item
        
        
    def content_filter(self, contents):
        
        _contents = []
        for content in contents:
            content = content.strip()
            content = content.replace('\u200b','')
            if '/static/upload' in content:
                content = self.start_urls[0] + content
            if content == '':
                continue
            _contents.append(content)
            
        return _contents