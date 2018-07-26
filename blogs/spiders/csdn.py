import scrapy
from urllib import request
import json
import re
from w3lib.html import remove_tags
from text.settings import COOKIE
from text.items import CsdnItem
class Csdn(scrapy.Spider):
    name = "csdn"
    allowed_domains = []
    start_urls = ['https://www.csdn.net/']

    custom_settings = {
        "ITEM_PIPELINES" : {
           'text.pipelines.CnsMysqlPipeline': 1,
        }

    }



    def parse(self, response):
        li_list = response.css('div.nav_com ul li')

        for li in li_list[3:]:
            item = CsdnItem()
            class_name = li.css('a::text').extract()[0]
            item['class_name'] = class_name
            class_url_list = li.css('a::attr(href)').extract()
            showmn_list = []
            for class_url in class_url_list:
                base_url = request.urljoin(response.url,class_url)
                yield scrapy.Request(base_url,callback=self.get_class_info,meta={'item':item})
            # print(showmn_list)
    def get_class_info(self,response):
        item = response.meta['item']
        shown_offset = response.xpath('//div[@class="fixed_content"]/main/ul/@shown-offset').extract()[0]
        # 文章
        types = response.url.split('/')[-1]
        if not types:
            types = 'home'

        url = "https://www.csdn.net/api/articles?type=more&category=%s&shown_offset=%s"
        # print(shown_offset)
        base_url = url % (types,shown_offset)

        yield scrapy.Request(base_url,callback=self.get_info,cookies=COOKIE,meta={'item':item})

    def get_info(self,response):
        item = response.meta['item']
        html = json.loads(response.text)
        shown_offset = html['shown_offset']

        if shown_offset != 0:
            new_url = "=".join(response.url.split("=")[:-1]) + '=' + str(shown_offset)
            yield scrapy.Request(new_url,callback=self.get_info,cookies=COOKIE)


        arti_list = html['articles']
        for art in arti_list:
            detail_url = art['url']
            item["detail_url"] = detail_url
            yield scrapy.Request(detail_url,callback=self.get_detail,meta={'item':item})


    def get_detail(self,response):
        item = response.meta['item']
        title = response.css('h1.title-article::text').extract()[0]
        info = response.css('div.article-bar-top span::text').extract()
        date_pud = info[0]
        readnum = info[1].strip('阅读数：')
        author = response.css('a#uid::text').extract()[0]
        content = response.css('div.htmledit_views').extract()[0]
        con = remove_tags(content,keep=('div','p'))
        content = self.re_move(con)

        item["title"] = title

        item["date_pud"] = date_pud
        item["readnum"] = readnum
        item["author"] = author
        item["content"] = content
        item['spider'] = "csdn"
        yield item


    def re_move(self,value):
        re_tag = re.compile(r'<div.*?>')
        res = re.sub(re_tag,'<div>',value)
        return res