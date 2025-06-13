# Molecular dynamics

This project is for the Simulation and Modeling course of the Summer
2025 semester in Uni Koln.

## TO-DO

 - [x] Setup
 - [x] Single particle
   - [x] Newton's equations
   - [x] Potential definitions
   - [x] Euler step
   - [x] Verlet step
   - [x] Check energy conservation
   - [x] Try different time steps
 - [x] Multi particle with N=20
 - [ ] Implement damping
 - [ ] Analyze floating point efficiency
 - [ ] Describe formal scaling wrt N
 - [ ] Improvement based on sparse systems?

## Design decisions:

 - Poetry for project management
 - Slide flow (bottom-up):
   - Single particle dynamics
   - Symplectic schemes
   - Scaling to multiple particles
 - Single particle
   - potential wrt the origin as no pairwise potentials
 - Animation of dynamics
   - Skip frames in between for faster animation
   - Shorter trail length on scaling particles
 - Multi particle
   - Change parameters to prevent exploding energy/enormous forces
   - Cap force to prevent explosion (removed later)
   - Super small time step for stability (found sweet spot)
   - Bounding box to prevent particles from moving too far

## Setup

To replicate results

 1. Install [poetry](https://python-poetry.org/docs/)
 2. Clone the repo
 3. `$ poetry install`
 4. `$ python simulation.py`

## Outputs

### Single-particle with euler step

#### Only harmonic force field

<p float="left">
  <img src="./img/single-particle/harmonic/trajectory.gif" width="200" />
  <img src="./img/single-particle/harmonic/energy.png" width="400" />
</p>

#### Only lennard-jones force field

<p float="left">
  <img src="./img/single-particle/lennard-jones/trajectory.gif" width="200" />
  <img src="./img/single-particle/lennard-jones/energy.png" width="400" />
</p>

#### Only morse force field

<p float="left">
  <img src="./img/single-particle/morse/trajectory.gif" width="200" />
  <img src="./img/single-particle/morse/energy.png" width="400" />
</p>

#### Combined

##### Euler steps

<p float="left">
  <img src="./img/single-particle/combined-euler/normal/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-euler/normal/energy.png" width="400" />
</p>

#### Verlet steps

<p float="left">
  <img src="./img/single-particle/combined-verlet/normal/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-verlet/normal/energy.png" width="400" />
</p>

#### Combined (unstable)

By changing A, B in lennard-jones from 1, 1 to 10, 10

##### Euler steps

<p float="left">
  <img src="./img/single-particle/combined-euler/unstable/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-euler/unstable/energy.png" width="400" />
</p>

##### Verlet steps

<p float="left">
  <img src="./img/single-particle/combined-verlet/unstable/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-verlet/unstable/energy.png" width="400" />
</p>

#### Combined (small timestep)

By changing timestep from 0.01 to 0.005 and increasing steps to 10000

##### Euler steps

<p float="left">
  <img src="./img/single-particle/combined-euler/small-timestep/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-euler/small-timestep/energy.png" width="400" />
</p>

##### Verlet steps

<p float="left">
  <img src="./img/single-particle/combined-verlet/small-timestep/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-verlet/small-timestep/energy.png" width="400" />
</p>

### Multi-particle

Adding in more particles (say 20), and simulating again with different
parameters to try stability

<p float="left">
  <img src="./img/multi-particle/not-almost/trajectory.gif" width="200" />
  <img src="./img/multi-particle/not-almost/energy.png" width="400" />
</p>

We notice no stable energy despite verlet, why? cause the forces don't
play well together. need prior info on type of molecules to set
parameters accordingly