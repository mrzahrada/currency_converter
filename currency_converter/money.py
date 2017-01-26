

import urllib
import json

# TODO: load from config
symbols = ['AR$': 'ARS',
            '$': 'USD',
            'R$': 'BRL',
            'CL$': 'CLP',
            '¥': 'JPY',
            '€': 'EUR',
            '£': 'GBP',
            '₪': 'ILS',
            '₩': 'KRW',
            '฿': 'THB',
            '₫': 'VND',
            'R': 'ZAR']

class Money:
    def __init__(self):

        self.url = "http://api.fixer.io/latest?base="
        self.base_currency = "USD"
        self.symbols = symbols
        self.rates = self.download_rates()

    def get_code(self, currency):
        # TODO: beautify this code
        currency = str(currency).strip().upper()
        if self.rates.get(currency) is not None:
            return currency
        else:
            symbol = self.symbols.get(currency)
            if symbol is not None:
                return symbol
        return None

    def supported_currencies(self):
        return self.rates.keys()

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
