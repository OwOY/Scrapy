import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    
    name = "cn_nytimes_com"
    allowed_domains = ["cn.nytimes.com"]
    start_urls = ["http://cn.nytimes.com/"]


    def parse(self, response):
        
        category_list = response.xpath("//li[@class='mainSection  drop']/a/text()|//li[@class='mainSection ']/a/text()").getall()
        category_link_list = response.xpath("//li[@class='mainSection  drop']/a/@href|//li[@class='mainSection ']/a/@href").getall()
        
        for category, category_link in zip(category_list, category_link_list):
            category_link = "https://cn.nytimes.com" + category_link
            yield scrapy.Request(category_link, callback=self.parse_article_urls, meta={"category" : category})
    
    
    
    def parse_article_urls(self, response):
        
        
            Link_list = response.xpath("//h3/a/@href").getall()
            next_link = response.xpath("//li/a[text()='下一页 >>']/@href").get()
            next_link = "https://cn.nytimes.com" + next_link
            
            category = response.meta["category"]
            
            for Link in Link_list:
                Link = f"https://cn.nytimes.com{Link}"
                yield scrapy.Request(Link, callback=self.parse_content, meta={"category" : category})
                
                
            if next_link.split("/")[-2].replace("/zh-hant","").replace("/","") != "101":
                yield scrapy.Request(next_link, callback=self.parse_article_urls, meta={"category" : category})
            
    
    
    def parse_content(self, response):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        Title = response.xpath("//h1/text()").get()
        content_ele = response.xpath("//div[@class='article-paragraph']")
        _content = []
        
        category = response.meta["category"]
        
        for content in content_ele:
            content = content.xpath(".//text()|.//img/@src").getall()
            content = "".join(content).replace("（歡迎點擊此處訂閱NYT簡報，我們將在每個工作日發送最新內容至您的郵箱。）","")
            content = "".join(content).replace("（欢迎点击此处订阅NYT简报，我们将在每个工作日发送最新内容至您的邮箱。）","")
            content = "".join(content).replace("[欢迎点击此处、或发送邮件至cn.letters@nytimes.com订阅《纽约时报》中文简报。]","")
            if content == "":
                continue
            if ".jpg" in content:
                content = content.split(".jpg")[0] + ".jpg"
            _content.append(content)
        
        print(f'{Title}\n{content}')
            
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = Title
        item["category"] = category
        item["content"] = _content
        yield item
            
            
            
            
            
            
            
            
            
