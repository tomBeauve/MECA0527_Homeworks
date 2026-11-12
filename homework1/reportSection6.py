import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("WLTP.xlsx", skiprows=0, decimal=",")


##########
# Car parameters

g = 9.81
# Car dimensions & weight
length = 3.999  # m
width = 1.775  # m
height = 1.597  # m
wheelbase = 2.57  # m
m_curb = 1195  # kg
m_driver = 75  # kg
m_tot = m_curb + m_driver


# ROlling resistance properties
SCx = 2.38 * 0.29  # m^2, for standard version
rho_air = 1.23  # kg/m^3
R_e = 0.339  # to refine
f_rr_0 = 0.008
f_rr_2 = 0.4e-7 * (3.6**2)  # from (kmh)^2 to (m/s)^2

# drivetrain properties
eta_t = 0.95
i_tot = 9.665

# engine properties
P_max = 75e3  # W
P_max_regen = 50e3  # W, max regen power
T_max = 250  # Nm
P_max_boost = 125e3  # W
T_max_boost = T_max * P_max_boost / P_max
# just scale T_max_regen so that omega_base remains the same in regen
T_max_regen = T_max * P_max_regen/P_max
omega_base = P_max/T_max  # rad/s
RPM_max = 11400
omega_max = RPM_max * 2*np.pi/60
J_m = 0.025  # kg * m^2

battery_capacity_gross = 22.6  # kWh
# usable battery, there is a safety buffer
battery_capacity = 18.8
alpha_regen = 0.3

# to compute the effective mass
gamma = 1.04 + (J_m/(m_curb * R_e)) * i_tot**2

# I convert the coefficients from 1/rpm to 1/rad/s to use with omega

a1 = 8.079e-1  # [-]
a2 = 1.827e-5 * (60/(2*np.pi))  # [1/(rad/s)]
a3 = 6.760e-4  # [1/Nm]
a4 = -1.087e-9 * (60/(2*np.pi))**2  # [1/(rad/s)^2]
a5 = 2.434e-9 * (60/(2*np.pi))  # [1/Nm /(rad/s)]
a6 = -1.864e-6  # [1/nm^2]


# I normalize the coefficients by the max omega & torque
# so that i can scale for regen efficiency
a1_norm = a1
a2_norm = a2 * omega_max
a3_norm = a3 * T_max
a4_norm = a4 * omega_max**2
a5_norm = a5 * omega_max * T_max
a6_norm = a6 * T_max**2


########
# Drivetrain efficiency map function
#########


def efficiency_motor(omega, T):
    """The efficiency of the electric motor using the Golverk formula

    Parameters:
    - omega : angular velocity of motor [rad/s] (scalar or numpy array)
    - T : torque of motor [Nm] (scalar or numpy array)

    Returns:
    - eta: efficiency of the motor
    """
    # Check if inputs are arrays or sequences
    is_array = isinstance(omega, np.ndarray) or isinstance(T, np.ndarray)

    omega_norm, T_norm = omega / omega_max, T / T_max

    if not is_array:
        # Scalar logic (original behavior)
        if (omega <= omega_base and T > T_max) or (T * omega > P_max):
            return 0.01
        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        return eta  # * eta_t
    else:
        # Vectorized array logic
        omega = np.asarray(omega)
        T = np.asarray(T)

        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        eta = eta  # * eta_t

        # Use element-wise logical operators (& and |) and np.where
        invalid = ((omega <= omega_base) & (T > T_max)) | ((T * omega) > P_max)
        return np.where(invalid, 0.01, eta)


def efficiency_regen(omega, T):

    is_array = isinstance(omega, np.ndarray) or isinstance(T, np.ndarray)

    omega_norm, T_norm = omega / omega_max, T / T_max_regen

    if not is_array:
        # Scalar logic (original behavior)
        if (omega <= omega_base and T > T_max_regen) or (T * omega > P_max_regen):
            return 0.01
        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        return eta  # * eta_t
    else:
        # Vectorized array logic
        omega = np.asarray(omega)
        T = np.asarray(T)

        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        eta = eta  # * eta_t

        # Use element-wise logical operators (& and |) and np.where
        invalid = ((omega <= omega_base) & (T > T_max_regen)) | (
            (T * omega) > P_max_regen)
        return np.where(invalid, 0.01, eta)


