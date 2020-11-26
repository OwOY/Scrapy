import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "new_qq_total1"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = [f"https://pacaio.match.qq.com/tags/tag2articles?id=101574&num=60&expIds=&callback=__jp0"]

    def parse(self, response):
        
        url_id_list = ['255683', '101574', '92548', '82542']
        
        for url_id in url_id_list:
            yield scrapy.Request(f"https://pacaio.match.qq.com/tags/tag2articles?id={url_id}&num=60&expIds=&callback=__jp0", callback=self.parse_article_urls) 
            
    def parse_article_urls(self, response):
        
        response_json = eval(response.text[6:-1])
        for data_inform in response_json['data']:
            article_urls = data_inform['vurl']
            category = data_inform['category_chn']
            yield scrapy.Request(f"{article_urls}", callback=self.parse_content, meta={'category':category}) 

    def parse_content(self, response):
        category = response.meta['category']
        title = response.xpath('//div[@class="LEFT"]/h1/text()').get()
        img = response.xpath('//div[@class="content-article"]/p/img/@src').getall()

        contents_xpath = response.xpath('//div[@class="content-article"]/p')
        contents = []
        for content_xpath in contents_xpath:
            content = content_xpath.xpath('.//text()|./img/@src').getall()
            contents.append(content[0])
        contents = self.content_filter(contents)

        if len(contents) >0:    
            print(f'=============={category}-{title}==={response.url}======================\n {contents}')

            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            item = AllscrapyItem()
            item["url"] = response.url
            item["time"] = f"{datetime.date.today()}_{current_time}"
            item["title"] = title
            item["category"] = category
            item["content"] = contents
            item['time_decline'] = datetime.datetime.utcnow()
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
    
    
