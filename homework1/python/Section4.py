omega = np.linspace(1*(2*np.pi)/60, 11400*(2*np.pi)/60, 11400)
rpm = omega*60/(2*np.pi)

P_peak = np.zeros_like(omega)
C_peak = np.zeros_like(omega)
P_nom = np.zeros_like(omega)
C_nom = np.zeros_like(omega)

# Before reaching base rotation speed, torque is constant at maximum value, then
# the power becomes constant after base rotation speed
for i in range(len(omega)):
  if omega[i] <= (P_1p/C_max):
    P_peak[i] = C_max*omega[i]
  else:
    P_peak[i] = P_1p
C_peak = P_peak/omega

# The base speed should be kept beween nominal & peak regimes, so a new torque
# value should be determined by knowing omega_b
C_max_nom = P_1n/omega_b
for j in range(len(omega)):
  if omega[j] <= (P_1n/C_max_nom):
    P_nom[j] = C_max_nom*omega[j]
  else:
    P_nom[j] = P_1n
C_nom = P_nom/omega

# For the next steps, it is more consistent to use nominal regime rather than
# peak one. However, sometimes the 2 of them will be compared


''' TRACTIVE FORCES'''
# Speed vector corresponding to the whole range of motor rotation speed
v_ms_t = (omega*R_e)/i_gear
v_kmh_t = v_ms_t*3.6

# Traction force and power
F_t = (eta_t * C_nom * i_gear)/R_e
P_t = F_t * v_ms

F_t_peak = (eta_t * C_peak * i_gear)/R_e
P_t_peak = F_t_peak * v_ms

''' NET FORCES'''
F_net = F_t - F_RES0
P_net = P_t - P_RES0

F_net5 = F_t - F_RES5
P_net5 = P_t - P_RES5

F_net10 = F_t - F_RES10
P_net10 = P_t - P_RES10

'''ACCELERATION CAPABILITY'''
m_e = m_curb*(1.04 + (J_mot/(m_curb*R_e**2))*i_gear**2) #effective mass

pos = F_net10>0
F_net10_pos = F_net10[pos]

accel_capa = m_e/F_net

accel_capa5 = m_e/F_net5

accel_capa10 = m_e/F_net10_pos
v_acc10 = v_kmh_t[pos]