#####
# Efficiency map plotting functions
######


def _efficiency_drivetrainPLOT(omega, T):
    """The efficiency of the drivetrain (transmission & electric motor using the Golverk formula)

    Parameters:
    - omega : angular velocity of motor [rad/s] (scalar or numpy array)
    - T : torque of motor [Nm] (scalar or numpy array)

    Returns:
    - eta: efficiency of the motor
    """
    # Check if inputs are arrays or sequences

    is_array = isinstance(omega, np.ndarray) or isinstance(T, np.ndarray)

    omega_norm, T_norm = omega / omega_max, T / T_max

    if not is_array:
        # Scalar logic (original behavior)
        if (omega <= omega_base and T > T_max) or (T * omega > P_max):
            return np.nan
        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        return eta  # * eta_t
    else:
        # Vectorized array logic
        omega = np.asarray(omega)
        T = np.asarray(T)

        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        eta = eta  # * eta_t

        # Use element-wise logical operators (& and |) and np.where
        invalid = ((omega <= omega_base) & (T > T_max)) | ((T * omega) > P_max)
        return np.where(invalid, np.nan, eta)


def _efficiency_regenPLOT(omega, T):

    is_array = isinstance(omega, np.ndarray) or isinstance(T, np.ndarray)

    omega_norm, T_norm = omega / omega_max, T / T_max_regen

    if not is_array:
        # Scalar logic (original behavior)
        if (omega <= omega_base and T > T_max_regen) or (T * omega > P_max_regen):
            return np.nan
        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        return eta  # * eta_t
    else:
        # Vectorized array logic
        omega = np.asarray(omega)
        T = np.asarray(T)

        eta = a1_norm + a2_norm * omega_norm +\
            a3_norm * T_norm + a4_norm * (omega_norm ** 2) +\
            a5_norm * T_norm * omega_norm + a6_norm * (T_norm ** 2)
        eta = eta  # * eta_t

        # Use element-wise logical operators (& and |) and np.where
        invalid = ((omega <= omega_base) & (T > T_max_regen)) | (
            (T * omega) > P_max_regen)
        return np.where(invalid, np.nan, eta)


def plot_efficiency_map(fig, ax):
    torques = np.linspace(0.0, T_max, 1000)
    omegas = np.linspace(5.0, omega_max, 1000)
    T_mesh, Omega_mesh = np.meshgrid(torques, omegas, indexing='ij')

    # Evaluate efficiency across the 2D mesh arrays directly
    eta_grid = _efficiency_drivetrainPLOT(Omega_mesh, T_mesh)

    # Convert omega to RPM for the main plot axis
    RPM_mesh = Omega_mesh * 60.0 / (2.0 * np.pi)

    # --- Plotting ---

    # Set vmin=0 and vmax=100 so the colorbar represents true percentage bounds
    contour = ax.contourf(RPM_mesh, T_mesh, eta_grid * 100.0,
                          levels=10, cmap='bone')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label('Efficiency [%]')

    contour_lines = ax.contour(
        RPM_mesh, T_mesh, eta_grid * 100.0, levels=10, colors='black', linewidths=1)
    ax.clabel(contour_lines, inline=True, fmt='%.1f%%', fontsize=9)

    ax.set_xlabel('Motor Speed [RPM]')
    ax.set_ylabel('Motor Torque [Nm]')
    ax.grid(True, linestyle='--', alpha=0.3)


def plot_regen_efficiency_map(fig, ax):
    torques = np.linspace(0.0, T_max_regen, 1000)
    omegas = np.linspace(5.0, omega_max, 1000)
    T_mesh, Omega_mesh = np.meshgrid(torques, omegas, indexing='ij')

    # Evaluate efficiency across the 2D mesh arrays directly
    eta_grid = _efficiency_regenPLOT(Omega_mesh, T_mesh)

    # Convert omega to RPM for the main plot axis
    RPM_mesh = Omega_mesh * 60.0 / (2.0 * np.pi)

    # --- Plotting ---

    # Set vmin=0 and vmax=100 so the colorbar represents true percentage bounds
    contour = ax.contourf(RPM_mesh, -T_mesh, eta_grid * 100.0,
                          levels=10, cmap='bone')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label('Efficiency [%]')

    contour_lines = ax.contour(
        RPM_mesh, -T_mesh, eta_grid * 100.0, levels=10, colors='black', linewidths=1)
    ax.clabel(contour_lines, inline=True, fmt='%.1f%%', fontsize=9)

    ax.set_xlabel('Motor Speed [RPM]')
    ax.set_ylabel('Motor Torque [Nm]')
    ax.grid(True, linestyle='--', alpha=0.3)


