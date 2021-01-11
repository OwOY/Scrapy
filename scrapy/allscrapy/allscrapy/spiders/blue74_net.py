import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "blue74_net"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://blue74.net/category/taichungfood/"]
    def parse(self, response):
        
        category_url_list = response.xpath("//ul[@class='menu']/li/a/@href").getall()[1:]
        category_list = response.xpath("//ul[@class='menu']/li/a/text()").getall()[1:]
        i = 0
        while i < len(category_url_list):
            yield scrapy.Request(category_url_list[i], callback=self.parse_article_urls, meta = {'category':category_list[i]})
            i += 1
    
    def parse_article_urls(self, response):
        
        article_urls = response.xpath("//article[@class='blog-post']//h1/a/@href").getall()
        next_page = response.xpath("//div[@class='nav-links']/a[text()='下一頁']/@href").get()
        
        for article_url in article_urls:
            yield scrapy.Request(f'{article_url}', callback=self.parse_article_contents, meta = {'category':response.meta['category']})
        try:
            yield scrapy.Request(f'{next_page}', callback=self.parse_article_urls, meta = {'category':response.meta['category']})
        except:
            pass
    def parse_article_contents(self, response):
        
        title = response.xpath('//article[@class="page-single"]/header/h1/text()').get()
        contents = response.xpath('//article[@class="page-single"]/p[not(.//span[@class="single-mid"])]//text()|//article[@class="page-single"]//img/@src').getall()
        imgs = response.xpath('//article[@class="page-single"]//img/@src').getall()
        contents = self.content_filter(contents, imgs)
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
        
    def content_filter(self, contents, imgs):
        
        _contents = []
        for content in contents:
            content = content.strip().replace(u'\xa0','').replace('　',' ')
            if content in imgs:
                content = f'http:{content}'
            if content != '':
                _contents.append(content)

        return _contents
    
    
