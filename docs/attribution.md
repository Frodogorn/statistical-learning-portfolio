# Academic provenance and editorial scope

## Author and context

Gabriel Trabelsi is the author of the submitted coursework implementations and completed experiments presented here. Current programme: M2 IASD, Université Paris Dauphine-PSL. This current affiliation does not change the provenance of earlier coursework.

The original notebooks mix supplied exercise frameworks, utility code and student answers. Authorship of the entire teaching scaffold is not claimed.

## Source mapping

| Repository material | Original academic material | Selection |
| --- | --- | --- |
| Air Quality | Combined statistical-learning submission and its exploratory/modelling notebooks | One combined version, avoiding duplicates |
| Random-variable simulation and rare events | UM4MA379 TP1, Statistique Computationnelle, Sorbonne Université, Master 1, 2025-2026 | Completed simulation and estimation code |
| Gaussian Bayes | UM4MA379 TP2 | Completed conjugate-Gaussian example |
| Metropolis and MALA | UM4MA379 TP3 | Completed Gaussian samplers and posterior-sampling code |
| MCMC helpers | Supplied TP6 MALA/HMC notebook | Completed target-density helpers and Metropolis function only |
| Gaussian-mixture EM | Supplied TP7 Expectation Maximization notebook | Completed univariate implementation and experiments |

The original UM4MA379 TP1-TP3 headers credit **A. Guyader** (course) and **M. Sangnier** (practical sessions). The TP6 and TP7 files do not provide an individual instructor attribution in their headers; none has been invented. The Air Quality instructions are acknowledged as the project brief; no instructor name was supplied with that brief.

## Presentation changes

- Numbered notebooks, English introductions and shorter explanatory sections.
- Repeated exercise prompts, empty answer cells, duplicated cells and unused template sections removed from the selection.
- Original algorithms and experiment settings preserved, apart from the small documented execution fix below.
- Dataset loading made relative to the repository, without changing its parsing or filtering.
- Unused `Geo_exp` helper fixed to pass the required sample-size argument to `expon`.
- An incorrect covariance comment corrected; mathematical interpretation aligned with the code.
- Historical execution counters cleared. Saved useful outputs retained; local paths, progress-bar noise and object-memory addresses removed.
- Air Quality narrative tables aligned with numerical cell outputs; overly strong interpretive claims qualified.
- Inconsistent saved outputs in the posterior-sampling section omitted. The completed code remains available.

No new algorithms or experimental extensions were added. The figure files are exported from the existing notebook outputs. Source-cell hashes are recorded in `source_manifest.json`; no local filesystem paths or student identifiers are published.

Course PDFs, provided corrections, unfilled exercise templates and redundant notebook copies are not republished. No completed HMC implementation, variational-inference project or fully completed TP2 is claimed.

## Data and reuse

The Air Quality dataset is credited separately in [data/README.md](../data/README.md). This repository does not apply a blanket software licence to supplied teaching material. For reuse beyond reviewing these academic projects, contact the relevant authors and consult the dataset terms.
