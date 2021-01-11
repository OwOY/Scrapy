import scrapy
from allscrapy.items import AllscrapyItem
import datetime
from scrapy import FormRequest

class NynewsSpider(scrapy.Spider):
    
    name = "mouzhan_org"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://mouzhan.org/"]
    
    def parse(self, response):
        # yield scrapy.Request(f'https://mouzhan.org/article/010659610.html', callback = self.parse_article_contents)
        
        category_urls = response.xpath("//div[@id='post-wrapper']//a/@href").getall()[6:12]
        i = 0
        while i < len(category_urls):
            # print(category_urls[i])
            yield scrapy.Request(f'https://mouzhan.org{category_urls[i]}', callback = self.parse_article_urls)
            i += 1
            
    def parse_article_urls(self, response):
        
        article_urls = response.xpath("//span[@class='post-first-category cat-links entry-meta-icon alignsize']//@href").getall()
        for article_url in article_urls:
            yield scrapy.Request(f'https://mouzhan.org{article_url}', callback = self.parse_article_contents)
                    
    def parse_article_contents(self, response):
        
        title = response.xpath("//h1[@class='entry-title']/text()").get().strip()
        
        imgs = response.xpath("//div[@id='deawfgregs']/*[not(self::blockquote)]/@src").getall()
        contents = response.xpath("//div[@id='deawfgregs']/*[not(self::blockquote)]/@src|//div[@id='deawfgregs']/text()").getall()
        if imgs == []:
            imgs = response.xpath("//div[@id='deawfgregs']/*[not(self::blockquote)]//@src").getall()
            contents = response.xpath("//div[@id='deawfgregs']/*[not(self::blockquote)]//@src|//div[@id='deawfgregs']/text()").getall()
        if imgs == []:
            imgs = response.xpath("//div[@class='entry-content']/p//@src").getall()
            contents = response.xpath("//div[@class='entry-content']/p//text()|//div[@class='entry-content']/p//@src").getall()
            
        category = response.xpath("//a[@rel='category tag']/text()").get()
        print(f'================{category}=={title}==================\n{response.url}')
        _contents = []
        for content in contents:
            content = content.strip()
            if "验证编码" in content:
                continue
            elif "高速上傳" in content:
                continue
            elif "全码" in content:
                continue
            elif "全碼" in content:
                continue
            elif "作种" in content:
                continue
            elif "做种" in content:
                continue
            elif "做種" in content:
                continue
            elif "下载" in content:
                continue
            elif "種子" in content:
                continue
            elif "特 征 码" in content:
                continue
            elif "哈希" in content:
                continue
            elif "期限" in content:
                continue
            elif "下載" in content:
                continue
            elif "download" in content:
                continue

            if content != '':
                _contents.append(content)
                print(content)
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = category
        item["content"] = _contents
        item["imgs"] = imgs
        item["cover"] = imgs[0]
        # item['time_decline'] = datetime.datetime.utcnow()
        yield item
