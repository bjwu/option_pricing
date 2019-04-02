"""
Implement the Monte Carlo method with control variate technique for arithmetic Asian call/put options.
# @Author  :  Wu Bijia
"""
from scipy.stats import norm
import numpy as np


class MCArithAsianOption:
    """
    Args:
        s0: Origin asset price
        sigma: Volatility
        r: Risk free rate
        T: Time to maturity
        K: Strike price
        n: The number of paths in the Monte Carlo simulation
        option_type: 'call' or 'put'
        ctrl_var: Using control variate or not
    """
    def __init__(self, s0=None, sigma=None, r=0, T=0, K=None,
                 n=0, option_type=None, ctrl_var=False ):

        assert option_type == 'call' or option_type == 'put'
        self.s0 = s0
        self.sigma = sigma
        self.r = r
        self.T = T
        self.K = K
        self.n = n
        self.option_type = option_type
        self.ctrl_var = ctrl_var

    """
    Args:
        num_randoms: The number of random variable in Mente Carlo Process
    """
    def pricing(self, num_randoms=1000):

        n = self.n
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

        arithPayoff = [0] * num_randoms
        geoPayoff = [0] * num_randoms

        for i in range(num_randoms):

            Z = np.random.normal(0, 1, n)
            Spath = [0] * n
            growthFactor = drift * np.exp(self.sigma*np.sqrt(dt)*Z[0])
            Spath[0] = self.s0 * growthFactor

            for j in range(1, n):
                growthFactor = drift * np.exp(self.sigma*np.sqrt(dt)*Z[j])
                Spath[j] = Spath[j-1] * growthFactor

            ### Arithmatic mean
            arithMean = np.mean(Spath)
            arithPayoff[i] = np.exp(-self.r*self.T) * max(arithMean-self.K, 0)

            ### Geometric mean
            geoMean = np.exp((1/n) * sum(np.log(Spath)))
            geoPayoff[i] = np.exp(-self.r*self.T) * max(geoMean-self.K, 0)

            if i % 50 == 0:
                print('[INFO] The {}th random variables have been generated.'.format(i))

        ### Standard Mente Carlo
        Pmean = np.mean(arithPayoff)
        Pstd = np.std(arithPayoff)
        confmc = (Pmean-1.96*Pstd/np.sqrt(num_randoms), Pmean+1.96*Pstd/np.sqrt(num_randoms))

        if not self.ctrl_var:
            print('The {} option price using Mente Carlo WITHOUT control variate is {}'.format(self.option_type, Pmean))
            return Pmean
        else:
            ### Control Variate
            conXY = np.mean(np.multiply(arithPayoff, geoPayoff)) - (np.mean(arithPayoff) * np.mean(geoPayoff))
            theta = conXY / np.var(geoPayoff)

            ### Control variate version
            if self.option_type == 'call':
                geo_call = np.exp(-self.r * self.T) * (self.s0 * np.exp(muT) * N1 - self.K * N2)
                Z = arithPayoff + theta * (geo_call - geoPayoff)

            elif self.option_type == 'put':
                geo_put = np.exp(-self.r * self.T) * (self.K * N2_ - self.s0 * np.exp(muT) * N1_)
                Z = arithPayoff + theta * (geo_put - geoPayoff)

            Zmean = np.mean(Z)
            Zstd = np.std(Z)
            confmc = (Zmean-1.96 * Zstd / np.sqrt(num_randoms), Zmean+1.96*Zstd/np.sqrt(num_randoms))
            print('The {} option price using Mente Carlo WITH control variate is {}'.format(self.option_type, Zmean))
            return Zmean


if __name__ == '__main__':
    option = MCArithAsianOption(s0=100, sigma=0.3, r=0.05, T=3, K=100,
                 n=100000, option_type='put', ctrl_var=True)
    option.pricing(num_randoms=100)

