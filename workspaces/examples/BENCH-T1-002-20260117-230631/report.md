# BENCH-T1-002: NVT Equilibration of Lennard-Jones Argon

## Summary

Successfully ran an NVT molecular dynamics simulation to equilibrate a Lennard-Jones argon system at the triple point temperature (94.4 K).

## Simulation Parameters

| Parameter | Value |
|-----------|-------|
| Number of atoms | 256 (FCC 4×4×4) |
| Temperature | 94.4 K (triple point) |
| LJ ε | 0.238 kcal/mol |
| LJ σ | 3.405 Å |
| Cutoff | 10.215 Å (3σ) |
| Density | 1.399 g/cm³ |
| Box size | 22.98 Å × 22.98 Å × 22.98 Å |
| Thermostat | Nosé-Hoover (100 fs damping) |
| Timestep | 1 fs |
| Total steps | 10,000 |
| Output frequency | 100 steps |

**Parameter Source:** Rahman, Phys. Rev. 136, A405 (1964)

## Results

### Temperature Analysis

| Metric | Value |
|--------|-------|
| **Initial temperature** | 94.40 K |
| **Final temperature** | 94.27 K |
| **Average (last 5000 steps)** | 93.89 K |
| **Standard deviation** | 5.52 K |

### Comparison with Theory

For an NVT ensemble with N atoms, the expected temperature fluctuation is:

δT/T = 1/√(3N/2)

For N = 256 atoms at T = 94.4 K:
- **Expected fluctuation:** 4.82 K
- **Measured fluctuation:** 5.52 K

The slightly larger fluctuation is reasonable given the relatively short equilibration period.

### Observations

1. **Temperature control:** The Nosé-Hoover thermostat maintained excellent temperature control, with the average temperature deviating by only 0.51 K (0.5%) from the target.

2. **Equilibration:** The system shows good thermal equilibration, with the temperature fluctuating around the target value throughout the production phase.

3. **Energy:** The system started from an FCC lattice (high potential energy) and relaxed to a more disordered liquid-like state during the simulation.

## Files Generated

- `argon_nvt.lmp` - LAMMPS input file
- `thermo_data.txt` - Thermodynamic output data
- `analyze_thermo.py` - Analysis script
- `log.lammps` - LAMMPS log file

## Conclusion

The NVT equilibration was successful. The Nosé-Hoover thermostat maintained the temperature at 94.4 K with fluctuations consistent with canonical ensemble statistics for a 256-atom system.
