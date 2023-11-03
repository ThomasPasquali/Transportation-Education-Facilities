import scrapy
from E656_scraper.items import Stop
import re

def parse_coordinate (x):
  if x is None:
    return 'NaN'
  digits = re.findall(r'\d+', x)
  if len(digits) < 4:
    digits.append('00')
  digits = ''.join(digits)
  print('?????????????????????????????????????????????????????????????????????????????', x, digits[:2] + ',' + digits[2:])
  return digits[:2] + ',' + digits[2:]

class TrainsFTMSpider(scrapy.Spider):
  name = 'FTMStops'
  allowed_domains = ['it.wikipedia.org']
  start_urls = ['https://it.wikipedia.org/wiki/Ferrovia_Trento-Mal%C3%A9-Mezzana']

  def parse(self, response):
    stops = response.css('table.wikitable tr > td:nth-child(3)')
    print(f'Found (in theory) {len(stops)} stops!!!')

    for stop in stops[1:]:
      stop = stop.css('a')
      if stop is not None:
        stop_name = stop.css('::text').get()
        if stop_name is not None and 'href' in stop.attrib:
          yield response.follow(
            f'https://it.wikipedia.org{stop.attrib["href"]}', 
            callback=self.parse_train_stop_geo,
            cb_kwargs=dict(stop_name=stop_name),
          )

  def parse_train_stop_geo (self, response, stop_name):
    stop = response.css('a > span.geo-default')
    lat = stop.css('span.latitude::text').get()
    lon = stop.css('span.longitude::text').get()
    yield Stop(
      item_type='Stop',
      stop_name=stop_name,
      stop_lat=parse_coordinate(lat),
      stop_lon=parse_coordinate(lon)
    )
  
  