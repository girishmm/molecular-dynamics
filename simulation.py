import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

dt = 0.005
mass = 1.0
num_steps = 4000

N = 20
box_size = 10.0
half_box = box_size / 2.0

grid_spacing = box_size / (np.ceil(np.sqrt(N)) + 1)
x_coords = np.arange(grid_spacing, box_size - grid_spacing / 2, grid_spacing)
y_coords = np.arange(grid_spacing, box_size - grid_spacing / 2, grid_spacing)

initial_positions = []
for x in x_coords:
    for y in y_coords:
        initial_positions.append([x, y])
        if len(initial_positions) == N:
            break
    if len(initial_positions) == N:
        break

positions = np.array(initial_positions)
positions += np.random.uniform(-0.05, 0.05, positions.shape)

velocities = np.random.uniform(-0.05, 0.05, (N, 2))
velocities -= np.mean(velocities, axis=0)

def lennard_jones_potential(r, A=10.0, B=10.0):
    r6 = r**6
    r12 = r6 * r6
    V = A / r12 - B / r6
    F = (12 * A / (r12 * r)) - (6 * B / (r6 * r))
    return V, F

def harmonic_potential(r, k=5.0, r_eq=1.12):
    V = 0.5 * k * (r - r_eq)**2
    F = -k * (r - r_eq)
    return V, F

def morse_potential(r, De=1.0, a=2.0, r_eq=1.10):
    V = De * (1 - np.exp(-a * (r - r_eq)))**2
    F = -2 * De * a * (1 - np.exp(-a * (r - r_eq))) * np.exp(-a * (r - r_eq))
    return V, F

def compute_forces(positions, box_size):
    N = len(positions)
    forces = np.zeros((N, 2))
    total_potential_energy = 0.0

    r_min_threshold = 0.5

    for i in range(N):
        for j in range(i + 1, N):
            dx = positions[j, 0] - positions[i, 0]
            dy = positions[j, 1] - positions[i, 1]

            dx -= box_size * round(dx / box_size)
            dy -= box_size * round(dy / box_size)

            r = np.sqrt(dx**2 + dy**2)

            if r < r_min_threshold:
                r = r_min_threshold


            V_LJ, F_LJ = lennard_jones_potential(r)
            V_harmonic, F_harmonic = harmonic_potential(r)
            V_morse, F_morse = morse_potential(r)

            V_total_pair = V_LJ + V_harmonic + V_morse
            F_total_pair = F_LJ + F_harmonic + F_morse # Sum the magnitudes of forces

            total_potential_energy += V_total_pair

            fx = F_total_pair * (dx / r)
            fy = F_total_pair * (dy / r)

            forces[i, 0] += fx
            forces[i, 1] += fy
            forces[j, 0] -= fx
            forces[j, 1] -= fy

    return total_potential_energy, forces

def verlet_step(positions, velocities, accelerations, dt, box_size):
    positions_new = positions + velocities * dt + 0.5 * accelerations * dt**2
    positions_new = positions_new % box_size

    _, forces_new = compute_forces(positions_new, box_size)
    accelerations_new = forces_new / mass

    velocities_new = velocities + 0.5 * (accelerations + accelerations_new) * dt

    return positions_new, velocities_new, accelerations_new

def simulate(positions, velocities):
    positions_history = []
    kinetic_energies = []
    potential_energies = []
    total_energies = []

    PE, forces = compute_forces(positions, box_size)
    accelerations = forces / mass

    for step in range(num_steps):
        positions, velocities, accelerations = verlet_step(positions, velocities, accelerations, dt, box_size)

        PE, _ = compute_forces(positions, box_size)

        positions_history.append(positions.copy())
        KE = 0.5 * mass * np.sum(velocities ** 2)
        kinetic_energies.append(KE)
        potential_energies.append(PE)
        total_energies.append(KE + PE)

    return np.array(positions_history), np.array(kinetic_energies), np.array(potential_energies), np.array(total_energies)

def plot_trajectory(positions_history, name, box_size):
    N = positions_history.shape[1]
    plt.figure(figsize=(7, 7))
    plt.scatter(positions_history[-1, :, 0], positions_history[-1, :, 1], s=50, c='blue', alpha=0.8, edgecolors='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.xlim(0, box_size)
    plt.ylim(0, box_size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f'{name}_final_positions.png')
    plt.close()

def plot_energy(time, kinetic, potential, total, name):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(time, kinetic, label='Kinetic Energy', color='blue', alpha=0.8)
    ax.plot(time, potential, label='Potential Energy', color='orange', alpha=0.8)
    ax.plot(time, total, label='Total Energy', color='green', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('Energy')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f'{name}_energy.png')
    plt.close()

def animate_trajectory(positions, name, box_size, fps=20, frame_skip=5):
    num_steps, num_particles, _ = positions.shape
    fig, ax = plt.subplots(figsize=(7, 7))

    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_aspect('equal', adjustable='box')

    colors = plt.cm.jet(np.linspace(0, 1, num_particles))
    scatter = ax.scatter(positions[0, :, 0], positions[0, :, 1], c=colors, s=60, edgecolors='black', zorder=5)

    animated_positions = positions[::frame_skip]

    def init():
        scatter.set_offsets(np.empty((num_particles, 2)))
        return [scatter]

    def update(frame):
        current_positions = animated_positions[frame]
        scatter.set_offsets(current_positions)
        return [scatter]

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)

    ani = animation.FuncAnimation(fig, update, frames=len(animated_positions),
                                  init_func=init, blit=True, interval=20)

    output_filename = f'{name}_trajectory.mp4'
    print(f"Saving animation to {output_filename}...")
    try:
        ani.save(output_filename, writer=writer)
        print(f"Animation saved as {output_filename}")
    except Exception as e:
        print(f"Error saving animation: {e}")
    plt.close(fig)

time = np.arange(0, num_steps * dt, dt)
name = 'N_simulation'

print("Starting simulation...")
positions, KE, PE, TE = simulate(positions, velocities)

print("Generating plots and animation...")
plot_trajectory(positions, name, box_size)
plot_energy(time, KE, PE, TE, name)
animate_trajectory(positions, name, box_size)

print("\nSimulation complete.")
