from dataClasses import Ticker
from dataClasses import Option
class OptionChain:
    def __init__(self, ticker: Ticker, date):
        self.ticker = ticker
        self.date = date
        self.call_chain = {}
        self.put_chain = {}
    ###add options to optionChain: "exp date" consisting of both calls/put chain
    ###get optionChain for each putChain/callChain
    
        
    def add_option(self, option: Option):
        if option.get_option_type() == "call":
            self.call_chain[option.get_strike()] = option
        else:
            self.put_chain[option.get_strike()] = option
    
    def get_call_chain(self):
        return self.call_chain
    
    def get_put_chain(self):
        return self.put_chain
    
    
    