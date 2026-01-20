#!/usr/bin/env python3
"""
Analysis script for liquid argon MD simulation
Reproducing Rahman 1964 diffusion coefficient calculation

This script:
1. Reads MSD data from LAMMPS output
2. Performs linear regression on the linear regime
3. Calculates diffusion coefficient using Einstein relation: D = MSD/(6t)
4. Estimates statistical uncertainty
5. Compares to Rahman's published value

Reference: Rahman, A. (1964). Phys. Rev. 136, A405-A411.
Expected D = 2.43 × 10⁻⁵ cm²/s
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

# =============================================================================
# Read MSD data from LAMMPS output
# =============================================================================

def read_msd_data(filename):
    """Read MSD data from LAMMPS fix ave/time output"""
    time_steps = []
    msd_values = []

    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                time_steps.append(int(parts[0]))
                msd_values.append(float(parts[1]))

    return np.array(time_steps), np.array(msd_values)

# =============================================================================
# Unit conversion
# =============================================================================

# LAMMPS "real" units:
# - Time: femtoseconds (fs)
# - Length: Angstroms (Å)
#
# Diffusion coefficient:
# - MSD in Å²
# - Time in fs
# - D = MSD / (6 * t) has units Å²/fs
#
# Convert to cm²/s:
# 1 Å = 10⁻⁸ cm → 1 Å² = 10⁻¹⁶ cm²
# 1 fs = 10⁻¹⁵ s
# D [cm²/s] = D [Å²/fs] × 10⁻¹⁶/10⁻¹⁵ = D [Å²/fs] × 10⁻¹

def angstrom2_per_fs_to_cm2_per_s(D):
    """Convert diffusion coefficient from Å²/fs to cm²/s"""
    return D * 1e-1

# =============================================================================
# Linear fitting for diffusion coefficient
# =============================================================================

def linear_func(x, a, b):
    """Linear function: y = a*x + b"""
    return a * x + b

def calculate_diffusion_with_uncertainty(timesteps, msd, dt_fs=2.0, skip_initial=10, skip_final=0):
    """
    Calculate diffusion coefficient from MSD using Einstein relation.

    Parameters:
    -----------
    timesteps : array
        LAMMPS timesteps
    msd : array
        Mean square displacement in Å²
    dt_fs : float
        Timestep in femtoseconds
    skip_initial : int
        Number of initial points to skip (ballistic regime)
    skip_final : int
        Number of final points to skip (poor statistics)

    Returns:
    --------
    D : float
        Diffusion coefficient in cm²/s
    D_err : float
        Standard error of D
    slope : float
        Slope of MSD vs time (Å²/fs)
    intercept : float
        Intercept of fit
    r_squared : float
        R² value of fit
    """
    # Convert timesteps to time in fs
    time_fs = timesteps * dt_fs

    # Select fitting region (skip ballistic and noisy regimes)
    n_points = len(time_fs)
    start_idx = skip_initial
    end_idx = n_points - skip_final if skip_final > 0 else n_points

    time_fit = time_fs[start_idx:end_idx]
    msd_fit = msd[start_idx:end_idx]

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_fit, msd_fit)

    # Diffusion coefficient from Einstein relation: MSD = 6*D*t
    # slope = d(MSD)/dt = 6D
    # D = slope / 6
    D_angstrom2_per_fs = slope / 6.0

    # Convert to cm²/s
    D_cm2_per_s = angstrom2_per_fs_to_cm2_per_s(D_angstrom2_per_fs)

    # Error propagation: σ_D = σ_slope / 6
    D_err_angstrom2_per_fs = std_err / 6.0
    D_err_cm2_per_s = angstrom2_per_fs_to_cm2_per_s(D_err_angstrom2_per_fs)

    return D_cm2_per_s, D_err_cm2_per_s, slope, intercept, r_value**2, time_fit, msd_fit

# =============================================================================
# Block averaging for uncertainty estimation
# =============================================================================

def block_averaging_uncertainty(time_fs, msd, n_blocks=5):
    """
    Estimate uncertainty using block averaging method.

    Divide data into n_blocks and calculate D for each block.
    """
    n_points = len(time_fs)
    block_size = n_points // n_blocks

    D_values = []

    for i in range(n_blocks):
        start = i * block_size
        end = (i + 1) * block_size if i < n_blocks - 1 else n_points

        # Need at least 10 points per block
        if end - start < 10:
            continue

        time_block = time_fs[start:end]
        msd_block = msd[start:end]

        # Rebase time to start from 0
        time_block = time_block - time_block[0]

        # Only fit points after initial ballistic regime (first 5 points)
        if len(time_block) > 5:
            slope, _, _, _, _ = stats.linregress(time_block[5:], msd_block[5:])
            D_block = angstrom2_per_fs_to_cm2_per_s(slope / 6.0)
            D_values.append(D_block)

    if len(D_values) > 1:
        D_mean = np.mean(D_values)
        D_std = np.std(D_values, ddof=1)  # Sample std
        D_sem = D_std / np.sqrt(len(D_values))  # Standard error of mean
        return D_mean, D_sem, D_std
    else:
        return None, None, None

# =============================================================================
# Main analysis
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DIFFUSION COEFFICIENT ANALYSIS")
    print("Reproduction of Rahman 1964 - Liquid Argon MD")
    print("=" * 70)
    print()

    # Read data
    timesteps, msd = read_msd_data("msd.dat")

    # Timestep in fs
    dt_fs = 2.0
    time_fs = timesteps * dt_fs
    time_ps = time_fs / 1000.0

    print(f"Data points: {len(timesteps)}")
    print(f"Time range: 0 to {time_ps[-1]:.1f} ps")
    print(f"Final MSD: {msd[-1]:.2f} Å²")
    print()

    # Calculate diffusion coefficient
    # Skip first 10 points (ballistic regime, ~2 ps)
    D, D_err, slope, intercept, r2, time_fit, msd_fit = \
        calculate_diffusion_with_uncertainty(timesteps, msd, dt_fs=dt_fs, skip_initial=10)

    print("LINEAR FIT RESULTS:")
    print("-" * 50)
    print(f"Fitting region: {time_fit[0]/1000:.2f} to {time_fit[-1]/1000:.2f} ps")
    print(f"Slope (d(MSD)/dt): {slope:.6f} Å²/fs")
    print(f"Intercept: {intercept:.2f} Å²")
    print(f"R² value: {r2:.6f}")
    print()

    # Alternative uncertainty using block averaging
    D_block, D_block_err, D_block_std = block_averaging_uncertainty(time_fs, msd, n_blocks=5)

    print("DIFFUSION COEFFICIENT:")
    print("-" * 50)
    print(f"From linear fit:      D = ({D*1e5:.4f} ± {D_err*1e5:.4f}) × 10⁻⁵ cm²/s")
    if D_block is not None:
        print(f"From block averaging: D = ({D_block*1e5:.4f} ± {D_block_err*1e5:.4f}) × 10⁻⁵ cm²/s")
    print()

    # Comparison with Rahman's value
    D_rahman = 2.43e-5  # cm²/s
    D_exp = 2.86e-5     # cm²/s (experimental)

    print("COMPARISON WITH LITERATURE:")
    print("-" * 50)
    print(f"Rahman (1964):        D = 2.43 × 10⁻⁵ cm²/s")
    print(f"Experimental:         D = 2.86 × 10⁻⁵ cm²/s")
    print(f"This work:            D = ({D*1e5:.2f} ± {D_err*1e5:.2f}) × 10⁻⁵ cm²/s")
    print()

    deviation_rahman = (D - D_rahman) / D_rahman * 100
    deviation_exp = (D - D_exp) / D_exp * 100

    print(f"Deviation from Rahman: {deviation_rahman:+.1f}%")
    print(f"Deviation from exp:    {deviation_exp:+.1f}%")
    print()

    # Check if result is within acceptable range
    if abs(deviation_rahman) < 20:
        print("✓ Result is in excellent agreement with Rahman (1964)")
    else:
        print("⚠ Result deviates significantly from Rahman (1964)")

    print()
    print("=" * 70)

    # ==========================================================================
    # PLOTTING
    # ==========================================================================

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: MSD vs Time with linear fit
    ax1 = axes[0]

    # Plot all data
    ax1.plot(time_ps, msd, 'b-', linewidth=1.5, label='MSD data', alpha=0.8)

    # Plot linear fit
    fit_line = slope * time_fit + intercept
    ax1.plot(time_fit/1000, fit_line, 'r--', linewidth=2,
             label=f'Linear fit (D = {D*1e5:.2f} × 10⁻⁵ cm²/s)')

    # Mark fitting region
    ax1.axvline(time_fit[0]/1000, color='gray', linestyle=':', alpha=0.5)
    ax1.axvline(time_fit[-1]/1000, color='gray', linestyle=':', alpha=0.5)

    ax1.set_xlabel('Time (ps)', fontsize=12)
    ax1.set_ylabel('MSD (Å²)', fontsize=12)
    ax1.set_title('Mean Square Displacement vs Time\n(Liquid Argon at 94.4 K)', fontsize=12)
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, time_ps[-1])
    ax1.set_ylim(0, None)

    # Plot 2: Comparison bar chart
    ax2 = axes[1]

    categories = ['This Work', 'Rahman (1964)', 'Experimental']
    values = [D * 1e5, D_rahman * 1e5, D_exp * 1e5]
    errors = [D_err * 1e5, 0, 0]  # Only our result has error bars
    colors = ['steelblue', 'forestgreen', 'darkorange']

    bars = ax2.bar(categories, values, yerr=errors, capsize=5, color=colors,
                   edgecolor='black', linewidth=1.5, alpha=0.8)

    ax2.set_ylabel('D (× 10⁻⁵ cm²/s)', fontsize=12)
    ax2.set_title('Diffusion Coefficient Comparison', fontsize=12)
    ax2.set_ylim(0, max(values) * 1.3)
    ax2.grid(True, axis='y', alpha=0.3)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f'{val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    plt.savefig('diffusion_plot.png', dpi=150, bbox_inches='tight')
    print("Plot saved as 'diffusion_plot.png'")
    plt.close()

    # ==========================================================================
    # Save numerical results to file
    # ==========================================================================

    with open('analysis_results.txt', 'w') as f:
        f.write("DIFFUSION COEFFICIENT ANALYSIS RESULTS\n")
        f.write("=" * 50 + "\n\n")
        f.write("System: 864 Argon atoms at 94.4 K, ρ = 1.374 g/cm³\n")
        f.write("Reference: Rahman, A. (1964). Phys. Rev. 136, A405.\n\n")
        f.write("RESULTS:\n")
        f.write(f"Diffusion coefficient: D = ({D*1e5:.4f} ± {D_err*1e5:.4f}) × 10⁻⁵ cm²/s\n")
        f.write(f"R² of linear fit: {r2:.6f}\n\n")
        f.write("COMPARISON:\n")
        f.write(f"Rahman (1964): D = 2.43 × 10⁻⁵ cm²/s\n")
        f.write(f"Experimental:  D = 2.86 × 10⁻⁵ cm²/s\n")
        f.write(f"Deviation from Rahman: {deviation_rahman:+.1f}%\n")
        f.write(f"Deviation from exp:    {deviation_exp:+.1f}%\n")

    print("Results saved to 'analysis_results.txt'")
