class Option:
    def __init__(self, strike, option_type, open_interest, volume, delta, gamma, theta):
        self.strike = strike
        self.option_type = option_type
        self.open_interest = open_interest
        self.volume = volume
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        
    def get_strike(self):
            return self.strike
    def set_strike(self,strike):
            self.strike = strike
    def get_option_type(self):
            return self.option_type
    def set_option_type(self, option_type):
            self.option_type = option_type
    def get_open_interest(self):
            return self.open_interest
    def set_open_interest(self, open_interest):
            self.open_interest = open_interest
    def get_volume(self):
            return self.volume
    def set_volume(self, volume):
            self.volume = volume
    def get_delta(self):
            return self.delta
    def set_delta(self, delta):
            self.delta = delta
    def get_gamma(self):
            return self.gamma
    def set_gamma(self, gamma):
            self.gamma = gamma
    def set_theta(self, theta):
            self.theta = theta
    def get_theta(self):
            return self.theta