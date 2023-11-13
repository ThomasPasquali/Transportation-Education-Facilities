import scrapy
from E656_scraper.items import Train, TripStop

FTM_CALENDARS_TRAIN_NUMBERS = [
  [
    # Andata: Trento-Mezzana
    '302', '240', '4', '6', 'TT304', '8', '306', '10', '12', '14', '308', '16', '18', '44', '20', '310', '24', '26', '42', '28', '30', '312', '32', '34', '46', '314',
    # Ritorno: Mezzana-Trento
    '301', '1', '303', '3', '305', '5', '7', 'TT307', '9', '11', '15', '319', '17', '309', '19', '311', '21', '23', '25', '27', '29', '31', '33', '35'
  ],
  [
    # Andata: Trento-Mezzana
    '50', '52', '54', '56', '58', '60', '62', '64',
    # Ritorno: Mezzana-Trento
    '51', '53', '55', '57', '59', '61', '63', '65'
  ]
]
FTM_CALENDARS = [
  { 'id': '123450001', 'weekdays': '1111110', 'start_date': '20230911', 'end_date': '20240621' },
  { 'id': '123450002', 'weekdays': '0000001', 'start_date': '20230911', 'end_date': '20240621' }
]

class TrainsSpider(scrapy.Spider):
  name = 'FTMTrains'
  allowed_domains = ['www.e656.net']
  start_urls = [
    'https://www.e656.net/orario/stazione-tte/trento_ftm.html',
    'https://www.e656.net/orario/stazione-tte/male.html',
    'https://www.e656.net/orario/stazione-tte/mezzana.html',
    'https://www.e656.net/orario/stazione-tte/mezzolombardo.html'
  ]

  def parse(self, response):
    trains = response.css('table.train-list tr')
    print(f'Found (in theory) {len(trains)} trains!!!')

    for train in trains[1:]:
      # print(train)
      train_info = train.css('td:nth-child(2) span.train-number a')
      if train_info.get() is not None:
        t = Train(item_type='Train')
        t['name'] = train_info.css('::text').get().strip()
        if t['name'] in FTM_CALENDARS_TRAIN_NUMBERS[0]:
          t['calendar'] = FTM_CALENDARS[0]['id']
        elif t['name'] in FTM_CALENDARS_TRAIN_NUMBERS[1]:
          t['calendar'] = FTM_CALENDARS[1]['id']
        else:
          t['calendar'] = 'NaN'
          print('WARNING: calendar not found for train ' + t['name'])
        t['url'] = train_info.attrib['href']
        yield response.follow(
          f'https://www.e656.net/orario/treno-tte/{t["name"]}.html', 
          callback=self.parse_train_stops,
          cb_kwargs=dict(train_name=t['name']),
        )
        yield t
      
  def parse_train_stops (self, response, train_name):
    stops = response.css('table > tbody > tr')

    for stop in stops[1:]:
      yield TripStop(
        item_type='TripStop',
        train_name=train_name,
        stop=stop.css('td:nth-child(1)::text').get(),
        arrival_time=stop.css('td:nth-child(2)::text').get(),
        departure_time=stop.css('td:nth-child(3)::text').get()
      )