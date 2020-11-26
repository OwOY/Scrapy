import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "hupu_com"
    allowed_domains = ["voice.hupu.com"]
    start_urls = ["https://voice.hupu.com/"]


    def parse(self, response):
        
        for page in range(1, 51):
            
            total_sport = {
                "英超":f"https://voice.hupu.com/soccer/tag/496-{page}.html",
                "西甲":f"https://voice.hupu.com/soccer/tag/225-{page}.html",
                "德甲":f"https://voice.hupu.com/soccer/tag/1106-{page}.html",
                "意甲":f"https://voice.hupu.com/soccer/tag/700-{page}.html",
                "中超":f"https://voice.hupu.com/china/{page}",
                "NBA":f"https://voice.hupu.com/nba/{page}",
                "CBA":f"https://voice.hupu.com/cba/{page}"
        }
            
            for sport in total_sport:
                # sport_type(sport, total_sport[sport])
                yield scrapy.Request(total_sport[sport], callback=self.parse_get_article_urls, meta={"category" : sport})
            
    def parse_get_article_urls(self, response):
        
        category = response.meta["category"]
        
        if category == "中超" or category == "NBA" or category == "CBA":
            article_link_list = response.xpath("//div[@class='list-hd']//a/@href").getall()
        else:
            article_link_list = response.xpath("//div[@class='list-content']//div/span/a//@href").getall()
            
        for article_link in article_link_list:
            yield scrapy.Request(article_link, callback=self.parse_get_article_content, meta={"category" : category})
    
    
    def parse_get_article_content(self, response):
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        title = response.xpath("//h1[@class='headline']/text()").get()
        title = title.strip()
        contents = response.xpath("//div[@class='artical-content-read']//text()|//div[@class='artical-content-read']//img//@src").getall()
        contents = self.content_filter(contents)
        print(f'{title}\n{contents}')
        
        item = AllscrapyItem()
        
        item["url"] = response.url
        item["title"] = title
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["category"] = response.meta["category"]
        item["content"] = contents
        yield item
            
            
    def content_filter(self, contents):
        
        _contents = []

        for content in contents:
            content = content.strip()
            
            if "(编辑：" in content:
                break 
            if len(content) > 0:
                _contents.append(content)

        return _contents


