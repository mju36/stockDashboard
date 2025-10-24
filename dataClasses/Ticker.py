class Ticker:
    def __init__(self, symbol, price, volume):
        self.symbol = symbol.upper()
        self.price = float(price)
        self.volume = int(volume) 
        
    def get_symbol(self):
            return self.symbol
        
    def set_symbol(self, symbol):
            self.symbol = symbol
            
    def get_price(self):
            return self.price
        
    def set_price(self, price):
            self.price = price
            
    def get_volume(self):
            return self.volume
        
    def set_volume(self, volume):
            self.volume = volume
            