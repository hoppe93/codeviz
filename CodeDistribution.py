
import numpy as np
import scipy.special as sp

class CodeDistribution:
    
    def __init__(self, f, y, delta, Nxi, ntheta=500):
        Np = len(y)
        self.origf = np.reshape(f, (Np, Nxi))
        thetas = np.linspace(np.pi, np.pi/2, ntheta)

        self.xis = np.cos(thetas)
        self.f = np.zeros((ntheta, Np))
        self.p = np.multiply(delta, y)

        transp = np.transpose(self.origf)
        for i in range(0, ntheta-1):
            p = np.polynomial.legendre.legval(self.xis[i], transp)
            self.f[i,:] = p

        """
        for n in range(0, Nxi-1):
            Ln = sp.legendre(n)
            for i in range(0, ntheta-1):
                l = Ln(self.xis[i])
                for j in range(0, len(y)-1):
                    self.f[i,j] = self.f[i,j] + self.origf[j,n] * l

        """
        self.P, self.XI = np.meshgrid(self.p, self.xis)
