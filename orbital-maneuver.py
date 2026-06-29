import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

G = 6.674e-11
M_earth = 5.972e24

R1 = 6.771e6 # low earth orbit 400 km above earth (meters)
R2 = 4.216e7 # Geostationary Orbit  (35786 km above earth) (meters)

V1 = np.sqrt(G * M_earth / R1)
V2 = np.sqrt(G * M_earth / R2)

# Hohmann transfer velocities 
V_transfer1 = np.sqrt(G * M_earth * (2/R1 - 1/(R1+R2)))
V_transfer2 = np.sqrt(G * M_earth * (2/R1 - 1/(R1+R2)))

# Delta-V
dV1 = V_transfer1 - V1
dV2 = V2 - V_transfer2
total_dV = abs(dV1) + abs(dV2)

print(f"V1 (LEO): {V1:.0f} m/s")
print(f"V2 (GEO): {V2:.0f} m/s")
print(f"Delta-V1: {dV1:.0f} m/s")
print(f"Delta-V2: {dV2:.0f} m/s")
print(f"Total Delta-V: {total_dV:.0f} m/s")


fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor("black")
ax.set_xlim(-5e7, 5e7)
ax.set_ylim(-5e7, 5e7)
ax.set_aspect("equal")

earth = plt.Circle((0, 0), 6.371e6, color = "blue", zorder = 5)
ax.add_patch(earth)


theta = np.linspace(0, 2 * np.pi, 1000)
ax.plot(R1*np.cos(theta), R1*np.sin(theta), "g--", linewidth=1, label = "LEO")
ax.plot(R2*np.cos(theta), R2*np.sin(theta), "r--", linewidth=1, label = "GEO")


satellite, = ax.plot([], [], "o", color="yellow", markersize=8, zorder=6)


t_orbit1 = np.linspace(0, 2*np.pi, 500)
t_transfer = np.linspace(0, np.pi, 250)
t_orbit2 = np.linspace(np.pi, 3*np.pi, 500)


positions_x = []
positions_y = []

# Phase1 - LEO
for t in t_orbit1:
    positions_x.append(R1 * np.cos(t))
    positions_y.append(R1 * np.sin(t))

    # Phase2 - Hohmann transfer ellipse
a = (R1 + R2) / 2
for t in t_transfer:
    x = a * np.cos(t) - (a - R1)
    y = R2 * np.sin(t) * np.sqrt(1 - ((a-R1)/a)**2) * (R1/a)
    positions_x.append(x)
    positions_y.append(y)

# Phase3 - GEO
for t in t_orbit2:
    positions_x.append(R2 * np.cos(t))
    positions_y.append(R2 * np.sin(t))


def animate(frame):
    satellite.set_data([positions_x[frame]], [positions_y[frame]])
    return satellite,


ax.legend(loc="upper right", facecolor="black", labelcolor="white")
ax.set_title("Hohmann Transfer Orbit", color="white")
fig.patch.set_facecolor("black")


total_frames = len(positions_x)
ani = animation.FuncAnimation(fig, animate, frames=total_frames, interval=10, blit=True)
plt.show()