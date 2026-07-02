#!/usr/bin/env python3
"""
Generate a synthetic LAMMPS NVT log file for benchmark testing.
Creates realistic thermodynamic data at 94.4 K with equilibration behavior.
"""

import numpy as np
import os

np.random.seed(42)  # For reproducibility

# Simulation parameters
n_steps = 10000
timestep = 0.001  # ps
output_freq = 10  # Every 10 steps
n_atoms = 256
target_temp = 94.4  # K (liquid argon at triple point)

# Generate step numbers
steps = np.arange(0, n_steps + 1, output_freq)
n_points = len(steps)
time = steps * timestep

# Generate temperature with equilibration behavior
# First 2000 steps: equilibrating from ~150K down to 94.4K
# After 2000 steps: stable at 94.4K with natural fluctuations

equilibration_end = 2000  # step number
eq_index = equilibration_end // output_freq

# Equilibration phase: exponential decay from 150K to 94.4K
initial_temp = 150.0
temp_equilibration = target_temp + (initial_temp - target_temp) * np.exp(-np.linspace(0, 5, eq_index))

# Add some noise to equilibration
temp_equilibration += np.random.normal(0, 3, eq_index)

# Production phase: stable temperature with natural NVT fluctuations
# Expected fluctuation for N atoms: σ_T = T * sqrt(2/(3*N-6))
# For 256 atoms: σ_T ≈ 94.4 * sqrt(2/762) ≈ 4.8 K
temp_fluctuation = target_temp * np.sqrt(2.0 / (3 * n_atoms - 6))
temp_production = target_temp + np.random.normal(0, temp_fluctuation, n_points - eq_index)

temperature = np.concatenate([temp_equilibration, temp_production])

# Generate energy data
# Total energy should be approximately constant after equilibration
# with small fluctuations

# Kinetic energy ~ 3/2 * N * k_B * T
# Using reduced units where k_B = 1
kinetic = 1.5 * n_atoms * temperature / 120.0  # Convert to kcal/mol units

# Potential energy: approximately constant after equilibration
pe_target = -850.0  # kcal/mol
pe_equilibration = pe_target + 100 * np.exp(-np.linspace(0, 5, eq_index))
pe_production = pe_target + np.random.normal(0, 5, n_points - eq_index)
potential = np.concatenate([pe_equilibration, pe_production])

# Total energy
total_energy = kinetic + potential

# Pressure data (for NVT, not strictly controlled)
pressure_target = 50.0  # atm
pressure = pressure_target + np.random.normal(0, 20, n_points)
# Add correlation with temperature
pressure += 0.5 * (temperature - target_temp)

# Write LAMMPS log file
output_path = os.path.join(os.path.dirname(__file__), 'lammps_nvt_log.txt')

with open(output_path, 'w') as f:
    # LAMMPS header
    f.write("LAMMPS (29 Aug 2024)\n")
    f.write("OMP_NUM_THREADS environment is not set. Defaulting to 1 thread. (src/comm.cpp:98)\n")
    f.write("  using 1 OpenMP thread(s) per MPI task\n")
    f.write("Reading data file ...\n")
    f.write("  orthogonal box = (0.0 0.0 0.0) to (34.8388 34.8388 34.8388)\n")
    f.write(f"  1 by 1 by 1 MPI processor grid\n")
    f.write(f"  reading atoms ...\n")
    f.write(f"  {n_atoms} atoms\n")
    f.write("  read_data CPU = 0.001 seconds\n")
    f.write("\n")
    f.write("Neighbor list info ...\n")
    f.write("  update every 1 steps, delay 0 steps, check yes\n")
    f.write("  max neighbors/atom: 2000, page size: 100000\n")
    f.write("  master list distance cutoff = 10.5\n")
    f.write("  ghost atom cutoff = 10.5\n")
    f.write("  binsize = 5.25, bins = 7 7 7\n")
    f.write("\n")
    f.write("Setting up Verlet run ...\n")
    f.write("  Unit style    : real\n")
    f.write("  Current step  : 0\n")
    f.write(f"  Time step     : {timestep}\n")
    f.write("\n")
    f.write("Per MPI rank memory allocation (min/avg/max) = 3.15 | 3.15 | 3.15 Mbytes\n")

    # Thermo output header
    f.write("Step Temp Press PotEng KinEng TotEng\n")

    # Write data
    for i in range(n_points):
        f.write(f"{int(steps[i]):8d} {temperature[i]:10.4f} {pressure[i]:10.4f} {potential[i]:12.4f} {kinetic[i]:12.4f} {total_energy[i]:12.4f}\n")

    # LAMMPS footer
    f.write(f"\nLoop time of 2.34567 on 1 procs for {n_steps} steps with {n_atoms} atoms\n")
    f.write("\n")
    f.write("Performance: 3.683 ns/day, 6.516 hours/ns, 4263.3 timesteps/s\n")
    f.write("99.8% CPU use with 1 MPI tasks x 1 OpenMP threads\n")
    f.write("\n")
    f.write("Total wall time: 0:00:02\n")

print(f"Generated LAMMPS log file: {output_path}")
print(f"  Steps: {n_steps}")
print(f"  Data points: {n_points}")
print(f"  Target temperature: {target_temp} K")
print(f"  Equilibration ends at step: {equilibration_end}")