def plot_efficiency_map_combined(fig, ax):

    # ==================================
    # Motor mode efficiency map plotting
    # ==================================

    torques = np.linspace(0.0, T_max, 1000)
    omegas = np.linspace(5.0, omega_max, 1000)
    T_mesh, Omega_mesh = np.meshgrid(torques, omegas, indexing='ij')

    # Evaluate efficiency across the 2D mesh arrays directly
    eta_grid = _efficiency_drivetrainPLOT(Omega_mesh, T_mesh)

    # Convert omega to RPM for the main plot axis
    RPM_mesh = Omega_mesh * 60.0 / (2.0 * np.pi)

    # Set vmin=0 and vmax=100 so the colorbar represents true percentage bounds
    contour = ax.contourf(RPM_mesh, T_mesh, eta_grid * 100.0,
                          levels=10, cmap='bone')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label('Efficiency [%]')

    contour_lines = ax.contour(
        RPM_mesh, T_mesh, eta_grid * 100.0, levels=10, colors='black', linewidths=1)
    ax.clabel(contour_lines, inline=True, fmt='%.1f%%', fontsize=9)

    # ==================================
    # Regen mode efficiency map plotting
    # ==================================

    torques = np.linspace(0.0, T_max_regen, 1000)
    omegas = np.linspace(5.0, omega_max, 1000)
    T_mesh, Omega_mesh = np.meshgrid(torques, omegas, indexing='ij')

    # Evaluate efficiency across the 2D mesh arrays directly
    eta_grid = _efficiency_regenPLOT(Omega_mesh, T_mesh)

    # Convert omega to RPM for the main plot axis
    RPM_mesh = Omega_mesh * 60.0 / (2.0 * np.pi)

    # Set vmin=0 and vmax=100 so the colorbar represents true percentage bounds
    contour = ax.contourf(RPM_mesh, -T_mesh, eta_grid * 100.0,
                          levels=10, cmap='bone')

    contour_lines = ax.contour(
        RPM_mesh, -T_mesh, eta_grid * 100.0, levels=10, colors='black', linewidths=1)
    ax.clabel(contour_lines, inline=True, fmt='%.1f%%', fontsize=9)

    ax.set_xlabel('Motor Speed [RPM]')
    ax.set_ylabel('Motor Torque [Nm]')
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.axhline(0, c="k", lw=4)


fig, ax = plt.subplots(1, 1, figsize=(10, 6))
plot_efficiency_map_combined(fig, ax)


####
# Resistive force function
####
def F_res(v, theta):
    F_rr = (f_rr_0 + f_rr_2 * v**2) * m_tot * g * np.cos(theta)
    F_aero = 0.5 * rho_air * SCx * v**2
    F_slope = m_tot * g * np.sin(theta)

    return F_rr + F_aero + F_slope


def F_acc(m_curb, m_driver, gamma, dv_dt):
    return (gamma * m_curb + m_driver) * dv_dt


# ====================================
# 6A : Consumption @ constant speeds
# ====================================
v = np.array([30, 50, 100, 120]) / 3.6  # velocities to test, kmh to m/s


# Energy consumption per km = F * 1km (J/km) /(1000*3600) (=>kwh/km)
for i in range(len(v)):
    omega = (v[i] / R_e) * i_tot
    torque = (F_res(v[i], 0) * R_e) / (i_tot * eta_t)

    F_mot = (F_res(v[i], 0)) / \
        eta_t / (efficiency_motor(omega, torque) * eta_t)
    energy_kwh_100km = (F_mot * 1000.0 / 36000.0)

    print(
        f"Energy consumption at {v[i] * 3.6:.1f} km/h : {energy_kwh_100km:.3f} (kWh/100km)")

# =======================================
# 6B : Constant speeds curves consumption
# =======================================

v = np.linspace(5, 150, 1000)/3.6  # kmh to m/s
slope_percent = np.array([0, 3, 6])  # they are there to draw multiple curves
slope_angle = np.arctan2(slope_percent, 100)  # = theta in the F_res fct

