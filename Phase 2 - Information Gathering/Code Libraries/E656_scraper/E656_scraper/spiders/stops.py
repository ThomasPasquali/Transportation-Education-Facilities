import scrapy
from E656_scraper.items import Stop
import re

# FIXME 'a'
LETTERS = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'z']

class StopsSpider(scrapy.Spider):
  name = 'Stops'
  allowed_domains = ['www.e656.net']
  start_urls = [f'https://www.e656.net/orario/stazioni/{l}.html' for l in LETTERS]

  def parse(self, response):
    # i = 0
    stop_links = response.css('#wrap > div.container > div > div:nth-child(3) a')
    print(f'Found (in theory) {len(stop_links)} stops!!!')

    for stop_link in stop_links:
      print('Fetch!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! '+ stop_link.css('::text').get())
      yield response.follow(
        f'https://www.e656.net{stop_link.attrib["href"]}', 
        callback=self.parse_train_stop_geo,
        cb_kwargs=dict(stop_name=stop_link.css('::text').get()),
      )
      # i = i + 1
      # if i > 5:
      #   break

  def parse_train_stop_geo (self, response, stop_name):
    script = response.css('#map-modal > div > div > div.modal-body.modal-body-map > script:nth-child(2)')
    if len(script) <= 0:
      print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Coords script not founf for stop: ' + stop_name)
    else:
      script = script[0]
      coords = re.findall(r'new Microsoft\.Maps\.Location\((\d+\.\d+), (\d+\.\d+)\)', script.css('::text').get())
      lat = None
      lon = None
      if len(coords) > 0:
        lat = coords[0][0]
        lon = coords[0][1]
      yield Stop(
        item_type='Stop',
        stop_name=stop_name,
        stop_lat=lat,
        stop_lon=lon
      )
  
  