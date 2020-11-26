import scrapy
from allscrapy.items import AllscrapyItem
import datetime



class zmartSpider(scrapy.Spider):
    name = "www_zmarterlife_com"
    # allowed_domains = [""]
    start_urls = ["https://www.zmarterlife.com"]

    def parse(self, response):
    
        # yield scrapy.Request(self.start_urls[0], callback=self.main_parse) 
        page = 1
        
        while True:
            
            _link_list = response.xpath("//h2[@class='post-title']//a//@href").getall()
            
            link_list = []
            for link in _link_list:
                link_list.append("https://www.zmarterlife.com" + link)

            
            for link in link_list:
                yield scrapy.Request(link, callback=self.main_parse) 
            
            page += 1
            yield scrapy.Request(f"https://www.zmarterlife.com/page/{page}", callback=self.parse) 
            
            if page == 101:
                break
        
    def main_parse(self, response):
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        title = response.xpath("//h1[@class='post-title']/text()").get()
        contents = response.xpath("//div[@itemprop='articleBody']/article//p//text()|//div[@itemprop='articleBody']/article//p/img/@src|//div[@itemprop='articleBody']//iframe[not(@class='embed-responsive-item')]/@src").getall()
        contents = self.content_filter(contents)
        item = AllscrapyItem()
        img_list = response.xpath("//div[@itemprop='articleBody']/article//p/img/@src|//div[@itemprop='articleBody']//iframe[not(@class='embed-responsive-item')]/@src").getall()
        img_list = self.img_filter(img_list)
        print(f'{title}\n{contents}')
        
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = "all"
        item["content"]  = contents
        # item['image_urls'] = img_list
        yield item
        
        
    def content_filter(self, contents):
        
        _content = []
        for content in contents:
            content = content.strip()
            content = content.replace(r"\xa0","")
            content = content.replace(r"\u3000","")
            if "/upload/" in content:
                content = self.start_urls[0] + content
            if "延伸閱讀" in content:
                break
            if content != "":
                _content.append(content)
            
        return _content
            
    def img_filter(self, img_list):
        _img_list = []
        for img in img_list:
            if "/upload/" in img: 
                img = self.start_urls[0] + img
            _img_list.append(img)
        return _img_list