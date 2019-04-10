#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[10]:
class BiTreeAmericanOption():

    def BiTreeAmericanOption(self, S0, sigma, r, T, K, N, option = 'call'):
    
        #S0: the spot price of asset S(0)
        #K: strike price
        #T: time to maturity (in years)
        #N: number of steps 
        #r: risk-free interest rate
        #sigma: volatility of underlying asset
        #option: option type (call or put)
    
        #deltt: delta_t
        deltat = float(T)/N
        u = np.exp(sigma * np.sqrt(deltat))
        d = np.exp(-sigma * np.sqrt(deltat))
        #p: probability
        p = (np.exp(r * deltat) - d) / (u - d)
        #DF: discount factor
        DF = np.exp(-r * deltat)
    
        #to work with vector we need to init the arrays using numpy
        fs =  np.asarray([0.0 for i in range(N + 1)])    
        #we need the stock tree for calculations of expiration values
        fs2 = np.asarray([(S0 * u**j * d**(N - j)) for j in range(N + 1)])
        #we vectorize the strikes as well so the expiration check will be faster
        fs3 =np.asarray( [float(K) for i in range(N + 1)])
    
        # Compute the leaves, f_{N, j}
        if option == 'call':
            fs[:] = np.maximum(fs2-fs3, 0.0) 
        if option == 'put':
            fs[:] = np.maximum(fs3-fs2, 0.0) 
    
        #calculate backward the option prices
        for i in range(N-1, -1, -1):
        
            fs[:-1]= DF * (p * fs[1:] + (1-p) * fs[:-1])
            fs2[:]=fs2[:]*u
        
            if option == 'call':
                    fs[:]=np.maximum(fs[:],fs2[:]-fs3[:])
            if option == 'put':
                    fs[:]=np.maximum(fs[:],-fs2[:]+fs3[:])
                
        # print fs
        return fs[0]
