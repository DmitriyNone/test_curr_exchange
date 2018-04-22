import requests
import json
from datetime import datetime, timedelta

open_exchange_rates_id = '###'
open_exchange_rates_api_location = "https://openexchangerates.org/api/latest.json?app_id="
request_address = open_exchange_rates_api_location + open_exchange_rates_id
rates_file = 'rates.json'


class CurrencyClass:
    def __init__(self, data_file, site_rates):
        self.base = 'USD'
        self.rates = {}
        self.data_file = data_file
        self.site_rates = site_rates
        self.all_rates = self.load_rates_from_file(data_file)
        self.rates_update_time = self.all_rates['timestamp']
        if self.rates_update_time < (datetime.now() - timedelta(days=1)).timestamp():
            print('rates are outdated')
            self.update_rates()
        self.rates['USD'] = self.all_rates['rates']['USD']
        self.rates['EUR'] = self.all_rates['rates']['EUR']
        self.rates['CZK'] = self.all_rates['rates']['CZK']
        self.rates['PLN'] = self.all_rates['rates']['PLN']

    def __str__(self):
        return 'timestamp: ' + str(self.all_rates['timestamp']) + '\nrates: ' + self.rates.__str__()

    def load_rates_from_file(self, file):
        with open(file, 'r') as fp:
            obj = json.load(fp)
            return obj

    def load_rates_from_site(self, address):
        obj = requests.get(address)
        with open(self.data_file, 'w') as outfile:
            json.dump(obj.json(), outfile)
        return obj.json()

    def update_rates(self):
        self.all_rates = self.load_rates_from_site(self.site_rates)
        self.rates['USD'] = self.all_rates['rates']['USD']
        self.rates['EUR'] = self.all_rates['rates']['EUR']
        self.rates['CZK'] = self.all_rates['rates']['CZK']
        self.rates['PLN'] = self.all_rates['rates']['PLN']
        print('rates updated\n')

    def curr_to_base(self, curr, amount):
        base_amount = amount / self.rates[curr]
        return base_amount

    def base_to_curr(self, curr, amount):
        curr_amount = amount * self.rates[curr]
        return curr_amount

    def curr_to_curr(self, from_curr, to_curr, amount):
        base_amount = self.curr_to_base(from_curr, amount)
        curr_amount = self.base_to_curr(to_curr, base_amount)
        return curr_amount
