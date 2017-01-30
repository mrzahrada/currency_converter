
import codecs
import json
import unittest

from mock import patch

from currency_converter.money import Money

def load_data(test_data_path):
    with open(test_data_path) as data_file:
        data = json.load(data_file)
    return data

class MockResponse:
    '''
        Simple mock for urllib.request for downloading exchange_rates
    '''
    def __init__(self, code=200, msg='OK'):
        data = load_data("raw_data/test_rates.json")
        self.resp_data = codecs.encode(json.dumps(data))
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        pass

class TestGetCode(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def test_valid_code(self):
        self.assertEqual(self.money.get_code("USD"), "USD")
        self.assertEqual(self.money.get_code("uSd"), "USD")
        self.assertEqual(self.money.get_code("sek"), "SEK")

        self.assertEqual(self.money.get_code("EUR "), "EUR")
        self.assertEqual(self.money.get_code(" CZK"), "CZK")
        self.assertEqual(self.money.get_code(" JPY   "), "JPY")

    def test_invalid_code(self):
        self.assertEqual(self.money.get_code("abcd"), None)
        self.assertEqual(self.money.get_code(44), None)
        self.assertEqual(self.money.get_code(None), None)
        # ZAR - it's not listed in ECB exchange rates
        self.assertEqual(self.money.get_code("R"), None)

    def test_valid_symbol(self):
        self.assertEqual(self.money.get_code("$"), "USD")
        self.assertEqual(self.money.get_code("€"), "EUR")
        self.assertEqual(self.money.get_code("£"), "GBP")
        self.assertEqual(self.money.get_code("₩"), "KRW")
        self.assertEqual(self.money.get_code("฿"), "THB")
        self.assertEqual(self.money.get_code("₫"), "VND")

    def tearDown(self):
        pass

class TestSupportedCurrencies(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def test_currencies(self):
        result = self.money.supported_currencies()
        expected = ["AUD","BGN","BRL","CAD","CHF","CNY","CZK","DKK","GBP",
            "HKD","HRK","HUF","IDR","ILS","INR","JPY","KRW","MXN","MYR",
            "NOK","NZD","PHP","PLN","RON","RUB","SEK","SGD","THB","TRY",
            "ZAR","EUR", "USD"]
        self.assertCountEqual(expected, result)

    def tearDown(self):
        pass

class TestGetSymbol(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money = Money()

    def test_valid_code(self):

        result = self.money.get_symbol("USD")
        print(result)
        self.assertEqual(result, "$")


        self.assertEqual(self.money.get_symbol("USD"), "$")
        self.assertEqual(self.money.get_symbol("uSd"), "$")
        #self.assertEqual(self.money.get_symbol("sek"), "kr")

        self.assertEqual(self.money.get_symbol("EUR "), "€")
        self.assertEqual(self.money.get_symbol(" CZK"), "Kč")
        self.assertEqual(self.money.get_symbol(" CNY   "), "¥")

    def test_invalid_code(self):
        self.assertEqual(self.money.get_symbol("abcd"), None)
        self.assertEqual(self.money.get_symbol(44), None)
        self.assertEqual(self.money.get_symbol(None), None)
        # ZAR - it's not listed in ECB exchange rates
        self.assertEqual(self.money.get_symbol("R"), None)
        self.assertEqual(self.money.get_symbol("$$"), None)
        self.assertEqual(self.money.get_symbol("€€"), None)
        self.assertEqual(self.money.get_symbol(" ₩ ₩ "), None)

    def test_valid_symbol(self):
        self.assertEqual(self.money.get_symbol("$"), "$")
        self.assertEqual(self.money.get_symbol("€"), "€")
        self.assertEqual(self.money.get_symbol(" £ "), "£")
        self.assertEqual(self.money.get_symbol(" ₩"), "₩")
        self.assertEqual(self.money.get_symbol("฿ "), "฿")
        self.assertEqual(self.money.get_symbol("   ₫  "), "₫")

    def tearDown(self):
        pass

class TestDownloadRates(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money = Money()
        self.rates = self.money.download_rates()

    def test_download(self):
        data = load_data("raw_data/test_rates.json")
        data["rates"]["USD"] = 1.0
        self.assertEqual(self.rates, data['rates'])

    def tearDown(self):
        pass

class TestGetRate(unittest.TestCase):
    # TODO: add more tests
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()
        self.rates = {'AUD': 1.323, 'BGN': 1.8205, 'BRL': 3.1702, 'CAD': 1.3097, 'CHF': 0.99898, 'CNY': 6.8822, 'CZK': 25.153, 'DKK': 6.9223, 'GBP': 0.79422, 'HKD': 7.7579, 'HRK': 6.9792, 'HUF': 288.3, 'IDR': 13330.0, 'ILS': 3.785, 'INR': 68.08, 'JPY': 113.37, 'KRW': 1164.9, 'MXN': 21.472, 'MYR': 4.4315, 'NOK': 8.3266, 'NZD': 1.3766, 'PHP': 49.638, 'PLN': 4.0623, 'RON': 4.1875, 'RUB': 59.227, 'SEK': 8.8274, 'SGD': 1.4184, 'THB': 35.23, 'TRY': 3.8241, 'ZAR': 13.273, 'EUR': 0.93084, 'USD': 1.0}

    def test_all_rates_USD(self):
        result = self.money.get_rate("USD")
        for cur, rate in self.rates.items():
            self.assertEqual(result[cur], rate)

    def test_single_rate(self):
        self.assertEqual(self.money.get_rate("USD", "USD")["USD"], 1.0)
        self.assertTrue(abs(self.money.get_rate("EUR", "USD")["USD"]-1.07430)  < 0.00001)
        self.assertTrue(abs(self.money.get_rate("USD", "JPY")["JPY"]-113.37)   < 0.00001)
        self.assertTrue(abs(self.money.get_rate("GBP", "CNY")["CNY"]-8.66536)  < 0.00001)
        self.assertTrue(abs(self.money.get_rate("CNY", "JPY")["JPY"]-16.47293) < 0.00001)
        self.assertTrue(abs(self.money.get_rate("USD", "CZK")["CZK"]-25.153)   < 0.00001)

    def tearDown(self):
        pass

class TestConvertFromRate(unittest.TestCase):
    # TODO: add more tests
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def test_convert_from_rate(self):
        rate = 1.23445
        amount = 100

        # rate*amount rounded
        expected = 123.45
        self.assertEqual(expected, self.money.convert_from_rate(amount, rate))

    def tearDown(self):
        pass

class TestConvert(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def assertConvert(self, amount, input_currency, output_currency, expected_output, expected_input):
        result = self.money.convert(amount, input_currency, output_currency)

        self.assertEqual(amount, result["input"]["amount"])
        self.assertEqual(expected_input, result["input"]["currency"])
        for key, value in expected_output.items():
            self.assertEqual(value, result["output"][key])

    def test_valid_code_code(self):
        amount = 100
        input_currency = "USD"
        output_currency = "EUR"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output, input_currency)

    def test_valid_code_none(self):
        amount = 100
        input_currency = "USD"
        output_currency = None
        expected_output = {
            "USD": 100,
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output, input_currency)

    def test_valid_symbol_code(self):
        amount = 100
        input_currency = "$"
        output_currency = "EUR"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output, "USD")

    def test_valid_code_symbol(self):
        amount = 100
        input_currency = "USD"
        output_currency = "€"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output, input_currency)

    def test_valid_symbol_symbol(self):
        amount = 100
        input_currency = "$"
        output_currency = "€"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output, "USD")

    def test_valid_symbol_none(self):
        amount = 100
        input_currency = "USD"
        output_currency = None
        expected_output = {
            "USD": 100,
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output, input_currency)

    def tearDown(self):
        pass

class TestTryConvert(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def tearDown(self):
        pass
