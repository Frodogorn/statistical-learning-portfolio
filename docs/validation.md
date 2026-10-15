# Validation record

Presentation checks performed on 14 September 2026; the HMC notebook was added and checked on 15 October 2026. Historical notebook outputs were preserved, not replaced by the checks below.

## Executed checks

| Notebook | Executed code cells | Scope | Result |
| --- | ---: | --- | --- |
| Air Quality | 15 | Exploratory analysis, actual-size preprocessing, chronological split and OLS/ridge baselines | PASS |
| Random-variable simulation | 10 | All selected cells, with bounded sample sizes in memory | PASS |
| Rare-event estimation | 9 | All selected cells, with bounded sample sizes in memory | PASS |
| Gaussian Bayes | 3 | All selected cells | PASS |
| Metropolis and MALA | 9 | All selected cells, including posterior code, with bounded sizes in memory | PASS |
| Expectation maximization | 14 | All selected cells, with bounded sizes in memory | PASS |
| Hamiltonian Monte Carlo | 12 | Full re-execution in a fresh kernel (these are the published outputs), then the bounded smoke check | PASS |

Air Quality reproduces the 5,552-by-8 training matrix and 1,389-by-8 evaluation matrix. Its recomputed linear scores are finite. A bounded EM run has finite, non-decreasing log-likelihood within numerical tolerance. These checks verify execution and limited invariants, not the validity of every scientific interpretation.

Expected headless-display warnings and a Matplotlib orientation deprecation were observed. No execution exception remained in the selected check paths.

## Inspection scope

- All published notebook code and Python scripts parsed for syntax.
- Local Markdown links checked.
- Original saved figures exported without changing their numerical contents.
- Air Quality report values checked against saved cell outputs.
- Local user paths, student identifiers, historical progress noise and empty exercise placeholders removed from the published selection.
- PDF pages rendered and visually inspected before publication.

## Not rerun in full

The complete Air Quality kernel searches, neural-network sweeps and SHAP calculation were not rerun. The 100-million/50-million-draw experiments and the original-size posterior-sampling workload were checked at reduced sizes only. The original random seeds and environment were not recovered as a fully locked historical environment.

Commands:

```bash
python scripts/validate.py
python scripts/smoke_check.py
```
