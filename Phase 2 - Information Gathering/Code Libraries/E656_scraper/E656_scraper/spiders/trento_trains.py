import scrapy
from E656_scraper.items import Train, TripStop

class TrainsSpider(scrapy.Spider):
  name = 'Trains'
  allowed_domains = ['www.e656.net']
  start_urls = [
    'https://www.e656.net/orario/stazione/trento/treni-dalle-00-alle-06.html',
    'https://www.e656.net/orario/stazione/trento/treni-dalle-06-alle-12.html',
    'https://www.e656.net/orario/stazione/trento/treni-dalle-12-alle-15.html',
    'https://www.e656.net/orario/stazione/trento/treni-dalle-15-alle-18.html',
    'https://www.e656.net/orario/stazione/trento/treni-dalle-18-alle-24.html',
  ]

  def parse(self, response):
    trains = response.css('table tbody tr')
    print(f'Got {len(trains)} trains!!!')
    for train in trains:
      if not 'ng-show' in train.attrib:
        train_info = train.css('td')
        t = Train(item_type='Train')
        train_number = train_info[1].css('span.train-number a')
        # Could also get train type e.g. Regionale, Regionale veloce tec.
        t['name'] = train_number.css('::text').get().strip()
        t['url'] = train_number.attrib['href']
        print(t['name'], t['url'])
        yield response.follow(
          f'https://www.e656.net{t["url"]}', 
          self.parse_train_stops,
          cb_kwargs=dict(train=t)
        )
        yield t

  def parse_train_stops (self, response, train):
    tmp = response.css('table')

    if len(tmp) > 1:
      stops_info = tmp[1].css('tbody tr')
    else:
      stops_info = tmp[0].css('tbody tr')

    # calendar_info = tmp[0].css('tbody')
    # TODO wait for element to render MADE WITH ANGULAR AND RENDERED AFTER
    # print('???????????????????', stops_info.get())
    # for c_info in calendar_info:
    #   c_info = c_info.css('td')
    #   print('BBBBBBBBB', c_info[0].get(), c_info[1].get())
    
    for s_info in stops_info:
      s_info = s_info.css('td')
      arrival_time = s_info[1].css('::text').get()
      if len(s_info) > 3:
        departure_time = s_info[2].css('::text').get()
      else:
        departure_time = arrival_time
      yield TripStop(
        item_type='TripStop',
        train_name=train['name'],
        stop=s_info[0].css('::text').get(),
        arrival_time=arrival_time,
        departure_time=departure_time
      )
