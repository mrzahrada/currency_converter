

class Money:
    def __init__(self):
        pass

    def get_code(self, currency):
        pass

    def supported_currencies(self):
        pass

    def get_symbol(self, currency):
        pass

    def download_rates(self):
        # unittest.request.urlopen
        pass

    def get_rate(self, input_currency, output_currency=None):
        pass

    def convert(self, amount, input_currency, output_currency=None):
        pass

    def try_convert(self, amount, input_currency, output_currency=None):
        pass
