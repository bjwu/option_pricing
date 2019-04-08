"""
Implement closed-form formulas for geometric basket call/put options.
# @Author : Zhang Weibin
"""

import math
from math import e
from numpy.random import standard_normal as StdNormal
from scipy.stats import norm

class CFGeoBasketOption:

    def __init__(self, s0_1 = None, s0_2 = None, sigma_1 = None, sigma_2 = None, 
                 r = 0, T = 0, K = None, rho = None, option_type = None):

        #assert option_type == 'call' or option_type == 'put'
        # the Spot Price of Asset S1(0)
        self.s0_1 = s0_1
        # the Spot Price of Asset S2(0)
        self.s0_2 = s0_2
        # the Volatility of Asset S1(0)
        self.sigma_1 = sigma_1
        # the Volatility of Asset S2(0)
        self.sigma_2 = sigma_2
        # the Risk-free Interest Rate
        self.r = r
        # Time to Maturity (in year)
        self.T = T
        # the Strike
        self.K = K
        # the correlation
        self.rho = rho
        self.option_type = option_type

    def CallGeoBasket(self, t = 0):
        
        s0_1, s0_2, sigma_1, sigma_2, r, T, K, rho = self.s0_1, self.s0_2, self.sigma_1, self.sigma_2, self.r, self.T, self.K, self.rho
        
        C11, C12, C22 = 1, rho, 1 
        sigma_B = math.sqrt((sigma_1**2)*C11 + 2*sigma_1*sigma_2*C12 + sigma_2**2*C22)/2
        mu = r - (1/2)*((sigma_1**2 + sigma_2**2)/2) + (1/2)*sigma_B**2
        
        Bg = math.sqrt(s0_1*s0_2)
        d1 = (math.log(Bg/K) + (mu + (1/2)*sigma_B**2)*T)/(sigma_B*math.sqrt(T))
        d2 = d1 - sigma_B*math.sqrt(T)
        
        N_d1_P = norm.cdf(d1)
        N_d2_P = norm.cdf(d2)
        
        # closed-form formula for geometric basket call option
        Call = e**(-(r*T))*(Bg*e**(mu*T)*N_d1_P - K*N_d2_P)
        
        return Call
    
    def PutGeoBasket(self, t = 0):
        
        s0_1, s0_2, sigma_1, sigma_2, r, T, K, rho = self.s0_1, self.s0_2, self.sigma_1, self.sigma_2, self.r, self.T, self.K, self.rho
        
        C11, C12, C22 = 1, rho, 1 
        sigma_B = math.sqrt((sigma_1**2)*C11 + 2*sigma_1*sigma_2*C12 + sigma_2**2*C22)/2
        mu = r - (1/2)*((sigma_1**2 + sigma_2**2)/2) + (1/2)*sigma_B**2
        
        Bg = math.sqrt(s0_1*s0_2)
        d1 = (math.log(Bg/K) + (mu + (1/2)*sigma_B**2)*T)/(sigma_B*math.sqrt(T))
        d2 = d1 - sigma_B*math.sqrt(T)
        
        N_d1_N = norm.cdf(-d1)
        N_d2_N = norm.cdf(-d2)
        
        # closed-form formula for geometric basket put option
        Put = e**(-(r*T))*(K*N_d2_N - Bg*e**(mu*T)*N_d1_N)
        
        return Put
