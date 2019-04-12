"""
Implement the Monte Carlo method with control variate technique for arithmetic mean basket call/put options.
For the arithmetic mean basket options, we only need to consider a basket with two assets.
# @Author  :  Wu Bijia
"""
from scipy.stats import norm
import numpy as np
from CFGeoBasketOption import CFGeoBasketOption


class MCArithBasketOption(CFGeoBasketOption):
    """
    Args:
        s0_1: Spot Price of Asset 1
        s0_2: Spot Price of Asset 2
        sigma_1: Volatility 1
        sigma_2: Volatility 2
        r: Risk-free Interest Rate
        T: Time to Maturity (in years)
        K: Strike
        rho: the correlation
        option_type: 'call' or 'put'
        m: The number of path in the Monte Carlo simulation
        ctrl_var: Using control variate or not
    """
    def __init__(self, s0_1=None, s0_2=None, sigma_1=None, sigma_2=None,
                 r=0, T=0, K=None, rho=None, option_type=None, m=100000,
                 ctrl_var=False):

        CFGeoBasketOption.__init__(self, s0_1, s0_2, sigma_1, sigma_2, r, T,
                                    K, rho, option_type)
        self.m = m
        self.ctrl_var = ctrl_var

    """
    Args:
        num_randoms: The observation time in Mente Carlo Process
    """
    def pricing(self, num_randoms=50):

        # n is number of baskets in the Mean Basket Options
        n = 2
        m = self.m
        dt = self.T / num_randoms
        # Calculate SigmaBg Square
        sigsqT = (self.sigma_1**2+2*self.sigma_1*self.sigma_2*self.rho+self.sigma_2**2)/(n**2)
        # mu multiply by T
        muT = (self.r - 0.5*((self.sigma_1**2+self.sigma_2**2)/n) + 0.5*sigsqT)*self.T

        Bg = [0] * m
        Ba = [0] * m
        Bg0 = np.sqrt(self.s0_1 * self.s0_2)

        d1 = (np.log(Bg0/self.K) + (muT + 0.5*sigsqT*self.T))/(np.sqrt(sigsqT)*np.sqrt(self.T))
        d2 = d1 - np.sqrt(sigsqT)*np.sqrt(self.T)

        N1 = norm.cdf(d1)
        N2 = norm.cdf(d2)

        N1_ = norm.cdf(-d1)
        N2_ = norm.cdf(-d2)

        drift_1 = np.exp((self.r - 0.5 * self.sigma_1 ** 2) * self.T)
        drift_2 = np.exp((self.r - 0.5 * self.sigma_2 ** 2) * self.T)

        arithPayoff = [0] * m
        geoPayoff_call = [0] * m
        geoPayoff_put = [0] * m

        for i in range(m):

            #Bg[0] = Bg0
            #Ba[0] = 0.5*(Spath_1[0]+Spath_2[0])

            # fix the initial state
            s = i
            np.random.seed(s)
            Z_1 = np.random.normal(0, 1, 1)
            # mu = 0, sigma = 1, X1, X2 are i.i.d
            # Y1 = mu + sigmaX1, Y2 = mu + sigma(rhoX1 + sqrt(1-rho**2*X2))
            Z_2 = self.rho*Z_1+np.sqrt(1-self.rho**2)*np.random.normal(0, 1, 1)
            S_1 = self.s0_1*drift_1 * np.exp(self.sigma_1 * np.sqrt(self.T) * Z_1)
            S_2 = self.s0_2*drift_2 * np.exp(self.sigma_2 * np.sqrt(self.T) * Z_2)
            
            '''
            Spath_1 = [0]*50
            Spath_2 = [0]*50
            Spath_1[0] =  self.s0_1*drift_1 * np.exp(self.sigma_1 * np.sqrt(self.T) * Z_1_o)
            for j in range(1, 50):
                
                Z_1 = np.random.normal(0, 1, 1)
                Z_2 = np.random.normal(0, 1, 1)
                Spath_1[0] = self.s0_1*drift_1 * np.exp(self.sigma_1 * np.sqrt(self.T) * Z_1)
                Spath_2[0] = self.s0_2*drift_2 * np.exp(self.sigma_2 * np.sqrt(self.T) * Z_2)
                growthFactor_1 = drift_11 * np.exp(self.sigma_1 * np.sqrt(dt) * Z_1)
                growthFactor_2 = drift_21 * np.exp(self.sigma_2 * np.sqrt(dt) * Z_2)
                Spath_1[j] = Spath_1[j - 1] * growthFactor_1
                Spath_2[j] = Spath_2[j - 1] * growthFactor_2
                #Bg[j] = np.sqrt(Spath_1[j]*Spath_2[j])
            '''
            
            Ba[i] = (1/n)*(S_1 + S_2)
            ### Geometric mean
            geoMean = np.exp((1/n) * (np.log(S_1) + np.log(S_2)))
            geoPayoff_call[i] = np.exp(-self.r*self.T)*max(geoMean-self.K, 0)
            geoPayoff_put[i] = np.exp(-self.r*self.T)*max(self.K-geoMean, 0)

            if i % 50 == 0:
                print('[INFO] The {} path has been generated.'.format(i))
                 
            if self.option_type == "call":
                
                arithPayoff[i] = Ba[i] - self.K
                if arithPayoff[i] > 0:
                    arithPayoff[i] = np.exp(-self.r*self.T)*arithPayoff[i]
                else:
                    arithPayoff[i] = 0

            elif self.option_type == "put":

                arithPayoff[i] = self.K - Ba[i]
                if arithPayoff[i] > 0:
                    arithPayoff[i] = np.exp(-self.r*self.T)*arithPayoff[i]
                else:
                    arithPayoff[i] = 0
                
        ### Standard Mente Carlo
        Pmean = float(np.mean(arithPayoff))
        Pstd = np.std(arithPayoff)
        confmc = (Pmean-1.96*Pstd/np.sqrt(m), Pmean+1.96*Pstd/np.sqrt(m))

        if not self.ctrl_var:
            print('The {} basket option price using Mente Carlo WITHOUT control variate is {}'.format(self.option_type, Pmean))
            print('The confidence interval is {}'.format(confmc))
            return Pmean, confmc
        else:
            ### Control Variate
            conXY_call = np.mean(np.multiply(arithPayoff, geoPayoff_call)) - (np.mean(arithPayoff) * np.mean(geoPayoff_call))
            theta_call = conXY_call / np.var(geoPayoff_call)
            conXY_put = np.mean(np.multiply(arithPayoff, geoPayoff_put)) - (np.mean(arithPayoff) * np.mean(geoPayoff_put))
            theta_put = conXY_put / np.var(geoPayoff_put)

            ### Control variate version
            if self.option_type == 'call':
                # implement the closed-from formula for Geometric Mean Basket Call Option
                geo_call = np.exp(-self.r * self.T) * (Bg0 * np.exp(muT) * N1 - self.K * N2)
                Z = arithPayoff + theta_call * (geo_call - geoPayoff_call)

            elif self.option_type == 'put':
                # implement the closed-from formula for Geometric Mean Basket Put Option
                geo_put = np.exp(-self.r * self.T) * (self.K * N2_ - Bg0 * np.exp(muT) * N1_)
                Z = arithPayoff + theta_put * (geo_put - geoPayoff_put)

            Zmean = np.mean(Z)
            Zstd = np.std(Z)
            confmc = (Zmean-1.96 * Zstd / np.sqrt(m), Zmean+1.96*Zstd/np.sqrt(m))
            print('The {} option price using Mente Carlo WITH control variate is {}'.format(self.option_type, Zmean))
            print('The confidence interval is {}'.format(confmc))
            return Zmean, confmc

if __name__ == '__main__':
    option = MCArithBasketOption(s0_1=100, s0_2=100, sigma_1=0.3, sigma_2=0.3,
                 r=0.05, T=3, K=100, rho=0.5, option_type='call', m=100000,
                 ctrl_var=True)
    option.pricing(num_randoms=50)
