#!/usr/bin/env python3
"""
Analyze thermodynamic output from LAMMPS NVT simulation
Benchmark Task: BENCH-T1-002
"""

import numpy as np

# Read thermodynamic data
data = []
with open('thermo_data.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('step') or not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            try:
                step = int(parts[0])
                temp = float(parts[1])
                data.append((step, temp))
            except ValueError:
                continue

data = np.array(data)
steps = data[:, 0]
temps = data[:, 1]

# Find initial and final temperatures
initial_temp = temps[0]
final_temp = temps[-1]

# Get data for last 5000 steps (steps 5100-10000 in our case)
# We output every 100 steps, so last 5000 steps = last 50 data points
last_half_mask = steps > 5000
temps_last_half = temps[last_half_mask]

avg_temp_last_half = np.mean(temps_last_half)
std_temp_last_half = np.std(temps_last_half)

print("=" * 60)
print("LAMMPS NVT Simulation Analysis - Argon at Triple Point")
print("=" * 60)
print()
print("Simulation Parameters:")
print(f"  Target temperature: 94.4 K")
print(f"  Thermostat: Nosé-Hoover (damping = 100 fs)")
print(f"  Total steps: 10,000")
print(f"  Timestep: 1 fs")
print()
print("Temperature Analysis:")
print("-" * 40)
print(f"  Initial temperature:    {initial_temp:.2f} K")
print(f"  Final temperature:      {final_temp:.2f} K")
print()
print(f"  Statistics over last 5000 steps:")
print(f"    Number of samples:    {len(temps_last_half)}")
print(f"    Average temperature:  {avg_temp_last_half:.2f} K")
print(f"    Standard deviation:   {std_temp_last_half:.2f} K")
print(f"    Min temperature:      {np.min(temps_last_half):.2f} K")
print(f"    Max temperature:      {np.max(temps_last_half):.2f} K")
print()

# Expected fluctuation for NVT ensemble
# δT/T = 1/√(3N/2) for canonical ensemble
N = 256
expected_fluctuation = 94.4 / np.sqrt(3 * N / 2)
print(f"  Expected T fluctuation (theory): {expected_fluctuation:.2f} K")
print(f"  Measured T fluctuation:          {std_temp_last_half:.2f} K")
print()

# Check if temperature control is working
deviation = abs(avg_temp_last_half - 94.4)
if deviation < 2:
    print("  ✓ Temperature control: EXCELLENT (deviation < 2 K)")
elif deviation < 5:
    print("  ✓ Temperature control: GOOD (deviation < 5 K)")
else:
    print("  ⚠ Temperature control: NEEDS IMPROVEMENT")
print()
print("=" * 60)
