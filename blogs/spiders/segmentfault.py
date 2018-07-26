
import scrapy
import json
from urllib import request
import re
from w3lib.html import remove_tags
from text.items import SegFaultItem


class SegFault(scrapy.Spider):
    name = "segfault"

    allowed_domains = []

    start_urls = ['https://segmentfault.com/']

    head = {
        "Host": "segmentfault.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        "Referer": "https://segmentfault.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    cookies = {
        "PHPSESSID": "web2~23veost2q6n7h7rnd5k295m97v",
        " _ga": "GA1.2.1258872482.1529971171",
        " Hm_lvt_e23800c454aa573c0ccb16b52665ac26": "1529971171,1530101549",
        " _gid": "GA1.2.791300640.1530101549",
        " afpCT": "1",
        " Hm_lpvt_e23800c454aa573c0ccb16b52665ac26": "1530144944",
    }

    custom_settings = {

        'ITEM_PIPELINES': {
           'text.pipelines.SegfaultMysqlPipeline': 1,
        }

    }


    def parse(self, response):
        url = "https://segmentfault.com/api/user/channels?_=467091321855a2789d5148272a9bcd08"

        yield scrapy.Request(url,callback=self.get_class,headers=self.head,cookies=self.cookies)

    def get_class(self,response):

        data = json.loads(response.text)
        status = data['status']
        for v in data['data']:
            item = SegFaultItem()
            class_name = v['name']
            class_id = v['id']
            url = v['url']
            slug = v['slug']

            item["class_name"] = class_name
            item["class_id"] = class_id




            base_url = request.urljoin(response.url,url)
            # print(base_url)
            # print(name,id,url,slug)
            yield scrapy.Request(base_url,callback=self.get_class_info,meta={'item':item})

    def get_class_info(self,response):
        item = response.meta['item']
        # 区块链
        url = "https://segmentfault.com/api/timelines/channel/1490000012722067/latest?before=1530099762582&_=378315c3feb615cd8db83e441553db2f "
        url = "https://segmentfault.com/api/timelines/channel/1490000012722067?offset=1528108238158&_=378315c3feb615cd8db83e441553db2f "


        # ai

        url = "https://segmentfault.com/api/timelines/channel/1490000010688683/latest?before=1530069781436&_=cd1c33d87034c2b1f43f49e180953c10"
        url = "https://segmentfault.com/api/timelines/channel/1490000010688683?offset=1529295508888&_=cd1c33d87034c2b1f43f49e180953c10 "

        # print(response.text)
        start_page_pat = re.compile(r'window.timelineBefore = (\d+?);')
        start_page = start_page_pat.search(response.text).group(1)

        start_param_pat = re.compile(r'window.pageParam = "(\d+?)"')
        start_param = start_param_pat.search(response.text).group(1)
        # print(start_param)
        # print(start_page)

        new_list = response.css("div.news-list>div")
        # print(new_list)
        for art in new_list:
            title = art.css('a.mr5::text').extract_first()
            art_url = art.css('a.mr5::attr(href)').extract_first()
            art_detail_url = request.urljoin(response.url,art_url)

            intor = art.css('div.article-excerpt::text').extract_first()

            likes = art.css('span.votes-num::text').extract_first()

            author = art.css('span.author a::text').extract_first()

            item["title"] = title
            item["art_detail_url"] = art_detail_url
            item["intor"] = intor
            item["likes"] = likes
            item["author"] = author



            # print(author)
            yield scrapy.Request(art_detail_url,callback=self.get_art_detail,meta={'item':item})

    def get_art_detail(self,response):
        item = response.meta['item']
        date = response.css('div.article__author span::text').extract()
        if len(date) >=2:
            date_pud = date[-1].split("·")[0].strip("\n \xa0")
            readnum = date[-1].split("·")[-1].strip("\n \xa0").strip('人阅读')
        else:
            date_pud = 'long long ago'
            readnum = "0"

        content = response.css('div.article__content').extract()
        if content:
            con = remove_tags(content[0],keep=('div','p'))
            content = self.re_tags(con)
        else:
            content = "么有内容"

        item["date_pud"] = date_pud
        item["readnum"] = readnum
        item["content"] = content
        item['spider'] = "segmentfault"

        yield item

    def re_tags(self,value):
        re_tags_pat = re.compile(r'<div.*?>')
        data = re.sub(re_tags_pat,'<div>',value)
        return data
