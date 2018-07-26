# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnsLogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    # 推荐
    diggitnum = scrapy.Field()

    # 作者
    author = scrapy.Field()
    # 评论
    comment = scrapy.Field()
    # 阅读
    view = scrapy.Field()
    # 发布时间
    date_pud = scrapy.Field()
    class_name = scrapy.Field()
    content = scrapy.Field()
    spider = scrapy.Field()

    def get_sql(self):
        sql = "insert into cnslogs(title,detail_url,diggitnum,author,comment,view,date_pud,class_name,content,spider) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (self["title"],self["detail_url"],self["diggitnum"],self["author"],self["comment"],self["view"],self["date_pud"],self["class_name"],self["content"],self["spider"])
        return sql,data


class CsdnItem(scrapy.Item):
    class_name = scrapy.Field()
    title = scrapy.Field()
    detail_url = scrapy.Field()
    date_pud = scrapy.Field()
    readnum = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    spider = scrapy.Field()
    def get_sql(self):
        sql = "insert into csdn(class_name,title,detail_url,date_pud,readnum,author,content,spider) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (self['class_name'],self['title'],self['detail_url'],self['date_pud'],self['readnum'],self['author'],self['content'],self['spider'])

        return sql,data


class SegFaultItem(scrapy.Item):
    class_name = scrapy.Field()
    class_id = scrapy.Field()
    title = scrapy.Field()
    art_detail_url = scrapy.Field()
    intor = scrapy.Field()
    likes = scrapy.Field()
    author = scrapy.Field()
    date_pud = scrapy.Field()
    readnum = scrapy.Field()
    content = scrapy.Field()
    spider = scrapy.Field()

    def get_sql(self):

        sql = "insert into segmentfault(class_name ,class_id ,title ,art_detail_url ,intor ,likes ,author ,date_pud ,readnum ,content ,spider ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (self["class_name"], self["class_id"], self["title"], self["art_detail_url"], self["intor"], self["likes"],self["author"], self["date_pud"], self["readnum"], self["content"], self["spider"])

        return sql,data

