# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MonidengluEasyPipeline(object):
    def process_item(self, item, spider):
        with open("data.html","w") as f:
            f.write(item["item"])
        return item
