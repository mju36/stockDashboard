import requests
import json
from dataClasses.Ticker import Ticker

def is_valid_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        # 3. Handle specific HTTP status code errors (e.g., 404 Not Found)
        print(f"ERROR: API returned a bad status code ({response.status_code}). Details: {e}")
        return None

    except requests.exceptions.RequestException as e:
        # 4. Handle general network/connection errors (e.g., DNS failure, timeout, connection reset)
        print(f"ERROR: A network or connection error occurred. Details: {e}")
        return None

    except Exception as e:
        # 5. Catch any other unexpected error
        print(f"AN UNEXPECTED ERROR OCCURRED: {e}")
        return None

class alphaVantage:
    def __init__(self, apiKey, symbol):
        self.base_url = 'https://www.alphavantage.co/query'
        self.symbol = symbol
        self.api_key = apiKey

    def get_stock_data(self) -> Ticker:
        url = f"{self.base_url}?function=GLOBAL_QUOTE&symbol={self.symbol}&apikey={self.api_key}"
        stock_data = is_valid_request(url)

        if stock_data is None:
            print('Failed to fetch stock data')
            return None

        try:
            quotes = stock_data.get('Global Quote')
            if not quotes:
                print('No quote data returned from API')
                return None

            price = quotes.get('05. price')
            volume = quotes.get('06. volume')

            if price is None or volume is None:
                print('Missing price or volume data')
                return None

        except (KeyError, AttributeError) as e:
            print(f'Error parsing ticker info: {e}')
            return None

        return Ticker(self.symbol, price, volume)
