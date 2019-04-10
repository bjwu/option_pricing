"""
Implement the Monte Carlo method with control variate technique for arithmetic Asian call/put options.
# @Author  :  Wu Bijia
"""
from scipy.stats import norm
import numpy as np


class MCArithAsianOption:
    """
    Args:
        s0: Spot Price of Asset S(0)
        sigma: Implied Volatility
        r: Risk-free Interest Rate
        T: Time to Maturity (in years)
        K: Strike
        n: the number of observation times for the option
        m: the number of paths in the Monte Carlo simulation
        option_type: 'call' or 'put'
        ctrl_var: Using control variate or not
    """
    def __init__(self, s0=None, sigma=None, r=0, T=0, K=None,
                 n=100, m=100000, option_type=None, ctrl_var=False):

        assert option_type == 'call' or option_type == 'put'
        self.s0 = s0
        self.sigma = sigma
        self.r = r
        self.T = T
        self.K = K
        self.n = n
        self.m = m
        self.option_type = option_type
        self.ctrl_var = ctrl_var

    def pricing(self):

        n = self.n
        m = self.m
        dt = self.T / n
        sigsqT = self.sigma**2 * self.T * (n+1) * (2*n+1) / (6*n**2)
        muT = 0.5*sigsqT + (self.r - 0.5*(self.sigma**2))*self.T*(n+1)/(2*n)

        d1 = (np.log(self.s0/self.K) + (muT + 0.5*sigsqT))/np.sqrt(sigsqT)
        d2 = d1 - np.sqrt(sigsqT)

        N1 = norm.cdf(d1)
        N2 = norm.cdf(d2)

        N1_ = norm.cdf(-d1)
        N2_ = norm.cdf(-d2)

        drift = np.exp((self.r - 0.5*self.sigma**2)*dt)

        arithPayoff_call = [0] * m
        arithPayoff_put = [0] * m 
        geoPayoff_call = [0] * m
        geoPayoff_put = [0] * m   

        for i in range(m):

            Z = np.random.normal(0, 1, n)
            Spath = [0] * n
            growthFactor = drift * np.exp(self.sigma*np.sqrt(dt)*Z[0])
            Spath[0] = self.s0 * growthFactor

            for j in range(1, n):
                growthFactor = drift * np.exp(self.sigma*np.sqrt(dt)*Z[j])
                Spath[j] = Spath[j-1] * growthFactor

            ### Arithmatic mean
            arithMean = np.mean(Spath)
            arithPayoff_call[i] = np.exp(-self.r*self.T) * max(arithMean-self.K, 0)
            arithPayoff_put[i] = np.exp(-self.r*self.T) * max(self.K-arithMean, 0) 

            ### Geometric mean
            geoMean = np.exp((1/n) * sum(np.log(Spath)))
            geoPayoff_call[i] = np.exp(-self.r*self.T) * max(geoMean-self.K, 0)
            geoPayoff_put[i] = np.exp(-self.r*self.T) * max(self.K-geoMean, 0)   

            if i % 50 == 0:
                print('[INFO] The {}th random variables have been generated.'.format(i))

        ### Standard Mente Carlo
        Pmean_call = np.mean(arithPayoff_call)
        Pstd_call = np.std(arithPayoff_call)
        
        Pmean_put = np.mean(arithPayoff_put)
        Pstd_put = np.std(arithPayoff_put)
        
        # the 95% confidence interval for call option without control variate
        confmc_call = (Pmean_call-1.96*Pstd_call/np.sqrt(m), Pmean_call+1.96*Pstd_call/np.sqrt(m))
        # the 95% confidence interval for put option without control variate
        confmc_put = (Pmean_put-1.96*Pstd_put/np.sqrt(m), Pmean_put+1.96*Pstd_put/np.sqrt(m))

        if not self.ctrl_var and self.option_type == 'call':
            
            print('The {} option price using Mente Carlo WITHOUT control variate is {}'.format(self.option_type, Pmean_call))
            return Pmean_call, confmc_call
        
        elif not self.ctrl_var and self.option_type == 'put':
            
            print('The {} option price using Mente Carlo WITHOUT control variate is {}'.format(self.option_type, Pmean_put))
            return Pmean_put, confmc_put
        
        else:
            ### Control Variate
            conXY_call = np.mean(np.multiply(arithPayoff_call, geoPayoff_call)) - (np.mean(arithPayoff_call) * np.mean(geoPayoff_call))
            conXY_put = np.mean(np.multiply(arithPayoff_put, geoPayoff_put)) - (np.mean(arithPayoff_put) * np.mean(geoPayoff_put))
            theta_call = conXY_call / np.var(geoPayoff_call)
            theta_put = conXY_put / np.var(geoPayoff_put) # for put

            ### Control variate version
            if self.option_type == 'call':
                geo_call = np.exp(-self.r * self.T) * (self.s0 * np.exp(muT) * N1 - self.K * N2)
                Z = arithPayoff_call + theta_call * (geo_call - geoPayoff_call)

            elif self.option_type == 'put':
                geo_put = np.exp(-self.r * self.T) * (self.K * N2_ - self.s0 * np.exp(muT) * N1_)
                Z = arithPayoff_put + theta_put * (geo_put - geoPayoff_put)

            Zmean = np.mean(Z)
            Zstd = np.std(Z)
            confmc = (Zmean-1.96 * Zstd / np.sqrt(m), Zmean+1.96*Zstd/np.sqrt(m))
            print('The {} option price using Mente Carlo WITH control variate is {}'.format(self.option_type, Zmean))
            return Zmean, confmc

'''
if __name__ == '__main__':
    option = MCArithAsianOption(s0=100, sigma=0.3, r=0.05, T=3, K=100,
                 n=100, m=100000, option_type='put', ctrl_var=True)
    option.pricing()
'''