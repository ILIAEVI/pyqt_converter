import requests


class CurrencyAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = f"https://api.currencyapi.com/v3/latest?apikey={self.api_key}&currencies=EUR%2CGEL%2CUSD"
        self.currency_rates = {}
        self.static_currency_rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GEL": 2.7
        }

    def fetch_currency_rates(self):
        try:
            response = requests.get(self.base_url)
            data = response.json()
            self.currency_rates = {code: details['value'] for code, details in data['data'].items()}
            return self.currency_rates
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to currency API: {e}")
            self.currency_rates = self.static_currency_rates
            return self.currency_rates

    def get_conversion_rate(self, from_currency, to_currency):
        return self.currency_rates[to_currency] / self.currency_rates[from_currency]
