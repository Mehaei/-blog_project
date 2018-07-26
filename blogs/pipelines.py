# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json
class TextPipeline(object):
    def process_item(self, item, spider):
        return item
class CnsLogsPipeline(object):
    def open_spider(self,spider):
        self.f = open('jsonfile/cnslogs.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        item['spider'] = spider.name
        try:
            self.f.write(json.dumps(dict(item),ensure_ascii=False)+',\n')
        except Exception as e:
            print('文件写入错误，错误为%s'%e)
        return item
    def close_spider(self,spider):
        self.f.close()


class CnsMysqlPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect('127.0.0.1','root','123456','reptile',charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        sql,data = item.get_sql()
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except Exception as e:
            print('写入数据库错误，错误为%s'%e)
            self.db.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()


class CsdnMysqlPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect('127.0.0.1','root','123456','reptile',charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        sql,data = item.get_sql()
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except Exception as e:
            print('写入数据库错误，错误为%s'%e)
            self.db.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()

class SegfaultMysqlPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect('127.0.0.1','root','123456','reptile',charset="utf8")
        self.cursor = self.db.cursor()

    def process_item(self,item,spider):
        sql,data = item.get_sql()
        try:
            self.cursor.execute(sql,data)
            self.db.commit()
        except Exception as e:
            print('写入数据库错误，错误为%s'%e)
            self.db.rollback()
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()
