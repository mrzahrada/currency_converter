

import urllib
import json

class Money:
    def __init__(self):

        self.url = "http://api.fixer.io/latest?base="
        self.base_currency = "USD"

        self.rates = self.download_rates()

    def get_code(self, currency):
        pass

    def supported_currencies(self):
        pass

    def get_symbol(self, currency):
        pass

    def download_rates(self):
        with urllib.request.urlopen(self.url + self.base_currency) as req:
            rates = json.loads(req.read().decode('utf-8'))['rates']
        rates[self.base_currency] = 1.0
        return rates

    def get_rate(self, input_currency, output_currency=None):
        pass

    def convert(self, amount, input_currency, output_currency=None):
        pass

    def try_convert(self, amount, input_currency, output_currency=None):
        pass
