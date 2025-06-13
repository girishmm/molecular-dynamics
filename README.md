# Molecular dynamics

This project is for the Cimulation and Modeling course of the Summer
2025 semester in Uni Koln.

## TO-DO

 - [x] Setup
 - [x] Single particle
  - [x] Newton's equations
  - [x] Potential definitions
  - [x] Euler step
  - [x] Verlet step
  - [ ] Check energy conservation
 - [ ] Multi particle
  - [ ] Random configuration with sufficient particles
 - [ ] Implement damping
 - [ ] Try different time steps
 - [ ] Analyze floating point efficiency
 - [ ] Describe formal scaling wrt N
 - [ ] Improvement based on sparse systems?

## Design decisions:

 - Poetry for project management
 - Animations of dynamics
 - Slide flow (bottom-up):
   - Single particle dynamics
   - Symplectic schemes
   - Scaling to multiple particles

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

<p float="left">
  <img src="./img/single-particle/combined-euler/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-euler/energy.png" width="400" />
</p>

<p float="left">
  <img src="./img/single-particle/combined-verlet/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-verlet/energy.png" width="400" />
</p>

#### Combined (unstable)

By changing A, B in lennard-jones from 1, 1 to 10, 10

<p float="left">
  <img src="./img/single-particle/combined-euler-unstable/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-euler-unstable/energy.png" width="400" />
</p>

<p float="left">
  <img src="./img/single-particle/combined-verlet-unstable/trajectory.gif" width="200" />
  <img src="./img/single-particle/combined-verlet-unstable/energy.png" width="400" />
</p>

### Multi-particle

### With euler step

### With verlet step