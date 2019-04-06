"""
Implement Black-Scholes Formulas for European Call/Put Option.
# @Author: Zhang Weibin
"""
import math
from math import e
from scipy.stats import norm

class BSEuroOption:
    
    # the Spot Price of Asset S
    # Implied Volatility sigma
    # Risk-free Interest Rate r
    # Repo Rate q
    # Time to Maturity (in years) T
    # Strike K
        
    def CallOption(self, S, sigma, r, q, T, K , t = 0):
        
        d1 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) + (1/2)*sigma*math.sqrt(T-t)
        d2 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) - (1/2)*sigma*math.sqrt(T-t)
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        CallPremium = S*e**(-q*(T-t))*N_d1 - K*e**(-r*(T-t))*N_d2
        
        return CallPremium
        
    def PutOption(self, S, sigma, r, q, T, K, t = 0):
        
        d1 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) + (1/2)*sigma*math.sqrt(T-t)
        d2 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) - (1/2)*sigma*math.sqrt(T-t)
        Negative_N_d1 = norm.cdf(-d1)
        Negative_N_d2 = norm.cdf(-d2)
        PutPremium = K*e**(-r*(T-t))*Negative_N_d2 - S*e**(-q*(T-t))*Negative_N_d1
        
        return PutPremium
        