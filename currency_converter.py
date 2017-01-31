#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from currency_converter.money import Money

def main(args):
    m = Money()
    result, code = m.try_convert(args.amount, args.input_currency, args.output_currency)
    print(json.dumps(result, indent=4, sort_keys=True))
    sys.exit(code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--amount', type=str, help="amount", required=True)
    parser.add_argument('--input_currency', type=str,  help="amount", required=True)
    parser.add_argument('--output_currency', type=str, help="amount", required=False)
    args = parser.parse_args()
    main(args)
