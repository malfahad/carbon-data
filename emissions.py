
import requests
from datetime import datetime, timedelta
class API:
    base_url = None
    
    def call_api(self):
        if self.request_url:
            r = requests.get(self.request_url)
            return r.json()
            

class CarbonIntesnsity(API):

    def __init__(self):
        self.base_url = 'https://api.carbonintensity.org.uk'    
    
    def _parse_time(self, obj):
        if not obj:
            return None
        if not isinstance(obj, datetime):
            raise Exception('time should be a valid date time object')
        return obj.strftime('%Y-%m-%dT%H:%MZ')
       
    def get_endpoint(self, endpoint, start_from=None, to=None):
        no_filter = start_from == None and to == None
        start_from = self._parse_time(start_from)
        to = self._parse_time(to)
        
        self.request_url = f'{self.base_url}/{endpoint}' if no_filter else f'{self.base_url}/{endpoint}/{start_from}/{to}'
        
        return self.call_api()
    
    def get_intensity_last_half_hour(self):
        return self.get_endpoint('intensity')

    def get_intensity_between_days(self, start_from, to):
        return self.get_endpoint('intensity', start_from=start_from, to=to)

    def get_generation_last_half_hour(self):
        return self.get_endpoint('generation')

    def get_generation_between_dates(self, start_from, to):
        return self.get_endpoint('generation', start_from=start_from, to=to)

def print_data(title, data):
    rows = {}
    for item in data:
        for key in item.keys():
            existing_val = rows.get(key,'')
            rows[key] = f'{existing_val}\t{item[key]}\t'
    print(title)
    print("=======================")
    for key in rows.keys():
        print(f'{key} : {rows[key]}')
    print("--------------")
    print("\n")

def check_emissions():
    """
    calls the carpon emissions api and prints the response on teh console in tabular format

    Sample response:
    Generation mix from 2021-04-06T14:00Z  to 2021-04-06T14:30Z
    =======================
    fuel :  biomass         coal            imports         gas             nuclear         other           hydro           solar           wind
    perc :  4               0               5.8             14.6            14              0               1.8             13              46.8
    --------------

    Cabon Intensity, last 30 minutes
    =======================
    forecast :      84
    actual :        90
    index :         low
    --------------
    """
    api = CarbonIntesnsity()
    
    # get generation in last half hour
    result = api.get_generation_last_half_hour()
    if result:
        print_data('Generation mix, last 30 minutes', result['data']['generationmix'])

    # get generation in last 2 days
    today = datetime.now()
    days_ago = today - timedelta(days=2)
    result = api.get_generation_between_dates(days_ago, today)
    if result:
        for data in result['data']:
            title = f'Generation mix from {data["from"]}  to {data["to"]}'
            print_data(title, data['generationmix'])

    # get intensity in last half hour
    result = api.get_intensity_last_half_hour()
    if result:
        intensity_result = [result['data'][0]['intensity']]
        print_data('Cabon Intensity, last 30 minutes', intensity_result)


if __name__ == '__main__':
    check_emissions()