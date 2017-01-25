
import unittest


class TestGetCode(unittest.TestCase):
    def setUp(self):
        self.money = Money()

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
    def setUp(self):
        pass

    def tearDown(self):
        pass

class TestGetSymbol(unittest.TestCase):
    def setUp(self):
        pass

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

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestGetRate(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestConvert(unittest.TestCase):
    def setUp(self):
        pass

    def test_valid_code_code(self):
        pass

    def test_valid_code_none(self):
        pass

    def test_valid_symbol_code(self):
        pass

    def test_valid_code_symbol(self):
        pass

    def test_valid_symbol_symbol(self):
        pass

    def test_valid_symbol_none(self):
        pass

    def tearDown(self):
        pass

class TestTryConvert(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
