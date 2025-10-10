import requests
import json
import Ticker as ticker
import Option as option
import OptionChain as optionchain

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
class apiConn:
#example endpoint
    apiKey = ""
    def __init__(self, base_url):
        self.base_url = base_url
            
    def get_optionchain_data(self, Ticker: ticker, expiration, limit) -> optionchain:
        calls_endpoint = f"{self.base_url}/snapshot/options/{ticker.symbol}?expiration_date={expiration}&contract_type=call&order=asc&limit={limit}&sort=strike_price&apiKey={apiKey}"
        puts_endpoint = f"{self.base_url}/snapshot/options/{ticker.symbol}?expiration_date={expiration}&contract_type=put&order=asc&limit={limit}&sort=strike_price&apiKey={apiKey}"
        print(f"Making a request for {ticker.symbol} with expirary {expiration}")
        call_data = is_valid_request(calls_endpoint)
        put_data = is_valid_request(puts_endpoint)
        
        if call_data is None or put_data is None:
            print(f"Error occured when trying to get option chain data")
            return None
        
        try:
            call_options = call_data['results']
            put_options = put_data['results']
        except KeyError:
            print("Missing results array containing array of options")
            return None
        
        return self.input_fetched_option_data(put_options, call_options)
        
    def input_fetched_option_data(self, put_options: list, call_options: list) -> optionchain:
        chain = optionchain.OptionChain()
        
        total_contracts = put_options + call_options
        for contract in total_contracts:
            details = contract.get('details',{})
            day_data = contract.get('day',{})
            greeks = contract.get('greeks',{})
            #will add more params later on, first have to test this 
            new_option = option.Option(
                strike_price = details.get('strike_price'),
                option_type = details.get('contract_type'),
                open_interest = contract.get('open_interest'),
                volume = day_data.get('volume'),
                delta = greeks.get('delta'),
                gamma = greeks.get('gamma'),
                theta = greeks.get('theta')
            )
            chain.add_option(new_option)
            
        return chain
            
            
        #loop through each contract and create option obj for each then append to optionChain
        
            
            
            

      


#make this a class that imports Ticker,Option,OptionChain
#will call methods from OptionChain depending on params 
#such as expirary, underlyingTicker, # of strikes
