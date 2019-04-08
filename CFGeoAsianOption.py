"""
Implement closed-form formulas for geometric Asian call/put options.
# @Author: Zhang Weibin
"""
import math
from math import e
from scipy.stats import norm

class GeoAsianOption():
    
    def __init__(self, S, sigma, r, T, K, n):
        
        # the Spot Price of Asset S(0)
        self.S = S
        # the Implied Volatility
        self.sigma = sigma
        # the Risk-free Interest Rate
        self.r = r
        # Time to Maturity (in year)
        self.T = T
        # the Strike
        self.K = K
        # the number of observation times for the geometric average
        self.n = n
    
    # for call option
    def CallGeoAsian(self):
        
        S, sigma, r, T, K, n = self.S, self.sigma, self.r, self.T, self.K, self.n
    
        sigma_hat = sigma*math.sqrt(((n + 1)*(2*n + 1))/(6*n**2))
        mu = (r - (1/2)*sigma**2)*((n+1)/(2*n))+(1/2)*sigma_hat**2
    
        d1 = ((math.log(S/K) + (mu + (1/2)*sigma_hat**2))*T)/(sigma_hat*math.sqrt(T))
        d2 = d1 - sigma_hat*math.sqrt(T)
    
        N_d1_P = norm.cdf(d1)
        N_d2_P = norm.cdf(d2)

        # the closed-form formulas for geometric Asian call option 
        Call = e**(-(r*T))*(S*e**(mu*T)*N_d1_P - K*N_d2_P)
        
        return Call

    # for put option
    def PutGeoAsian(self):
        
        S, sigma, r, T, K, n = self.S, self.sigma, self.r, self.T, self.K, self.n
    
        sigma_hat = sigma*math.sqrt(((n + 1)*(2*n + 1))/(6*n**2))
        mu = (r - (1/2)*sigma**2)*((n+1)/(2*n))+(1/2)*sigma_hat**2
        
        d1 = ((math.log(S/K) + (mu + (1/2)*sigma_hat**2))*T)/(sigma_hat*math.sqrt(T))
        d2 = d1 - sigma_hat*math.sqrt(T)
        
        N_d1_N = norm.cdf(-d1)
        N_d2_N = norm.cdf(-d2)
        
        # the closed-form formulas for geometric Asian put option 
        Put = e**(-(r*T))*(K*N_d2_N - S*e**(mu*T)*N_d1_N)
        
        return Put
    