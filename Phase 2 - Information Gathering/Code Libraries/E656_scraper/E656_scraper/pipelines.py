# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class E656ScraperPipeline:
  def process_item(self, item, spider):
    i = ItemAdapter(item)
    for field in i.field_names():
      print('PIPELINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE', field, i.get(field))
      if i.get(field) is not None and i.get(field).strip:
        i[field] = i.get(field).strip()
    return item
