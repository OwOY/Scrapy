import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "news_qq_gossiping"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=ent&srv_id=pc&offset=0&limit=20&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:7,%22check_type%22:true}"]

    def parse(self, response):
        # yield scrapy.Request(f"{self.start_urls[0]}", callback=self.parse_article_urls) 
        offset = 0
        while offset < 200:
            next_urls = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=ent&srv_id=pc&offset='+str(offset)+'&limit=20&strategy=1&ext={%22pool%22:[%22top%22],%22is_filter%22:7,%22check_type%22:true}'
            yield scrapy.Request(f"{next_urls}", callback=self.parse_article_urls) 
            offset += 20
            
    def parse_article_urls(self, response):
        
        for data_inform in response.json()['data']['list']:
            article_urls = data_inform['url']
            category = data_inform['category_cn']
            if 'TWF' not in article_urls:
                print(article_urls)
                yield scrapy.Request(f"{article_urls}", callback=self.parse_content, meta={'category':category}) 

    def parse_content(self, response):
        
        category = response.meta['category']
        title = response.xpath('//div[@class="LEFT"]/h1/text()').get()
        img = response.xpath('//div[@class="content-article"]/p/img/@src').getall()
        
        if len(img) > 2:
            contents_xpath = response.xpath('//div[@class="content-article"]/p')
            contents = []
            for content_xpath in contents_xpath:
                content = content_xpath.xpath('.//text()|./img/@src').getall()
                contents.append(content[0])
            contents = self.content_filter(contents)
            
            if len(contents) < 20:
                print(f'=============={category}-{title}==={response.url}======================\n {contents}')
    
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                
                item = AllscrapyItem()
                item["url"] = response.url
                item["time"] = f"{datetime.date.today()}_{current_time}"
                item["title"] = title
                item["category"] = category
                item["content"] = contents
                yield item
        
    def content_filter(self, contents):
        
        _contents = []
        for content in contents:
            
            content = content.strip()
            if '本文作者原创' in content:
                continue
            if content != '':
                _contents.append(content)
        return _contents
    
    