fig, ax = plt.subplots()

for i in range(len(slope_angle)):

    omega = (v / R_e) * i_tot
    torque = (F_res(v, slope_angle[i]) * R_e) / (i_tot * eta_t)

    F_mot = (F_res(v, slope_angle[i])) / \
        eta_t / efficiency_motor(omega, torque) / eta_t
    ax.plot(v*3.6, F_mot * 1000_00 / (1000*3600),
            label=f"{slope_percent[i]}% slope")

ax.set_xlabel(r"Velocity (km/h)")
plt.ylabel(r"Consumption (kWh/100km)")
ax.set_xlim(0, 150)
ax.legend(loc="best", frameon=True, facecolor="white", edgecolor="none")
plt.grid(alpha=0.5)
plt.tight_layout()
plt.savefig("figures/consumption/constantSpeedConsumption.pdf", dpi=300)
plt.show()


torques = np.linspace(0.0, T_max, 1000)
omegas = np.linspace(5.0, omega_max, 1000)
T_mesh, Omega_mesh = np.meshgrid(torques, omegas, indexing='ij')

# Evaluate efficiency across the 2D mesh arrays directly
eta_grid = _efficiency_drivetrainPLOT(Omega_mesh, T_mesh)

# Convert omega to RPM for the main plot axis
RPM_mesh = Omega_mesh * 60.0 / (2.0 * np.pi)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(9, 6))

plot_efficiency_map(fig, ax)
for i in range(len(slope_angle)):

    omega = (v / R_e) * i_tot
    torque = (F_res(v, slope_angle[i]) * R_e) / (i_tot * eta_t)
    ax.plot(omega * 60/(2*np.pi), torque,
            label=f"{slope_percent[i]}% slope", linewidth=5)

ax.set_xlim(0)
plt.legend()

rpm_to_kmh_factor = (2 * np.pi * R_e * 3.6) / (60 * i_tot)


def rpm_to_kmh(rpm):
    return rpm * rpm_to_kmh_factor


def kmh_to_rpm(kmh):
    return kmh / rpm_to_kmh_factor


# Create the twin top x-axis
secax = ax.secondary_xaxis("top", functions=(rpm_to_kmh, kmh_to_rpm))
secax.set_xlabel("Vehicle Speed (km/h)")

plt.tight_layout()
plt.savefig("figures/consumption/constantSpeedMotorMap.pdf", dpi=300)


#####
# WLTP ANALYSIS
#####


alpha_regen = 1.0


df = pd.read_excel("WLTP.xlsx", skiprows=0, decimal=",")

phase = df['Phase'].to_numpy()[1:]  # string says which phase we are in
total_time = df['Total elapsed time'].to_numpy()[1:]  # [s]
phase_time = df['Phase elapsed time'].to_numpy()[1:]  # [s]
speed = df['WLTC class 3, version 5, vehicle speed'].to_numpy()[1:]  # [km/h]
speed = speed / 3.6  # [m/s]
dv_dt = np.gradient(speed, total_time)
delta_t = 1  # [s]
delta_x = speed * delta_t
E_tot = 0  # J, cumulative


def Power_regen(v, dv_dt):
    """The absolute value of regen power, following chap 5 slide 14 convention
    The way the max regen power is handled is : 
    compute the mechanical power, multiplied by motor efficiency => gives the electrical power delivered to the battery
    then cap this power to the battery at 50kW
    By capping after having computed the efficiency we could apply the efficiency in an extrapolated region (beyond T_max & P_max)
    but if we applied capping onto mechanical power we would never reach the 50kW power delivered to battery
    """

    # net force available for regen (deleration is due partly to f_res)
    F_mot = (F_acc(m_curb, m_driver, gamma, dv_dt) + F_res(v, 0))

    omega = (v / R_e) * i_tot
    torque = abs((F_mot * R_e) / (i_tot * eta_t))
    eta = efficiency_regen(omega, torque) * eta_t

    P_mot = F_mot * v

    if P_mot >= 0:
        return 0.0
    else:
        P_bat = np.abs(P_mot) * eta * alpha_regen
        return min(50000, P_bat)


