import scrapy
from allscrapy.items import AllscrapyItem
import datetime

class NynewsSpider(scrapy.Spider):
    
    name = "bbs_2048"
    # allowed_domains = ["i.news.qq.com"]
    start_urls = ["https://bbs.98bazj.site/2048/thread.php?fid-15-page-1.html"]
    
    def parse(self, response):
        
        # yield scrapy.Request(f'https://bbs.98bazj.site/2048/read.php?tid-2945454-fpage-4.html', callback= self.parse_article_contents)
        for page in range(1,10):
            yield scrapy.Request(f'https://bbs.98bazj.site/2048/thread.php?fid-15-page-{page}.html', callback = self.parse_article_urls, meta = {'page':page})
    
            
    def parse_article_urls(self, response):

        if response.meta['page'] == 1:
            article_urls = response.xpath("//tr[@class='tr3 t_one']/td/a[@class='subject']//@href").getall()[6:]
        else:
            article_urls = response.xpath("//tr[@class='tr3 t_one']/td/a[@class='subject']//@href").getall()
        i = 0
        # article_urls = response.xpath("//tr[@class='tr3 t_one']/td/a[@class='subject']//@href").getall()
        
        while i < len(article_urls):
            # print(article_urls[i])
            yield scrapy.Request(f'https://bbs.98bazj.site/2048/{article_urls[i]}', callback=self.parse_article_contents)
            i+= 1
            
        # for article_url in article_urls:
            # print(article_url)
            
    def parse_article_contents(self, response):
        
        title = response.xpath("//h1[@id='subject_tpc']/text()").get().strip()
        contents = response.xpath("//div[@id='read_tpc'][.//*[not(contains(@href,'download'))]]/div/text()|//div[@id='read_tpc']//img/@src").getall()
        imgs = response.xpath("//div[@id='read_tpc']//img/@src").getall()
        if response.xpath("//div[@id='read_tpc']/div/text()").getall() == []:
            contents = response.xpath("//div[@id='read_tpc'][.//*[not(contains(@href,'download'))]]//text()|//div[@id='read_tpc']//img/@src").getall()
        
        
        print(f'=================={title}==================\n{response.url}')
        _contents = []
        for content in contents:
            content = content.strip()
            
            if '種子連結' in content:
                break
            elif "验证编码" in content:
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
            elif "種子" in content:
                continue
            elif "种子" in content:
                continue
            elif "特 征 码" in content:
                continue
            elif "哈希" in content:
                continue
            elif "期限" in content:
                continue
            elif "下載" in content:
                continue
            elif "下载" in content:
                continue
            elif "編碼" in content:
                continue
            elif "download" in content:
                continue
            if content != '':
                print(content)
                _contents.append(content)
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        item = AllscrapyItem()
        item["url"] = response.url
        item["time"] = f"{datetime.date.today()}_{current_time}"
        item["title"] = title
        item["category"] = '國內原創'
        item["content"] = _contents
        item["imgs"] = imgs
        item["cover"] = imgs[0]
        # item['time_decline'] = datetime.datetime.utcnow()
        yield item
