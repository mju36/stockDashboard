import requests
import json
import dataClasses.Ticker as Ticker
import dataClasses.Option as Option
import dataClasses.OptionChain as OptionChain

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
class polygonAPI:
#example endpoint
    def __init__(self, apiKey):
        self.base_url = 'https://api.polygon.io/v3'
        self.apiKey = apiKey
            
    def get_optionchain_data(self, Ticker: Ticker, expiration, limit) -> OptionChain:
            calls_endpoint = f"{self.base_url}/snapshot/options/{Ticker.symbol}?expiration_date={expiration}&contract_type=call&order=asc&limit=50&sort=strike_price&apiKey={self.apiKey}"
            puts_endpoint = f"{self.base_url}/snapshot/options/{Ticker.symbol}?expiration_date={expiration}&contract_type=put&order=asc&limit=50&sort=strike_price&apiKey={self.apiKey}"
            print(f"Making a request for {Ticker.symbol} with expirary {expiration}")
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
        
            return self.input_fetched_option_data(put_options, call_options, Ticker, expiration)
        
    def input_fetched_option_data(self, put_options: list, call_options: list, ticker: Ticker, expiration: str) -> OptionChain:
        chain = OptionChain.OptionChain(ticker, expiration)
    
        total_contracts = put_options + call_options
    
    # Extract all strike prices
        strikes = [contract.get('details', {}).get('strike_price') 
               for contract in total_contracts 
               if contract.get('details', {}).get('strike_price') is not None]
    
    # Get unique strikes
        unique_strikes = list(set(strikes))
    
    # Sort by distance from current ticker price
        unique_strikes.sort(key=lambda strike: abs(strike - ticker.price))
    
    # Take closest 10 strikes
        closest_10_strikes = unique_strikes[:10]
    
    # Convert to set for fast lookup
        selected_strikes = set(closest_10_strikes)
    
    # Filter contracts to only include those with selected strikes
        filtered_contracts = [contract for contract in total_contracts 
                         if contract.get('details', {}).get('strike_price') in selected_strikes]
    
    # Create Option objects for filtered contracts
        for contract in filtered_contracts:
            details = contract.get('details', {})
            day_data = contract.get('day', {})
            greeks = contract.get('greeks', {})
        
        # Will add more params later on, first have to test this 
            new_option = Option.Option(
                strike=details.get('strike_price'),
                option_type=details.get('contract_type'),
                open_interest=contract.get('open_interest'),
                volume=day_data.get('volume'),
                delta=greeks.get('delta'),
                gamma=greeks.get('gamma'),
                theta=greeks.get('theta')
            )
            chain.add_option(new_option)
    
        return chain
            
            
        #loop through each contract and create option obj for each then append to optionChain
        
            
            
            

      


#make this a class that imports Ticker,Option,OptionChain
#will call methods from OptionChain depending on params 
#such as expirary, underlyingTicker, # of strikes
