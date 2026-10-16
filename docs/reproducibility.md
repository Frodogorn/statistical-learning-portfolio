# Reproduction guide

## Environment

Use Python 3.11 or newer and install `requirements.txt` in a fresh virtual environment. The presentation was inspected with Python 3.13; `environment-observed.txt` records the locally available scientific package versions, not a recovered lockfile for every historical run.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv/Scripts/Activate.ps1
```

```bash
# Linux or macOS
source .venv/bin/activate
```

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Open each notebook with a fresh Python kernel and execute cells in order. Air Quality locates the CSV from either the repository root or the notebooks directory. Other notebooks use simulated data.

## Saved outputs and randomness

The displayed outputs and exported figures come from the original notebooks, except the HMC and variational-inference notebooks, re-executed with a fixed seed (see their headers). Their historical execution counters were cleared because they do not certify sequential execution. The original stochastic notebooks do not consistently fix random seeds. Re-execution can produce different figures, timings and estimates. The MLP examples preserve their original `random_state=42`.

Validation runs do not overwrite the saved experimental outputs. See [validation record](validation.md) for the exact checks performed.

## Computational cost

| Notebook | Execution considerations |
| --- | --- |
| Air Quality | Multiple kernel grids, neural-network sweeps and Kernel SHAP. Full execution can take a long time and uses parallel grid search. |
| Random-variable simulation | The original Box-Muller timing uses 10 million pairs; Marsaglia includes a scalar rejection loop. |
| Rare-event estimation | Direct Gaussian simulation uses 100 million draws; the final Pareto run uses 50 million. Several arrays are allocated together. |
| Gaussian Bayes | Small conjugate example. |
| Metropolis/MALA | Gaussian examples are small; the posterior section combines 50,000 observations and thousands of proposals and can be memory-intensive. |
| EM | Several small, repeated mixture fits. |
| HMC | Fourteen 500-iteration HMC chains plus Metropolis and MALA baselines, with automatic differentiation; about one to two minutes on a laptop. |
| Variational inference | Eleven CAVI runs on 1,000 points and a 30,000-step Metropolis chain; about one minute. |

You can reduce sample sizes for a quick local exploration, but such a run will not reproduce the displayed historical values. The provided smoke check does exactly this in memory and reports its scope explicitly.

## Repository checks

```bash
python scripts/validate.py
python scripts/smoke_check.py
```

`validate.py` uses the Python standard library to parse all notebooks and source files and inspect local Markdown links. `smoke_check.py` executes the existing completed cells with bounded sampling sizes. It does not execute the full Air Quality grid search and does not establish the statistical validity of the study.
