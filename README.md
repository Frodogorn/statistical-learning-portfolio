# Statistical Learning & Computational Statistics

**Gabriel Trabelsi** · M2 IASD · Université Paris Dauphine-PSL

A selection of academic projects connecting statistical methods, Python implementations and experimental analysis: learning from environmental sensors, simulating rare events and fitting latent-variable models.

**[Read the illustrated portfolio (PDF)](report/portfolio.pdf)** · [Read it on GitHub](report/portfolio.md) · [Reproduce the notebooks](docs/reproducibility.md)

## Selected work

| Study | What the code explores | Start here |
| --- | --- | --- |
| **Air-quality estimation** | Data cleaning, chronological splitting, OLS, ridge, RBF kernels, dense networks, feature attribution and residuals | [Notebook](notebooks/01_air_quality.ipynb) |
| **Monte-Carlo simulation** | Inverse transforms, Box-Muller, Marsaglia and correlated Gaussian sampling | [Notebook](notebooks/02_random_variable_simulation.ipynb) |
| **Rare-event estimation** | Direct Monte-Carlo versus importance sampling; Gaussian and Pareto tails | [Notebook](notebooks/03_rare_event_estimation.ipynb) |
| **Bayesian inference** | Gaussian conjugacy, random-walk Metropolis and MALA | [Gaussian update](notebooks/04_gaussian_bayes.ipynb) · [MCMC](notebooks/05_metropolis_and_mala.ipynb) |
| **Latent-variable estimation** | Gaussian-mixture EM, initialization, iteration budget and misspecification | [Notebook](notebooks/06_expectation_maximization.ipynb) |

## From sensor data to model analysis

The Air Quality project estimates four pollutant concentrations using five sensor responses and three weather variables. It compares linear and nonlinear models, then examines hyperparameter sensitivity and prediction errors.

![Selected predictions from the original Air Quality experiment](assets/air_predictions.png)

The original study uses 6,941 complete observations and a chronological 80/20 split. The scores are exploratory rather than a final benchmark; the [methodology notes](docs/methodology.md) detail the limits of the original protocol.

## From sampling to statistical inference

The rare-event notebook illustrates why direct sampling can miss a Gaussian tail with probability around 10⁻⁹, and how a shifted proposal changes the estimate. A Pareto example shows the instability of poorly matched importance weights. The EM notebook follows fitted parameters and likelihood across several existing experiments.

![EM parameter and likelihood trajectories from the original notebook](assets/em_convergence.png)

## Code and academic context

These projects were developed as coursework and practical assignments. This repository organizes the completed implementations and existing experiments into a coherent selection. Course scaffolding and data sources are credited in [attribution](docs/attribution.md).

The report and notebook introductions are in English; original implementation comments and figure labels are retained where useful. Saved figures are from the original work. No new experimental results are claimed for this presentation edition.

## Run locally

```bash
python -m venv .venv
# Activate .venv for your operating system.
python -m pip install -r requirements.txt
jupyter lab
```

Open the numbered notebooks in `notebooks/`. The CSV is provided in `data/`. Computational cost varies substantially: the complete Air Quality search and some Monte-Carlo cells are intentionally larger experiments. See [reproduction details](docs/reproducibility.md).

```text
notebooks/      Six curated notebooks, with original saved outputs
report/         Illustrated PDF and GitHub-readable report
assets/         Selected original figures
data/           Air Quality CSV and source attribution
docs/           Methodology, provenance and reproduction notes
supplementary/  Completed MCMC helper definitions
scripts/        Structural validation and execution checks
```
