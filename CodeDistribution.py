
import numpy as np
import scipy.special as sp

class CodeDistribution:
    
    def __init__(self, f, y, delta, Nxi, ntheta=500):
        Np = len(y)
        self.origf = np.reshape(f, (Nxi, Np))
        thetas = np.linspace(np.pi, np.pi/2, ntheta)

        self.xis = np.cos(thetas)
        self.f = np.zeros((ntheta, Np))
        self.p = np.multiply(delta, y)

        for i in range(0, ntheta-1):
            p = np.polynomial.legendre.legval(self.xis[i], self.origf)
            self.f[i,:] = p

        # Normalize
        self.f = np.divide(self.f, np.amax(np.amax(self.f)))

        # Compute variable grids
        self.P, self.XI = np.meshgrid(self.p, self.xis)
        self.THETA = np.arccos(self.XI)
        self.PPAR = np.array(np.multiply(self.P, -self.XI))
        self.PPERP = np.multiply(self.P, np.sqrt(1 - self.XI**2))
