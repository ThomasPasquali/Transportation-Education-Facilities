# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
import re

class Train(scrapy.Item):
  item_type = Field()
  name = Field()
  url = Field()
  calendar = Field()

class TripStop(scrapy.Item):
  item_type = Field()
  train_name = Field()
  stop = Field()
  arrival_time = Field()
  departure_time = Field()

class Stop(scrapy.Item):
  item_type = Field()
  stop_name = Field()
  stop_lat = Field()
  stop_lon = Field()

