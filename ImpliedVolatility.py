"""
Implement Volatility Calculator for European Call/Put Options with Newton Raphson Method.
# @Author: Zhang Weibin  
"""

import math
from BSEuroOption import BSEuroOption
from math import e
from scipy.stats import norm

class ImpliedVolatility(BSEuroOption):
    
    def __init__(self, S, r, q, T, K, V, t = 0):
        
        # the Spot Price of Asset S(0)
        self.S = S
        # the Risk-free Interest Rate
        self.r = r
        # the Repo Rate q
        self.q = q
        # Time to Maturity (in year)
        self.T = T
        # Current Time (in year)
        self.t = t
        # Strike
        self.K = K
        # The Option Premium
        self.V = V
    
    # set a initial sigma value for Newton Raphson Method
    def SigmaInit(self):
        
        S, K, q, T, t, r = self.S, self.K, self.q, self.T, self.t, self.r 
        SigmaInit = math.sqrt(2*abs((math.log(S/K)+(r-q)*(T-t))/(T-t)))
        return SigmaInit
    
    def CallAndPutDerivative(self, S, K, q, T, r, sigma, t = 0):
        
        d1 = (math.log(S/K) + (r-q)*(T-t))/(sigma*math.sqrt(T-t)) + (1/2)*sigma*math.sqrt(T-t)
        diff_N_d1 = norm.pdf(d1)
        Dev = S*e**(-q*(T-t))*math.sqrt(T-t)*diff_N_d1
        return Dev 
    
    def CallVolatility(self, m_max = 100, tolerance = 1e-8):
        
        # m_max: the max iteration steps for Newton Raphson Method
        # tolerance: tolerance for the Newton Raphson Method
        # the initial iteration step for Newton Raphson Method 
        m = 1
        # create initial sigma value as the input for Newton Raphson Method
        SigmaInit = self.SigmaInit()
        # set initial sigma value as the input for Newton Raphson Method
        SigmaNewCall = SigmaInit
        S, r, q, T, K, V = self.S, self.r, self.q, self.T, self.K, self.V  
        
        SigmaDiff = abs((BSEuroOption().CallOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall))
        SigmaNewCall = SigmaNewCall - (BSEuroOption().CallOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall)
        
        while(SigmaDiff > tolerance and m < m_max):
            
            SigmaDiff = abs((BSEuroOption().CallOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall))
            SigmaNewCall = SigmaNewCall - (BSEuroOption().CallOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall)
            m += 1
            
        return SigmaNewCall
    
    def PutVolatility(self, n_max = 100, tolerance = 1e-8):
        
        # n_max: the max iteration steps for Newton Raphson Method
        # tolerance: tolerance for the Newton Raphson Method
        # the initial iteration step for Newton Raphson Method
        n = 1
        # create initial sigma value as the input for Newton Raphson Method
        SigmaInit = self.SigmaInit()
        # set initial sigma value as the input for Newton Raphson Method
        SigmaNewCall = SigmaInit
        S, r, q, T, K, V = self.S, self.r, self.q, self.T, self.K, self.V
        
        SigmaDiff = abs((BSEuroOption().PutOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall))
        SigmaNewCall = SigmaNewCall - (BSEuroOption().PutOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall)
        
        while(SigmaDiff > tolerance and n < n_max):
            
            SigmaDiff = abs((BSEuroOption().PutOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall))
            SigmaNewCall = SigmaNewCall - (BSEuroOption().PutOption(S = S, sigma = SigmaNewCall, r = r, q = q, T = T, K = K) - V)/self.CallAndPutDerivative(S = S, K = K, q = q, T = T, r = r, sigma = SigmaNewCall)
            n += 1
            
        return SigmaNewCall
    