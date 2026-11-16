''' SLOPES '''
theta0 = np.arctan(0) #°
theta5 = np.arctan(0.05) #°
theta10 = np.arctan(0.1) #°

''' SPEED VECTORS '''
v_kmh = np.linspace(0,150,11400) #km/h; 150 is max speed given in litterature
v_ms = v_kmh/3.6

''' GRADING '''
F_grading0 = m*g*np.sin(theta0)
F_grading5 = m*g*np.sin(theta5)
F_grading10 = m*g*np.sin(theta10)

P_grading0 = F_grading0 * v_ms
P_grading5 = F_grading5 * v_ms
P_grading10 = F_grading10 * v_ms

''' AERODYNAMIC DRAG '''
F_AERO = 0.5*rho*S*C_x*(v_ms**2)
P_AERO = F_AERO * v_ms

''' ROLLING RESISTANCE '''
F_RR0  = m*g*(f0 + f2*(v_kmh**2))*np.cos(theta0)
F_RR5  = m*g*(f0 + f2*(v_kmh**2))*np.cos(theta5)
F_RR10 = m*g*(f0 + f2*(v_kmh**2))*np.cos(theta10)

P_RR0  = F_RR0 * v_ms
P_RR5  = F_RR5 * v_ms
P_RR10 = F_RR10 * v_ms

''' TOTAL '''
F_RES0 = F_grading0 + F_AERO + F_RR0
F_RES5 = F_grading5 + F_AERO + F_RR5
F_RES10 = F_grading10 + F_AERO + F_RR10

P_RES0 = P_grading0 + P_AERO + P_RR0
P_RES5 = P_grading5 + P_AERO + P_RR5
P_RES10 = P_grading10 + P_AERO + P_RR10