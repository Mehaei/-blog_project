import scrapy
from urllib import request
from w3lib.html import remove_tags
import re
from text.items import CnsLogsItem
class CnsLogs(scrapy.Spider):

    name = 'cnslogs'
    allowed_domains = []
    start_urls = ['https://www.cnblogs.com/']
    custom_settings = {
        "ITEM_PIPELINES" :{
            'text.pipelines.CnsLogsPipeline':1,
            'text.pipelines.CnsMysqlPipeline': 2,

        }
    }

    def parse(self, response):
        url = "https://www.cnblogs.com/aggsite/SubCategories"
        body = '{"cateIds":"108698,2,108701,108703,108704,108705,108709,108712,108724,4"}'
        yield scrapy.Request(url,callback=self.get_class_info,method="POST",body=body)
        # classify_list_url = response.css('ul#cate_item li a::attr(href)').extract()
        # for classify_url in classify_list_url[:-1]:
        #     class_ify_url = request.urljoin(response.url,classify_url)

            # yield scrapy.Request(class_ify_url,callback=self.get_class_info)

    def get_class_info(self,response):
        class_list = response.xpath('//div[@class="cate_content_block_wrapper"]/div[@class="cate_content_block"]/ul')
        for class_i in class_list:
            # title = class_i.css('li a::text').extract()
            class_url = class_i.css('li a::attr(href)').extract()
            for url in class_url:
                base_url = request.urljoin(response.url,url)
                yield scrapy.Request(base_url,callback=self.get_detail_class)

    def get_detail_class(self,response):
        # print(response.url)
        max_page = response.xpath('//div[@class="pager"]/a[last()-1]/text()').extract()[0]
        # print(base_url)
        for page in range(int(max_page),0,-1):
            info_url = request.urljoin(response.url,str(page))
            # print(info_url)
            yield scrapy.Request(info_url,callback=self.get_info)

    def get_info(self,response):

        # title = response.xpath('//div[@class="post_item_body"]/h3/a/text()').extract()

        # for url in detail_url:
            # yield scrapy.Request(url,callback=self.get_detail)
        class_name = response.xpath('//a[@class="current_nav"]/text()').extract()[0]

        article_list =  response.css('div#post_list div.post_item')
        for article in article_list:
            item = CnsLogsItem()
            title = article.css('div.post_item_body h3 a::text').extract()[0]
            detail_url = article.css('div.post_item_body h3 a::attr(href)').extract()[0]
            # 推荐
            diggitnum = article.css('span.diggnum::text').extract()[0]

            article_info = article.css('div.post_item_foot a::text').extract()
            # 作者
            author = article_info[0]
            # 评论
            comment = article_info[1].strip().strip('评论()')
            # 阅读
            view = article_info[2].strip('阅读()')
            # 发布时间
            date_pud = article.css('div.post_item_foot::text').extract()[-1].strip().strip('发布于')

            # print(class_name,title,diggitnum,author,comment,view,date_pud)
            item["title"] = title
            item["detail_url"] = detail_url
            # 推荐
            item["diggitnum"] = diggitnum
            # 作者
            item["author"] = author
            # 评论
            item["comment"] = comment
            # 阅读
            item["view"] = view
            # 发布时间
            item["date_pud"] = date_pud
            item["class_name"] = class_name

            yield scrapy.Request(detail_url,callback=self.get_detail,meta={'item':item})

            # print(diggitnum,author,comment,view,date_pud)
    def get_detail(self,response):
        item = response.meta['item']
        # title = response.css('a#cb_post_title_url::text').extract()[0]
        # author_detail = response.xpath('//div[@id="author_profile_detail"]')
        content = response.css('div#cnblogs_post_body').extract()[0]
        con = remove_tags(content,keep=('div','p'))
        content = self.tags_pat(con)
        item["content"] = content
        # print(title,author_detail)
        yield item
    def tags_pat(self,value):
        tag_pat = re.compile(r'<div.*?>')
        con = re.sub(tag_pat,'<div>',value)
        return con


