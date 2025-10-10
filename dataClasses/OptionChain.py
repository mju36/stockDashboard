import Ticker as ticker
import Option as option
class OptionChain:
    def __init__(self, ticker, date):
        self._ticker = ticker
        self._option = option
        self._date = date
        self._call_chain = {}
        self._put_chain = {}
    ###add options to optionChain: "exp date" consisting of both calls/put chain
    ###get optionChain for each putChain/callChain
    
        
    def add_option(self, option: "Option"):
        if option.get_option_type() == "call":
            self._call_chain[option.get_strike()] = option
        else:
            self._put_chain[option.get_strik()] = option
    