def Power_consumption(v, dv_dt):
    # tractive force by motor = force to accelerate + to fight road resistance
    F_mot = (F_acc(m_curb, m_driver, gamma, dv_dt) + F_res(v, 0))

    omega = (v / R_e) * i_tot
    torque = abs((F_mot * R_e) / (i_tot * eta_t))
    eta = efficiency_motor(omega, torque) * eta_t

    P_mot = F_mot * v

    if P_mot < 0:
        return 0.0
    else:
        P_bat = np.abs(P_mot) / eta
        return P_bat


p_cons_array = np.zeros(len(total_time))  # array for debug
p_regen_array = np.zeros(len(total_time))  # array for debug
total_distance = np.sum(speed * delta_t)
T_WLTP = np.zeros(len(total_time))
omega_WLTP = np.zeros(len(total_time))

for i in range(len(speed)):
    p_cons_array[i] = Power_consumption(float(speed[i]), float(dv_dt[i]))
    p_regen_array[i] = -Power_regen(float(speed[i]), float(dv_dt[i]))
    E_tot += Power_consumption(speed[i], dv_dt[i]) * delta_t
    E_tot -= Power_regen(speed[i], dv_dt[i]) * delta_t
    omega_WLTP[i] = speed[i] * i_tot/R_e

    F_mot = (F_acc(m_curb, m_driver, gamma, dv_dt[i]) + F_res(speed[i], 0))
    T_WLTP[i] = F_mot * R_e/i_tot


E_tot_kWh = E_tot / 3_600_000.0
total_distance_km = total_distance / 1000.0
WLTP_consumption = (E_tot_kWh / total_distance_km) * 100.0

print(f"Total Energy: {E_tot_kWh:.3f} kWh")
print(f"Total Distance: {total_distance_km:.3f} km")
print(f"WLTP Consumption: {WLTP_consumption:.2f} kWh/100km")
print(f" Autonomy (km) : {battery_capacity / WLTP_consumption * 100}")

# ======================================
# Plot the P vs time of the WLTP Cycle
# ======================================

fig, ax = plt.subplots(1, 1, figsize=(11, 6))

# Primary axis (left) - Power
line1 = ax.plot(total_time, p_cons_array / 1000,
                label="Consumption", color="tab:blue")
line2 = ax.plot(total_time, p_regen_array / 1000,
                label="Regeneration", color="tab:orange")
ax.set_xlabel(r"Elapsed time (s)")
ax.set_ylabel(r"Motor power (kW)")

# Secondary axis (right) - Speed
ax_speed = ax.twinx()
line3 = ax_speed.plot(total_time, speed*3.6,
                      label="vehicle speed", color="tab:green", linestyle="--")
ax_speed.set_ylabel(r"Speed (km/h)")  # update unit as needed

# Combine handles and labels into a single unified legend
lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax.legend(lines, labels, loc="best", frameon=True,
          facecolor="white", edgecolor="none")

ax.set_xlim(0, 450)
ax.set_ylim(-12, 36)
ax_speed.set_ylim(-20, 60)
ax.grid(True, axis='y',  alpha=0.5)
plt.tight_layout()
plt.savefig("figures/consumption/WLTP1PowerSpeed.pdf", dpi=300)

plt.show()


fig, ax = plt.subplots()

# Primary axis (left) - Power
line1 = ax.plot(total_time, p_cons_array / 1000,
                label="Consumption", color="tab:blue")
line2 = ax.plot(total_time, p_regen_array / 1000,
                label="Regeneration", color="tab:orange")
ax.set_xlabel(r"Elapsed time (s)")
ax.set_ylabel(r"Motor power (kW)")

# Secondary axis (right) - Speed

# Combine handles and labels into a single unified legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax.legend(lines, labels, loc="best", frameon=True,
          facecolor="white", edgecolor="none")

ax.set_xlim(0, 450)
ax.set_ylim(-12, 36)
ax.grid(True, axis='y',  alpha=0.5)
plt.savefig("figures/consumption/WLTP1Power.pdf", dpi=300)

plt.show()


# ======================================
# Plot the locations of points (T,omega) along the WLTP cycle
# ======================================

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
plot_efficiency_map_combined(fig, ax)
ax.scatter(omega_WLTP * 60/(2*np.pi), T_WLTP, color="red")
plt.xlim(0)
plt.tight_layout()
plt.savefig("figures/consumption/WLTPLocusMotorMap.pdf", dpi=300)
plt.show()
