"""Completed helpers from the supplied TP6 MCMC practical.

The MALA, leapfrog and HMC templates are unfinished and are not exported.
See docs/attribution.md for academic provenance.
"""

import autograd.numpy as np
import scipy.stats as st
from tqdm import tqdm

def multi_gauss(mu, sigma):
    """
    Inputs
    ----------
    mu: mean of the Gaussian distribution
    sigma: covariance matrix of the Gaussian distribution

    Outputs
    -------
    logp: opposite of the loglikelihood
    """

    def logp(x):
        n = mu.size
        diff = (x - mu)
        logdet = np.linalg.slogdet(sigma)[1]
        inv_sigma = np.linalg.inv(sigma)

        return n/2*np.log(2*np.pi) + 1/2 * logdet  + 1/2*(diff.T)@inv_sigma@diff

    return logp

def mixture(log_prob, weights):
    """
    Inputs
    ----------
    log_prob: opposite of the likelihood of each term
    weights: weights of the components of the mixture

    Outputs
    -------
    logp: opposite of the loglikelihood of the mixture
    """

    def logp(x):
        logprobvalue = np.array([lp(x) for lp in log_prob])
        return -np.log(np.sum(weights * np.exp(-logprobvalue)))

    return logp


def HM_monte_carlo(n_samples, log_prob, initial_state, step_size = 0.1):
    """
    Inputs
    ----------
    n_samples: number of samples to return
    log_prob: opposite of the loglikelihood to sample from
    initial_state: initial sample
    step_size: standard deviation of the proposed moves

    Outputs
    -------
    samples: samples from the MCMC algorithm
    accepted: array of 0 and 1 to display which proposed moves have been accepted
    """
    initial_state = np.array(initial_state)

    samples  = [initial_state]
    accepted = []

    size = (n_samples,) + initial_state.shape[:1]

    # random variable to sample proposed moves
    epsilon = st.norm(0, 1).rvs(size)

    for noise in tqdm(epsilon):
        unif = st.uniform().rvs()
        Z = initial_state + step_size*noise
        if unif < min(1, np.exp(-log_prob(Z) + log_prob(initial_state))):
            accepted.append(1); samples.append(Z)
            initial_state = Z
        else:
            samples.append(initial_state); accepted.append(0)

    return (np.array(samples[1:]),np.array(accepted),)
