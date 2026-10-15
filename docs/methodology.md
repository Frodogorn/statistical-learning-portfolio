# Reading the experiments

This portfolio is a presentation of existing coursework. It does not replace the recorded experiments with a new benchmark.

## Air Quality

1. **Task.** Sensor-based estimation of contemporaneous reference concentrations. A chronological split is used, but the model is not defined as a forecast at a future horizon.
2. **Missingness.** `-200` is converted to missing values. `NMHC(GT)` is removed and complete-case filtering retains 6,941 observations. Selection from missingness can affect the sample.
3. **Outer split.** 5,552 training rows and 1,389 later evaluation rows. The original file order is chronological after cleaning.
4. **Preprocessing.** The scaler is fitted only on the outer training partition, but before the inner cross-validation. A fully isolated inner protocol would fit preprocessing separately within each fold.
5. **Model selection.** Kernel ridge uses temporal folds. RidgeCV retains its default validation. MLP early stopping uses its internal holdout; it is not a chronological holdout. The final chronological partition is reused for architecture/hyperparameter comparisons and feature exploration.
6. **Reported values.** The report transcribes saved outputs, rather than the original hand-written summary table. The fixed `(64, 32)` MLP column is one defined configuration, not a per-target maximum across architectures.
7. **Interpretation.** Correlations, coefficient magnitudes, permutation importance and Kernel SHAP are descriptive. None establishes causality. SHAP is affected by background/masking assumptions and does not automatically resolve correlated predictors.
8. **Residuals.** The residual plot uses a deeper `(256, 128, 64, 32)` network with time features, not the fixed MLP shown in the main comparison table.

Reference implementation guidance: [scikit-learn: common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html), [Kernel SHAP API](https://shap.readthedocs.io/en/latest/generated/shap.KernelExplainer.html).

## Simulation and importance sampling

Saved timings describe individual runs on the original machine. Box-Muller returns two values per row, whereas the adjacent SciPy timing generates one value per row; the recorded timings are not a matched-throughput comparison. The geometric trial loop has a finite iteration guard.

The Gaussian rare-event examples illustrate the dependence of an estimator on the proposal. Pointwise asymptotic intervals are not simultaneous confidence bands. For the Pareto target with an exponential proposal, extreme weights invalidate a casual interpretation of the displayed normal-approximation interval. There is no repeated-run coverage experiment in this work.

## MCMC

The Gaussian examples display marginal histograms and acceptance rates. They do not report effective sample sizes or multi-chain convergence diagnostics. Direct-density arithmetic can underflow. The supplementary posterior code uses large sample arrays and has not been promoted as a verified performance comparison. Its inconsistent historical outputs are omitted, and the local proposal's actual `1/sqrt(m)` scale is documented.

## EM

The implemented univariate model has separate component variances, while some supplied theoretical notes discuss a shared covariance. The portfolio describes the implemented model. The algorithm uses direct densities and a fixed iteration budget, with no variance floor or log-sum-exp stabilization. Initialization experiments are informative single runs, not guarantees of global optimization. The sample-size experiment draws fresh data at each size and does not estimate expected performance.
