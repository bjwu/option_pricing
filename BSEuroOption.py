"""
Implement Black-Scholes Formulas for European call/put option.
# @Author  :  Zhang Weibin
"""
import math
from math import e
from scipy.stats import norm

class BSEuroOption:
    
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
        
    def CallOption(self, t = 0):
        
        S, sigma, r, q, T, K = self.S, self.sigma, self.r, self.q, self.T, self.K
        d1 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) + (1/2)*sigma*math.sqrt(T-t)
        d2 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) - (1/2)*sigma*math.sqrt(T-t)
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        CallValue = S*e**(-q*(T-t))*N_d1 - K*e**(-r*(T-t))*N_d2
        
        return CallValue
        
    def PutOption(self, t = 0):
        
        S, sigma, r, q, T, K = self.S, self.sigma, self.r, self.q, self.T, self.K
        d1 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) + (1/2)*sigma*math.sqrt(T-t)
        d2 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) - (1/2)*sigma*math.sqrt(T-t)
        Negative_N_d1 = norm.cdf(-d1)
        Negative_N_d2 = norm.cdf(-d2)
        PutValue = K*e**(-r*(T-t))*Negative_N_d2 - S*e**(-q*(T-t))*Negative_N_d1
        
        return PutValue
        