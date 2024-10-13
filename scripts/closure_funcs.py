import numpy as np
from scipy.optimize import root_scalar

def S_func(D, D_d, k):
    '''
    Calculates the saturation of a particle given three parameters
    :param D: wet diameter in m
    :param D_d: dry diameter in m
    :param k: kappa
    :return: Saturation
    '''
    A = 2.1e-09 # constant
    
    # cube diameters
    D3 = D**3
    D_d3 = D_d**3

    S = (D3 - D_d3) / (D3 - D_d3 * (1 - k)) * np.exp(A / D)

    return S
def find_critical_ss(D_d, k):
    '''
    Finds the critical s by finding the peak of the saturation curve and subtracting 1
    '''
    Ds = np.arange(D_d, 1000e-9, 1e-9) # range of wet diameters in nm
    return (np.max(S_func(Ds, D_d, k))-1) * 100
def find_d_act(s, k):
    '''
    Finds critical activation diameter by finding the root of the function: (S-1) - s
    :param s: super saturation
    :param k: kappa
    :return: activation diameter in nm
    '''
    
    def find_ss_diff(D_d):
        '''
        Find difference between target ss and calculated s
        '''
        return find_critical_ss(D_d, k) - s

    result = root_scalar(find_ss_diff, bracket=[1e-9, 900e-9])

    return result.root * 1e9
def find_k(s, D_d):
    '''
    Finds critical activation diameter by finding the root of the function: (S-1) - s
    :param s: super saturation
    :param k: kappa
    :return: activation diameter in nm
    '''
    D_d *= 1e-9
    
    def find_ss_diff(k):
        '''
        Find difference between target ss and calculated s
        '''
        return find_critical_ss(D_d, k) - s

    result = root_scalar(find_ss_diff, bracket=[.02, 3.0])

    return result.root