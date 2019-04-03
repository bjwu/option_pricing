"""
Implement Black-Scholes Formulas for European call/put option.
# @Author  :  Zhang Weibin
"""
import math
from math import e
from scipy.stats import norm

class BS_European_Option:
    
    def __init__(self, S, sigma, r, q, T, K):
        
        # the spot price of asset S(0) 
        self.S = S
        # the volatility
        self.sigma = sigma
        # risk-free interest rate r
        self.r = r
        # repo rate q
        self.q = q
        # time to maturity (in years) T
        self.T = T
        # strike
        self.K = K
        
    def Call_Option(self, t):
        
        t = 0
        S, sigma, r, q, T, K = self.S, self.sigma, self.r, self.q, self.T, self.K
        d1 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) + (1/2)*sigma*math.sqrt(T-t)
        d2 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) - (1/2)*sigma*math.sqrt(T-t)
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        C = S*e**(-q*(T-t))*N_d1 - K*e**(-r*(T-t))*N_d2
        return C
        
    def Put_Option(self, S, sigmoid, r, q, T, K):
        
        pass
        