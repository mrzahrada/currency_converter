
import codecs
import json
import unittest

from mock import patch

from currency_converter.money import Money


test_data_path = "raw_data/test_rates.json"

class MockResponse(object):
    '''
        Simple mock for urllib.request for downloading exchange_rates
    '''
    def __init__(self, code=200, msg='OK'):
        self.resp_data = self.load_data()
        self.code = code
        self.msg = msg
        self.headers = {'content-type': 'text/plain; charset=utf-8'}

    def read(self):
        return self.resp_data

    def getcode(self):
        return self.code

    def load_data(self):
        with open(test_data_path) as data_file:
            data = json.load(data_file)
        return codecs.encode(json.dumps(data))

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
        self.assertEqual(self.money.get_code("€"), "GBP")
        self.assertEqual(self.money.get_code("£"), "ISL")
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
        expected = []
        self.assertEqual(result, expected)

    def tearDown(self):
        pass

class TestGetSymbol(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def test_valid_code(self):
        self.assertEqual(self.money.get_code("USD"), "$")
        self.assertEqual(self.money.get_code("uSd"), "$")
        self.assertEqual(self.money.get_code("sek"), "kr")

        self.assertEqual(self.money.get_code("EUR "), "€")
        self.assertEqual(self.money.get_code(" CZK"), "Kč")
        self.assertEqual(self.money.get_code(" JPY   "), "¥")

    def test_invalid_code(self):
        self.assertEqual(self.money.get_code("abcd"), None)
        self.assertEqual(self.money.get_code(44), None)
        self.assertEqual(self.money.get_code(None), None)
        # ZAR - it's not listed in ECB exchange rates
        self.assertEqual(self.money.get_code("R"), None)
        self.assertEqual(self.money.get_code("$$"), None)
        self.assertEqual(self.money.get_code("€€"), None)
        self.assertEqual(self.money.get_code(" ₩ ₩ "), None)

    def test_valid_symbol(self):
        self.assertEqual(self.money.get_code("$"), "$")
        self.assertEqual(self.money.get_code("€"), "€")
        self.assertEqual(self.money.get_code(" £ "), "£")
        self.assertEqual(self.money.get_code(" ₩"), "₩")
        self.assertEqual(self.money.get_code("฿ "), "฿")
        self.assertEqual(self.money.get_code("   ₫  "), "₫")

    def tearDown(self):
        pass

class TestDownloadRates(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def tearDown(self):
        pass


class TestGetRate(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def tearDown(self):
        pass

class TestConvert(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def assertConvert(self, amount, input_currency, output_currency, expected_output):
        result = self.money.convert(amount, input_currency, output_currency)

        self.assertEqual(amount, result["input"]["amount"])
        self.assertEqual(input_currency, result["input"]["input_currency"])
        for key, value in expected_output.items():
            self.assertEqual(value, result["output"][key])

    def test_valid_code_code(self):
        amount = 100
        input_currency = "USD"
        output_currency = "EUR"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output)

    def test_valid_code_none(self):
        amount = 100
        input_currency = "USD"
        output_currency = None
        expected_output = {
            "USD": 100,
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output)

    def test_valid_symbol_code(self):
        amount = 100
        input_currency = "$"
        output_currency = "EUR"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output)

    def test_valid_code_symbol(self):
        amount = 100
        input_currency = "USD"
        output_currency = "€"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output)

    def test_valid_symbol_symbol(self):
        amount = 100
        input_currency = "$"
        output_currency = "€"
        expected_output = {
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output)

    def test_valid_symbol_none(self):
        amount = 100
        input_currency = "USD"
        output_currency = None
        expected_output = {
            "USD": 100,
            "EUR": 93.08
        }
        self.assertConvert(amount, input_currency, output_currency, expected_output)

    def tearDown(self):
        pass

class TestTryConvert(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def setUp(self, urlopen_mock):
        urlopen_mock.return_value = MockResponse()
        self.money =  Money()

    def tearDown(self):
        pass
