---
name: quantum-espresso
description: Run Quantum ESPRESSO DFT calculations. Use when asked to perform first-principles calculations, SCF, structural relaxation, band structure, DOS, phonons, or any ab initio quantum mechanical calculation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# Quantum ESPRESSO DFT Calculations

You are executing Quantum ESPRESSO density functional theory calculations.

## CRITICAL: Pseudopotentials Are NOT Pre-Installed

**You must find and download pseudopotentials yourself.**

Pseudopotentials are NOT stored locally. You need to:
1. Determine what elements and functional you need
2. Find appropriate pseudopotentials online
3. Download them to your workspace
4. Reference them in your input file

### How to Acquire Pseudopotentials

**Step 1: Determine requirements**
```
Element(s): Si, O, Li, etc.
Functional: PBE (most common), LDA, PBEsol
Type: NC (norm-conserving), US (ultrasoft), PAW (projector augmented wave)
```

**Step 2: Find pseudopotentials online**

| Source | URL | Best For |
|--------|-----|----------|
| **SSSP** | https://www.materialscloud.org/discover/sssp/table/efficiency | Production - curated, tested |
| **PseudoDojo** | http://www.pseudo-dojo.org/ | High accuracy |
| **QE Library** | https://www.quantum-espresso.org/pseudopotentials | Quick access |
| **Materials Cloud** | https://www.materialscloud.org/ | Various libraries |

**Step 3: Download the files**

Use WebFetch or Playwright:
```
Search for: "silicon PBE pseudopotential SSSP download"
Navigate to SSSP table, find Si row, download .UPF file
```

Example file names:
- `Si.pbe-n-rrkjus_psl.1.0.0.UPF` (PBE, ultrasoft)
- `Si.pz-vbc.UPF` (LDA, norm-conserving)
- `O.pbe-n-kjpaw_psl.1.0.0.UPF` (PBE, PAW)

**Step 4: Save to workspace**
```
workspaces/your-project/pseudo/Si.pbe-n-rrkjus_psl.1.0.0.UPF
```

**Step 5: Note recommended cutoffs**

SSSP provides recommended cutoffs. If not available:
- NC: ecutwfc ~40-80 Ry, ecutrho = 4 × ecutwfc
- US: ecutwfc ~30-50 Ry, ecutrho = 8-12 × ecutwfc
- PAW: ecutwfc ~40-60 Ry, ecutrho = 8-12 × ecutwfc

**Step 6: Reference in input**
```fortran
&CONTROL
    pseudo_dir = './pseudo'
/
ATOMIC_SPECIES
Si  28.0855  Si.pbe-n-rrkjus_psl.1.0.0.UPF
```

---

## Complete Agentic Workflow

### Example: Silicon Band Structure

**Given only:** "Calculate the band structure of silicon"

**You do:**

1. **Get crystal structure**
   ```python
   # From Materials Project
   from mp_api.client import MPRester
   import os
   with MPRester(os.environ.get("MP_API_KEY")) as mpr:
       si = mpr.get_structure_by_material_id("mp-149")
       # Note: a = 5.431 Å, diamond structure, Fd-3m
   ```

2. **Find and download pseudopotential**
   - Search: "silicon PBE pseudopotential SSSP"
   - Navigate to SSSP table
   - Download Si.pbe-n-rrkjus_psl.1.0.0.UPF
   - Note: recommended ecutwfc = 30 Ry

3. **Create SCF input**
   ```fortran
   &CONTROL
       calculation = 'scf'
       prefix = 'si'
       outdir = './tmp'
       pseudo_dir = './pseudo'
   /
   &SYSTEM
       ibrav = 2                   ! FCC
       celldm(1) = 10.26           ! a in Bohr (5.43 Å)
       nat = 2
       ntyp = 1
       ecutwfc = 40.0              ! From SSSP recommendation
       ecutrho = 320.0             ! 8x for US pseudo
   /
   &ELECTRONS
       conv_thr = 1.0d-8
   /
   ATOMIC_SPECIES
   Si  28.0855  Si.pbe-n-rrkjus_psl.1.0.0.UPF

   ATOMIC_POSITIONS crystal
   Si  0.00  0.00  0.00
   Si  0.25  0.25  0.25

   K_POINTS automatic
   8 8 8 0 0 0
   ```

4. **Run SCF**
   ```bash
   /path/to/pw.x < scf.in > scf.out
   ```

5. **Create bands input**
   ```fortran
   &CONTROL
       calculation = 'bands'
       prefix = 'si'
       outdir = './tmp'
       pseudo_dir = './pseudo'
   /
   ...
   K_POINTS crystal_b
   5
   0.5  0.5  0.5   20  ! L
   0.0  0.0  0.0   20  ! Gamma
   0.5  0.0  0.5   20  ! X
   0.5  0.25 0.75  20  ! W
   0.5  0.5  0.5   1   ! L
   ```

6. **Run bands and post-process**
   ```bash
   pw.x < bands.in > bands.out
   bands.x < bands_pp.in > bands_pp.out
   ```

7. **Analyze**
   - Extract band gap from output
   - Si has indirect gap ~0.5 eV (LDA underestimates, exp ~1.1 eV)

---

## Binary Locations

> **Status 2026-07-03:** these builds are ARCHIVED (WSL-era; moved to
> `~/work/archive/gpu-tests-wsl/`, compute M-3) and do **not** run on the
> bare-metal host (MPI runtime rot — `libmpi.so.40` missing; verified
> 2026-07-02, rebase A-04 refuted). Local QE is unavailable until the
> toolchain rebuild (owner queue). `harness.py --verify` reports live state.

