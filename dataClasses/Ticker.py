class Ticker:
    def __init__(self, symbol, price, volume):
        self.__symbol = symbol.upper()
        self._price = price
        self.__volume = volume 
        
        def get_symbol(self):
            return self.__symbol
        
        def set_symbol(self, symbol):
            self.__symbol = symbol
            
        def get_price(self):
            return self.__price
        
        def set_price(self, price):
            self.__price = price
            
        def get_volume(self):
            return self._volume
        
        def set_volume(self, volume):
            self._volume = volume
            