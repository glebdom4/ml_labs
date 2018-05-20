import requests
import sys

from .exceptions import ConversionError


class CurrencyConverter:
    """
    Class for converting currencies using rates from
    min-api.cryptocompare.com.
    """

    URL_API = "https://min-api.cryptocompare.com/data/{}"
    REQUESTS_TIMEOUT = 10

    _KEY_FROM = 'from'
    _KEY_TO = 'to'


    def __init__(self, currencies, new_currencies):
        """
        Gets available currencies.
        """
        self._currencies = dict()
        self._rates = self._get_rates(currencies, new_currencies)


    def _get_rates(self, currencies, new_currencies):
        """
        Gets available currencies rates.
        """
        rates = dict()
        for curr in currencies:
            new_curr = ','.join(map(str, new_currencies))
            local_rates = self._make_request('price', fsym=curr,
                                             tsyms=new_curr)
            if self._check_bad_response(local_rates):
                raise ValueError(local_rates['Message'])
            else:
                self._save_currencies(currencies, new_currencies)

            rates[curr] = local_rates

        return rates


    def _check_bad_response(self, request_res):
        """
        Checks bad response.
        """
        if 'Response' in request_res and request_res['Response'] == 'Error':
            return True
        
        return False


    def _save_currencies(self, curr, new_curr):
        """
        Saves available currencies to dictionary.
        """
        self._currencies[self._KEY_FROM] = list(set(curr))
        self._currencies[self._KEY_TO] = list(set(new_curr))


    def _make_request(self, suburl, **params):
        """
        Makes a request to the api of the cryptocompare.com service
        and returns a response in json format.
        """
        r = requests.get(self.URL_API.format(suburl), params=params,
                         timeout=self.REQUESTS_TIMEOUT)
        r.raise_for_status()

        return r.json()


    def convert(self, amount, currency, new_currency='EUR'):
        """
        Convert amount from a currency to another one.
        """
        conv_amount = -1
        self._check_currency(currency)
        self._check_currency(new_currency)

        if self._check_convertibility(currency,
                                      new_currency,
                                      self._KEY_FROM,
                                      self._KEY_TO):
            conv_amount = amount * float(self._rates[currency][new_currency])
        elif self._check_convertibility(currency,
                                        new_currency,
                                        self._KEY_TO,
                                        self._KEY_FROM):
            conv_amount = amount / float(self._rates[new_currency][currency])
        elif currency == new_currency:
            conv_amount = amount
        else:
            raise ConversionError(
                "'{0}' can't be converted to '{1}'...".format(currency,
                                                              new_currency))
        
        return float(conv_amount)


    def _check_currency(self, currency):
        """
        Checks if any rates available for the input currency. 
        """
        if (currency not in self._currencies['from'] and
                currency not in self._currencies['to']):
            raise ValueError(
                '{0} is not a supported currency.'.format(currency))


    def _check_convertibility(self, currency, new_currency, first_key, second_key):
        """
        Checks if currencies can be converted.
        """
        if (currency in self._currencies[first_key] and
                new_currency in self._currencies[second_key]):
            return True
        
        return False


if __name__ == '__main__':

    currencies = ['BYN', 'USD', 'EUR'] 
    new_currencies = ['RUB',]
    c = CurrencyConverter(currencies, new_currencies)
    print(c._currencies['from'])
    print(c._currencies['to'])
    print(c._rates)
    print(str(c.convert(1500.0, 'USD', 'RUB')))
