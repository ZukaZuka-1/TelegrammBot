import requests
import json
from config import keys


class APIException(Exception):
    pass


class ValuesConverter:
    @staticmethod
    def get_prise(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Незачем переводить одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось перевести валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось перевести валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось перевести колличество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base