class Option:
    def __init__(self, strike, option_type, open_interest, volume, delta, gamma, theta):
        self.__strike = strike
        self.__option_type = option_type
        self.__open_interest = open_interest
        self.__volume = volume
        self.__delta = delta
        self.__gamma = gamma
        self._theta = theta
        
    def get_strike(self):
            return self.__strike
    def set_strike(self,strike):
            self.__strike = strike
    def get_option_type(self):
            return self.__option_type
    def set_option_type(self, option_type):
            self.__option_type = option_type
    def get_open_interest(self):
            return self.__open_interest
    def set_open_interest(self, open_interest):
            self.__open_interest = open_interest
    def get_volume(self):
            return self.__volume
    def set_volume(self, volume):
            self.__volume = volume
    def get_delta(self):
            return self.__delta
    def set_delta(self, delta):
            self.__delta = delta
    def get_gamma(self):
            return self.__gamma
    def set_gamma(self, gamma):
            self.__gamma = gamma
    def set_theta(self, theta):
            self.__theta = theta
    def get_theta(self):
            return self.__theta