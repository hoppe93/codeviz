
import numpy as np
import scipy.special as sp
from Bekefi import Spectrum
from Bremsstrahlung import DSigmaDk

class CodeDistribution:
    
    def __init__(self, f, y, delta, Nxi, ntheta=500):
        Np = len(y)
        self.origf = np.reshape(f, (Nxi, Np))
        thetas = np.linspace(np.pi/2, 0, ntheta)

        self.xis = np.cos(thetas)
        self.f = np.zeros((ntheta, Np))
        self.p = np.multiply(delta, y)

        for i in range(0, ntheta-1):
            p = np.polynomial.legendre.legval(-self.xis[i], self.origf)
            self.f[i,:] = p

        # Normalize
        self.f = np.abs(np.divide(self.f, np.amax(np.amax(self.f))))

        # Compute variable grids
        self.P, self.XI = np.meshgrid(self.p, self.xis)
        self.THETA = np.arccos(self.XI)
        self.PPAR = np.array(np.multiply(self.P, self.XI))
        self.PPERP = np.multiply(self.P, np.sqrt(1 - self.XI**2))

        self.maxp = np.amax(self.p)
        self.maxtheta = np.amax(np.amax(self.THETA))
        self.maxppar = np.amax(np.amax(self.PPAR))
        self.maxpperp = np.amax(np.amax(self.PPERP))

    def getBremsstrahlungWeighting(self, k):
        return DSigmaDk(self.P, self.XI, k)

    def getFullWeighting(self, lambda1, lambda2, magneticField):
        return Spectrum(self.P, self.XI, lambda1, lambda2, magneticField)

    def getParameterMax(self, param='p'):
        if param == 'p': return self.maxp
        elif param == 'pitch': return self.maxtheta
        elif param == 'ppar': return self.maxppar
        elif param == 'pperp': return self.maxpperp
        else:
            raise ValueError('Maximum value of unknown parameter requested: '+param)
