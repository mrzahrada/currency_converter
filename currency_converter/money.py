

import urllib.request
import json
import sys

from datetime import datetime
from operator import mul
from toolz import valmap
from toolz.functoolz import  partial

from currency_converter.exceptions import ConnectionError, UnsupportedCurrencyError

def load_json(file_path):
    '''
    From file returns json
    '''
    with open(file_path) as data_file:
        data = json.load(data_file)
    return data

class Money:
    def __init__(self):
        self.url = "http://api.fixer.io/latest?base="
        self.base_currency = "USD"
        self.symbols = self.load_symbols()
        self.rates = self.download_rates()
        self.last_rates_update = datetime.utcnow()

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
        currency = str(currency).strip().upper()
        if currency in self.rates:
            return currency
        # if currency is not in symbols, returns None
        return self.symbols.get(currency)

    def supported_currencies(self):
        '''
        This method returns all supported currency codes
        '''
        return self.rates.keys()

    def get_symbol(self, currency):
        '''
        This method returns symbol for any supported currency. Otherwise returns None.
        '''
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
        # TODO: check datetime
        self.rates = self.download_rates()
        self.last_rates_update = datetime.utcnow()

    def download_rates(self):
        try:
            with urllib.request.urlopen(self.url + self.base_currency) as req:
                rates = json.loads(req.read().decode('utf-8'))['rates']
            rates[self.base_currency] = 1.0
            return rates
        except urllib.error.URLError as e:
            raise ConnectionError("Can't download rates, url error.")
        except urllib.error.HTTPError as e:
            raise ConnectionError("Can't download rates, http error.")
        except:
            raise ConnectionError("Can't download rates")

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
        # input_currency has to be specified
        if input_currency is None:
            raise UnsupportedCurrencyError("Unknown input currency")
 
        # get rates which interest me
        rates = self.get_rate(input_currency, output_currency)
        # conversion function
        convert_single = partial(self.convert_from_rate, amount)
        # convert rates that interested me
        output = valmap(convert_single, rates)

        return {
            "input": {
                "amount": amount,
                "currency": input_currency,
            },
            "output": output
        }

    def try_convert(self, amount, input_currency, output_currency=None):
        '''
        This method calls convert safely, returns convert result
        or error message. And error code
        '''
        try:
            return self.convert(amount, input_currency, output_currency), 0
        except ConnectionError as e:
            return { 'ConnectionError': str(e)}, 1
        except UnsupportedCurrencyError as e:
            return { 'UnsupportedCurrencyError': str(e)}, 1
        except ValueError as e:
            return {'ValueError': 'Wrong input type.'}, 1
        except:
            e = sys.exc_info()[0]
            return { 'error': str(e)}, 1


