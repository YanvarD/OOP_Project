import requests
import json
from config import keys


class APIexception(Exception):
    pass


class ConvertCurrency:

    @staticmethod
    def convert(quote: str, base: str, amount: str):
        quote_tiker, base_tiker = keys[quote], keys[base]


        if quote == base:
            raise APIexception('Невозможно перевести одну валюту в другую')
        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIexception(f'Не удалось обработать валюту{quote}')
        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIexception(f'Не удалось обработать валюту{base} ')

        try:
            amount = float(amount)
        except ValueError:
            raise APIexception(f'Не удалось обработать количество {amount}')

        link = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiker}&tsyms={base_tiker}')

        total_base = json.loads(link.content)[keys[base]]
        data = float(total_base) * float(amount)
        data = round(data, 2)

        return data