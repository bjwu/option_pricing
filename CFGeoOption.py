"""
Implement closed-form formulas for geometric Asian call/put options and geometric basket call/put options.
# @Author :
"""

class CFGeoAsianOption:

    def __init__(self):
        pass

    def pricing(self):
        pass


class CFGeoBasketOpton:

    def __init__(self, s0_1=None, s0_2=None, sigma_1=None, sigma_2=None,
                 r=0, T=0, K=None, rho=None, option_type=None):

        assert option_type == 'call' or option_type == 'put'
        self.s0_1 = s0_1
        self.s0_2 = s0_2
        self.sigma_1 = sigma_1
        self.sigma_2 = sigma_2
        self.r = r
        self.T = T
        self.K = K
        self.rho = rho
        self.option_type = option_type

    def pricing(self):
        pass
