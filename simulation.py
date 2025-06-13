import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
dt = 0.01
num_steps = 1000
mass = 1.0

x, y = 1.5, 0.0
vx, vy = 0.0, 1.0

# Potential definitions
def harmonic_potential(r, k=1.0, r_eq=0.0):
    V = 0.5 * k * (r - r_eq)**2
    F = -k * (r - r_eq)
    return V, F

def lennard_jones_potential(r, A=1.0, B=1.0):
    V = A / r**12 - B / r**6
    F = - (12 * A / r**13 - 6 * B / r**7)
    return V, F

def morse_potential(r, De=1.0, a=1.0, r_eq=1.0):
    V = De * (1 - np.exp(-a * (r - r_eq)))**2
    F = -2 * De * a * (1 - np.exp(-a * (r - r_eq))) * np.exp(-a * (r - r_eq))
    return V, F

# Force calculation
def compute_force(x, y):
    r = np.sqrt(x**2 + y**2)
    harmonic_V, harmonic_F_mag = harmonic_potential(r)
    lennard_jones_V, lennard_jones_F_mag = lennard_jones_potential(r)
    morse_V, morse_F_mag = morse_potential(r)

    V = harmonic_V + lennard_jones_V + morse_V
    F_mag = harmonic_F_mag + lennard_jones_F_mag + morse_F_mag

    fx = F_mag * (x / r)
    fy = F_mag * (y / r)

    return V, fx, fy

# Step definitions
def euler_step(x, y, vx, vy, ax, ay, dt):
    vx_new = vx + dt * ax
    vy_new = vy + dt * ay

    x_new = x + dt * vx_new
    y_new = y + dt * vy_new

    return x_new, y_new, vx_new, vy_new

def verlet_step(x, y, vx, vy, ax, ay, dt):
    x_new = x + vx * dt + 0.5 * ax * dt**2
    y_new = y + vy * dt + 0.5 * ay * dt**2

    _, fx_new, fy_new = compute_force(x_new, y_new)
    ax_new = fx_new / mass
    ay_new = fy_new / mass

    vx_new = vx + 0.5 * (ax + ax_new) * dt
    vy_new = vy + 0.5 * (ay + ay_new) * dt

    return x_new, y_new, vx_new, vy_new, ax_new, ay_new


def simulate(x, y, vx, vy, method='euler'):
    positions = []
    kinetic_energies = []
    potential_energies = []
    total_energies = []

    V, fx, fy = compute_force(x, y)
    ax = fx / mass
    ay = fy / mass

    for _ in range(num_steps):
        if method == 'euler':
            x, y, vx, vy = euler_step(x, y, vx, vy, ax, ay, dt)
            V, fx, fy = compute_force(x, y)
            ax = fx / mass
            ay = fy / mass
        elif method == 'verlet':
            x, y, vx, vy, ax, ay = verlet_step(x, y, vx, vy, ax, ay, dt)
            V, _, _ = compute_force(x, y)
        else:
            raise ValueError(f"Unknown integration method: {method}")

        positions.append([x, y])

        KE = 0.5 * mass * (vx**2 + vy**2)
        kinetic_energies.append(KE)
        potential_energies.append(V)
        total_energies.append(KE + V)

    return np.array(positions), np.array(kinetic_energies), np.array(potential_energies), np.array(total_energies)


def plot_trajectory(positions, name):
    plt.figure(figsize=(6, 6))
    plt.plot(positions[:, 0], positions[:, 1], label='Trajectory')
    plt.scatter(positions[0, 0], positions[0, 1], color='green', label='Start', zorder=5)
    plt.scatter(positions[-1, 0], positions[-1, 1], color='red', label='End', zorder=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=True, shadow=True)
    plt.axis('equal')
    plt.grid()
    plt.savefig(f'{name}_trajectory.png')

def plot_energy(time, kinetic, potential, total, name):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(time, kinetic, label='Kinetic Energy', color='blue')
    ax.plot(time, potential, label='Potential Energy', color='orange')
    ax.plot(time, total, label='Total Energy', color='green')
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1),
          ncol=3, fancybox=True, shadow=True)
    ax.grid()
    plt.savefig(f'{name}_energy.png')

def animate_trajectory(positions, name):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(np.min(positions[:, 0]) - 0.5, np.max(positions[:, 0]) + 0.5)
    ax.set_ylim(np.min(positions[:, 1]) - 0.5, np.max(positions[:, 1]) + 0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid()

    particle, = ax.plot([], [], 'ro')
    trail, = ax.plot([], [], 'b-', lw=1)

    def init():
        particle.set_data([], [])
        trail.set_data([], [])
        return particle, trail

    def update(frame):
        particle.set_data([positions[frame][0]], [positions[frame][1]])
        trail.set_data(positions[:frame+1, 0], positions[:frame+1, 1])
        return particle, trail

    ani = animation.FuncAnimation(fig, update, frames=len(positions),
                                  init_func=init, blit=True, interval=20)

    ani.save(f'{name}_trajectory.gif', writer='pillow', fps=50)
    print(f"Animation saved as {name}_trajectory.gif")
    plt.close(fig)

# Run simulation
time = np.arange(0, num_steps * dt, dt)
all_energies = {}
name = 'combined'

positions, KE, PE, TE = simulate(x, y, vx, vy, 'verlet')

plot_trajectory(positions, name)
plot_energy(time, KE, PE, TE, name)
animate_trajectory(positions, name)
