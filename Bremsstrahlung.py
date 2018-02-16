
import numpy as np

def DSigmaDk(P, XI, k):
    E0 = np.sqrt(P*P + 1)
    E = E0 - k
    k2 = k*k

    E02 = E0*E0
    E2  = E*E

    p0  = P
    p02 = p0*p0
    p03 = p02*p0

    p  = np.sqrt(E*E-1)
    p2 = p*p
    p3 = p2*p

    p0p = p0*p

    L    = 2*np.log((E0*E  + p0p-1)/k)
    eps0 = np.log((E0+p)/(E0-p0))
    eps  = np.log((E+p)/(E-p))

    S1  = 4.0/3.0
    S1 += 2*E0*E*(p2 + p02)/(p2 * p02)
    S1 += eps0 * E / p03
    S1 += eps * E0 / p3
    S1 += eps*eps0 / p0p

    S2  = 8*E0*E/(3*p0p)
    S2 += k2 * (E02*E2 + p0p*p0p)/(p0p*p0p*p0p)
    
    S3  = eps0*(E0*E + p02)/p03
    S3 +=-eps*(E0*E+p03)/p3
    S3 += 2*k*E0*E/(p0p*p0p)

    S = S1 + L * (S2 + k/(2*p0p) * S3)

    return np.nan_to_num(S)
