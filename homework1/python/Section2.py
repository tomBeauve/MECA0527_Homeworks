import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

''' GEOMETRY & MASS '''
m_curb = 1195 #kg
m_driver = 75 #kg
m = m_curb + m_driver #kg
length = 3.999 #m
width = 1.775 #m
height = 1.597 #m
L = 2.570 #m
b_cg = 0.53*L #m
c_cg = 0.47*L #m
h_cg = 0.49 #m

'''TRANSMISSION & TIRE '''
# 19 inches rim; /39.37 converts inches in meters; 0.7*155 is thickness of tire
D_wheel = (( 19 / 39.37 ) + ( 155 * 0.7 * 2)*10**-3)
eta_t = 0.95 #-
i_gear = 9.665 #-
f0 = 0.008
f2 = 0.4e-7
R_e = 0.339 #m

''' ENGINE '''
P_1p = 125e3 #W
P_1n = 75e3 #W
C_max = 250 #Nm
omega_b = 4800 * (2*np.pi / 60) #rad/s
E_bat = 22.6e3 #Wh
J_mot = 0.025 #kg m^2

''' OTHER '''
g = 9.81 #m/s**2
rho = 1.23 #kg/m**3
S = 2.38 #m**2
C_x = 0.29 #-