import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Simulation parameters
dt = 0.01
num_steps = 1000
mass = 1.0

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

# Step definition
def euler_step(y, h, f):
    return y + h*f

def simulate(potential_func):

    x, y = 1.5, 0.0
    vx, vy = 0.0, 1.0

    positions = []
    kinetic_energies = []
    potential_energies = []
    total_energies = []

    for _ in range(num_steps):
        r = np.sqrt(x**2 + y**2)
        V, F_mag = potential_func(r)

        # Compute force
        fx = F_mag * (x / r)
        fy = F_mag * (y / r)

        # Compute acceleration
        ax = fx / mass
        ay = fy / mass

        # Take step
        vx = euler_step(vx, dt, ax)
        vy = euler_step(vy, dt, ay)

        x = euler_step(x, dt, vx)
        y = euler_step(y, dt, vy)

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

potentials = {
    'Harmonic': harmonic_potential,
    'Lennard-Jones': lennard_jones_potential,
    'Morse': morse_potential
}

for name, potential_func in potentials.items():
    positions, KE, PE, TE = simulate(potential_func)

    plot_trajectory(positions, name)
    plot_energy(time, KE, PE, TE, name)
    animate_trajectory(positions, name)
