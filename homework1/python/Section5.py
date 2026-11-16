''' MAXIMUM THEORETICAL SPEED'''
max_iter = 1000
tol = 1e-4
v_0 = 1 # arbitrary choice
A_v = (m*g*np.sin(theta0)) + (m*g*f0*np.cos(theta0))
B_v = (0.5 * rho * S * C_x) + (m*g*(f2/12.96)*np.cos(theta0))

# Computation of v_max_max and ideal gear ratio
i=0
for i in range(max_iter):
  if i==0:
    v_next = ( ((eta_t * P_1n) - (A_v * v_0)) / B_v )**(1/3)
    v_act = v_next

  else :
    v_next = ( ((eta_t * P_1n) - (A_v * v_act)) / B_v )**(1/3)

    if (np.abs(v_next - v_act) < tol ) :
      break
    else:
      v_act = v_next

v_max_max = v_next
print("Theorical greatest maximum speed: ", v_max_max * 3.6, "km/h")
omega_max = 11400 * (2*np.pi/60)
ideal_i = ((omega_max) * R_e) / v_max_max
print("Ideal gear ratio to reach v_max_max: ", ideal_i)

''' MAXIMUM SPEED WITH IMPOSED GEAR RATIO'''
v_act_bis = 150/3.6
for k in range(max_iter):
    omega_max = 11399*(2*np.pi)/60
    omega_k = min(v_act_bis*i_gear/R_e,omega_max)
    P_k = eta_t *C_nom[int(omega_k * 60 / (2*np.pi))] *omega_k

    v_new = ((P_k - (A_v * v_act_bis)) / B_v) ** (1/3)

    if abs(v_new - v_act_bis) < tol:
        break
    v_act_bis = v_new
v_power = v_new
v_rpm = ((11400 * (2*np.pi) / 60) * R_e) / i_gear
v_max = min(v_rpm, v_power)
print(f"{v_power*3.6:.2f}")
print(f"Real greatest maximum speed: {v_max*3.6:.2f} km/h")

mu = np.array([0.2, 0.5, 0.8, 1]) # choice
print("mu=",mu)


'''MAXIMUM SLOPE IN FROM STANSTILL'''
max_slope1 = 100 * ( ((mu * b_cg / L) - f0) / ( 1 - (mu * h_cg / L) ) )
print("Maximum slope in 1st gear : ",max_slope1, "%")

'''MAXIMUM SLOPE AT 80 KM/H '''
F_t_80 = np.interp(80, v_kmh_t, F_t) #need to obtain the value for the exact 80kph speed
F_aero80 = 0.5*rho*S*C_x*(80/3.6)**2
d_80 = (F_t_80 - F_aero80) / (m*g)
max_slope80 = 100 * np.tan( np.arcsin( (d_80 - (f0 * np.sqrt(1 + f0**2 - d_80**2))) / (1 + f0**2) ) )
print("Maximum slope at 80 km/h ",max_slope80, "%")

# VERIFICATION OF TRACTION-LIMITED SLOPE
a = (m*g*(f0+(f2*80**2))) - (mu * m * g * c_cg/L)
b = (m*g) + (mu * m * g * h_cg/L)
max_slope80_adhesion = 100 * np.tan(np.arcsin(-F_aero80/(np.sqrt(a**2 + b**2))) - np.arcsin(a/(np.sqrt(a**2 + b**2))))
print("Verification que la limite de traction est plus grande que la puissance : ", max_slope80_adhesion, ">? 24%")

''' 50 TO 90 km/h'''
v_50_90 = np.linspace(50/3.6, 90/3.6, 100)
F_net_50_90 = np.interp(v_50_90*3.6, v_kmh_t, F_net)
integral_50_90 = np.trapz(1/F_net_50_90,v_50_90)
time_50_90 = m_e * integral_50_90
print("Acceleration time to go from 50 km/h to 90 km/h :", time_50_90, "s")

'''0 TO 100 km/h'''
v_0_100 = np.linspace(1/3.6, 100/3.6, 100)
F_net_0_100 = np.interp(v_0_100*3.6, v_kmh_t, F_net)
integral_0_100 = np.trapz(1/F_net_0_100,v_0_100)
time_0_100 = m_e * integral_0_100
print("Acceleration time to go from 0 km/h to 100 km/h :", time_0_100, "s")

'''0 TO 400m'''
#aucune idee de v_finale => d'abord calculer temps et distance pour 0-150. Si en dessous de 400m =>
#imposer vitesse constante 150km/h pour derniers metres. Sinon, interpoler avant 150km/h
v_0_150 = np.linspace(1/3.6, 150/3.6, 1000)
F_net_0_150 = np.interp(v_0_150 * 3.6, v_kmh_t, F_net)
time_cumul = m_e * cumulative_trapezoid(1 / F_net_0_150, v_0_150, initial=0)
dist_cumul = m_e * cumulative_trapezoid(v_0_150 / F_net_0_150, v_0_150, initial=0)# pour stocker les valeurs dans un vecteur, utile
# pour interpoler après s'il faut
dist_150 = dist_cumul[-1]
time_150 = time_cumul[-1]

if dist_150 >= 400:
    time_400m = np.interp(400, dist_cumul, time_cumul)
    v_400m_kmh = np.interp(400, dist_cumul, v_0_150 * 3.6)
else:
    dist_restante = 400 - dist_150
    time_400m = time_150 + (dist_restante / (150/3.6))
    v_400m_kmh = 150

print("Acceleration time for 0 to 400m :", time_400m, "s")
print("Speed at 400m :", v_400m_kmh, "km/h")
print("Distance at which 150 km/h is reached :", dist_150, "m")