

import urllib.request
import json

from operator import mul
from toolz import valmap
from toolz.functoolz import  partial


def load_json(file_path):
    with open(file_path) as data_file:
        data = json.load(data_file)
    return data

class Money:
    def __init__(self):
        self.url = "http://api.fixer.io/latest?base="
        self.base_currency = "USD"
        self.symbols = self.load_symbols()
        self.rates = self.download_rates()


    def load_symbols(self):
        currencies = load_json('raw_data/currencies.json')["currencies"]
        result = {}
        for cur in currencies:
            if cur['symbols'].get('suported') is None:
                continue
            for symbol in cur['symbols']['suported']:
                result[symbol] = cur['code']
        return result



    def get_code(self, currency):
        # TODO: beautify this code
        # TODO: kr -> SEK, DKK, NOK. so for kr symbol raise exception
        #       try_convert should return help message with possible codes
        currency = str(currency).strip().upper()
        if currency in self.rates:
            return currency
        # if currency is not in symbols, returns None
        return self.symbols.get(currency)

    def supported_currencies(self):
        return self.rates.keys()

    def get_symbol(self, currency):
        currency = str(currency).strip()

        if self.symbols.get(currency) is not None:
            return currency

        currency = currency.upper()
        for key, value in self.symbols.items():
            if value == currency:
                return key
        return None

    def update_rates(self):
        '''
        This class downloads latest rates if neccesary (ECB publish new
        rates peridically) and store them in property.
        Also updates property last_rates_update
        '''
        pass

    def download_rates(self):
        with urllib.request.urlopen(self.url + self.base_currency) as req:
            rates = json.loads(req.read().decode('utf-8'))['rates']
        rates[self.base_currency] = 1.0
        return rates

    def get_rate(self, input_currency, output_currency=None):
        '''
        This method returns dict with key as input currency code and value as
            exchange rate input_currency/output_currency.
        If output_currency is None or not specified, return exchange rates
            to all supported currencies
        TODO: add examples
        '''
        input_currency_rate = self.rates[input_currency]
        generate_rate = partial(mul, 1/input_currency_rate)
        if output_currency is None:
            return valmap(generate_rate, self.rates)
        else:
            return {output_currency : generate_rate(self.rates[output_currency])}

    def convert_from_rate(self, amount, exchange_rate):
        mul_by_amount = partial(mul, amount)
        return round(mul_by_amount(exchange_rate), 2)

    def convert(self, amount, input_currency, output_currency=None):
        '''
        This method takes, amount, input_currency,output_currency and
        generates conversion. If output_currency is not defined or None,
        geenerates conversion to all supported currencies.
        return dictionary:
            {
                "input" : {
                    "amount": <amount>,
                    "currency": <input_currency>
                },
                "output": {
                    "<output_currency>": <conversion_rate>
                }
            }
        '''
        # correct inputs
        amount = float(amount)
        input_currency = self.get_code(input_currency)
        output_currency = self.get_code(output_currency)
        # get rates which interest me
        rates = self.get_rate(input_currency, output_currency)
        # conversion function
        convert_single = partial(self.convert_from_rate, amount)
        # convert rates that interested me
        output = valmap(convert_single, rates)

        # TODO: ugly return, define method
        return {
            "input": {
                "amount": amount,
                "currency": input_currency,
            },
            "output": output
        }

    def try_convert(self, amount, input_currency, output_currency=None):
        # TODO: return convert result or error message + return code ()
        pass