**Local GPU-accelerated QE (RTX 5080):**
```bash
# GPU Build (NVHPC-compiled, sm_120)
QE_GPU="/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-gpu/bin"

# CPU Build (GCC/MPI)
QE_CPU="/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-cpu/bin"

# Environment setup for GPU build
QE_ENV="/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/env/setup_nvhpc.sh"
```

### Execution

**CPU (general purpose):**
```bash
/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-cpu/bin/pw.x < input.in > output.out

# With MPI
mpirun -np 4 /home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-cpu/bin/pw.x < input.in > output.out
```

**GPU (RTX 5080 accelerated - recommended for production):**
```bash
# First source NVHPC environment
source /home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/env/setup_nvhpc.sh

# Run GPU-accelerated QE
/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-gpu/bin/pw.x < input.in > output.out

# Or with wrapper variables
$QE_GPU/pw.x < input.in > output.out
```

**Test scripts available:**
```bash
bash /home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/scripts/run_example01_cpu.sh
bash /home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/scripts/run_example01_gpu.sh
```

---

## Calculation Types

| Type | Use For |
|------|---------|
| `scf` | Ground state energy, charge density |
| `relax` | Optimize atomic positions |
| `vc-relax` | Optimize cell + positions |
| `bands` | Band structure (after SCF) |
| `nscf` | DOS, more k-points (after SCF) |

---

## Crystal Structure Input

### Common ibrav Values

| ibrav | Lattice | Example |
|-------|---------|---------|
| 1 | Simple cubic | Po |
| 2 | FCC | Si, Cu, Al |
| 3 | BCC | Fe, W, Na |
| 4 | Hexagonal | Graphite, Ti |
| 0 | General (provide CELL_PARAMETERS) | Any |

### From Materials Project or CIF

If you get a structure from Materials Project or a CIF file:
```fortran
ibrav = 0  ! General cell

CELL_PARAMETERS angstrom
5.431  0.000  0.000
0.000  5.431  0.000
0.000  0.000  5.431

ATOMIC_POSITIONS angstrom
Si  0.000  0.000  0.000
Si  1.358  1.358  1.358
...
```

---

## Cutoff Selection

**Always check pseudopotential recommendations.**

If not available, use these guidelines:

| Pseudo Type | ecutwfc | ecutrho |
|-------------|---------|---------|
| Norm-conserving (NC) | 60-80 Ry | 4 × ecutwfc |
| Ultrasoft (US) | 30-50 Ry | 8-12 × ecutwfc |
| PAW | 40-60 Ry | 8-12 × ecutwfc |

**Test convergence** for production calculations.

---

## K-point Selection

| System | K-grid |
|--------|--------|
| Metals | Dense: 12×12×12 or more |
| Semiconductors | Medium: 6×6×6 to 8×8×8 |
| Insulators | Coarse: 4×4×4 often sufficient |
| Molecules/surfaces | Gamma only or few k-points |

For band structure, use crystal_b with high-symmetry path.

---

## Output Parsing

```bash
# Total energy
grep "!" output.out

# Forces
grep -A 20 "Forces acting" output.out

# Fermi energy
grep "Fermi" output.out

# Band gap (for insulators)
grep "highest occupied" output.out
```

---

## Common Issues

1. **"Error reading pseudo file"**
   - Check pseudo_dir path
   - Verify file was downloaded correctly
   - Check filename matches ATOMIC_SPECIES

2. **Convergence failure**
   - Reduce mixing_beta to 0.3-0.5
   - Increase ecutwfc
   - Check structure for overlapping atoms

3. **Memory issues**
   - Reduce k-points
   - Use disk_io = 'low'

4. **Negative frequencies in phonons**
   - Structure not fully relaxed
   - Reduce forc_conv_thr and re-relax

---

## Key Principle

**Never assume pseudopotentials exist locally.**

Every QE calculation requires you to:
1. Identify the elements
2. Choose appropriate functional
3. Find and download pseudopotentials
4. Note recommended cutoffs
5. Reference correctly in input

If a pseudopotential doesn't exist for your element/functional combination, that's important information to report.

---

## Example: Formation Energy Calculation

**Task:** Calculate formation energy of NaCl

**Complete workflow:**

1. **Get structure**
   ```bash
   # From Materials Project
   mp-22862 → NaCl rock salt structure
   ```

2. **Download pseudopotentials**
   ```
   Na.pbe-spn-kjpaw_psl.1.0.0.UPF (ecutwfc=66 Ry)
   Cl.pbe-n-rrkjus_psl.1.0.0.UPF (ecutwfc=45 Ry)
   ```

3. **Run SCF for NaCl**
   - ecutwfc = 66 Ry (use max of both elements)
   - k-points: 6x6x6 automatic
   - Check convergence

4. **Run reference calculations**
   - Na metal (BCC structure)
   - Cl₂ molecule (in large box)

5. **Calculate formation energy**
   ```
   E_f = E(NaCl) - E(Na_metal) - 0.5*E(Cl₂)
   ```

6. **Compare to literature**
   - Expected: ~-4.2 eV/atom
   - If different by >10%, investigate

**Common pitfall:** Forgetting reference calculations. You need ALL of:
- The compound (NaCl)
- The elemental references (Na metal, Cl₂)

**See also:** `examples/workflows/multi-compound-study.md` for multi-compound studies
