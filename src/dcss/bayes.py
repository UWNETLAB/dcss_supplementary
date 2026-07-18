import pandas as pd
pd.set_option("display.notebook_repr_html", False)
import numpy as np
import seaborn as sns
import arviz as az

import matplotlib as mpl
from matplotlib import pyplot as plt

from dcss.plotting import custom_seaborn
custom_seaborn()

import warnings
warnings.filterwarnings('ignore')


def _flat_posterior(posterior, var):
    """
    Return posterior samples of ``var`` flattened across chains, shaped
    (n_samples,) for scalar variables and (n_samples, dim) for vector
    variables. This mirrors the sample-major layout of the old PyMC3
    MultiTrace objects (trace[var]) so the plotting code below can index
    samples the same way the book does.
    """
    da = posterior[var]
    return da.stack(sample=("chain", "draw")).transpose("sample", ...).values


def _flat_predictive(ppc, var):
    """
    Return posterior/prior predictive samples of ``var`` from an ArviZ
    InferenceData object, flattened across chains: (n_samples, n_obs).
    """
    da = ppc.posterior_predictive[var]
    return da.stack(sample=("chain", "draw")).transpose("sample", ...).values


def plot_2020_election_diff(df):
    fig, ax = plt.subplots(figsize=(8,7))
    g = sns.scatterplot(x=df['spend'], y=df['vote'], alpha=.8)

    g.set(xlim = (-2.5e7, 15000000))
    g.set(ylim = (-250000, 350000))

    plt.text(-2e7, 300000, "Democrats Win and Underspend")
    plt.text(-2e7, -200000, "Democrats Lose and Underspend")
    plt.text(3e6, -200000, "Democrats Lose and Overspend")
    plt.text(3e6, 300000, "Democrats Win and Overspend")

    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')

    plt.axhspan(0, 370000, xmin=0.625, xmax=1, facecolor='gray', alpha=0.3)
    plt.axhspan(0, -370000, xmin=0, xmax=0.625, facecolor='crimson', alpha=0.1)
    plt.axhspan(0, 370000, xmin=0, xmax=0.625, facecolor='lightgray', alpha=0.3)
    plt.axhspan(0, -370000, xmin=0.625, xmax=1, facecolor='crimson', alpha=0.3)

    # style the axes
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    ax.set(xlabel='Spending differential (Democrat - Republican)', ylabel='Vote differential (Democrat - Republican)')

    sns.despine(left=True, bottom=True)
    plt.show()




def plot_2020_election_fit(spend_std, vote_std, trace_pool, ppc):
    """
    Plot the pooled-model fit. ``trace_pool`` is the InferenceData returned
    by pm.sample() and ``ppc`` is the InferenceData returned by
    pm.sample_posterior_predictive(). (Updated from the PyMC3-era version,
    which took a MultiTrace and a dict of predictive samples.)
    """
    g = sns.scatterplot(x=spend_std, y=vote_std, alpha=.8)
    g.set(xlim = (-10, 5))
    g.set(ylim = (-3, 4))
    g.axhline(y=0, color='grey')
    g.axvline(x=0, color='grey')
    x_range = np.linspace(-10, 4, 10)

    post = trace_pool.posterior
    alpha_m = post['alpha'].mean().item()
    beta_m = post['beta'].mean().item()

    g.plot(
        x_range,
        alpha_m + beta_m * x_range, # This is our linear model
        c='k',
    )

    alpha_samples = _flat_posterior(post, 'alpha')
    beta_samples = _flat_posterior(post, 'beta')

    mu_pool = (
        alpha_samples
        + beta_samples * np.array(spend_std)[:, None]
        )

    az.plot_hdi(
        spend_std,
        mu_pool.T,
        ax = g,
        fill_kwargs={"alpha": 0.4, "label": "Mean outcome 94% HPD"},
    )

    az.plot_hdi(
        spend_std,
        _flat_predictive(ppc, 'votes'),
        ax = g,
        fill_kwargs={"alpha": 0.4, "color": "lightgray", "label": "Outcome 94% HPD"}
    )

    sns.despine()
    plt.show()


def plot_2020_no_pool(
    no_pool_model,
    trace_no_pool,
    n_states,
    state_idx,
    spend_std,
    vote_std,
    ppc,
    state_cat
):
    """
    Plot per-state fits for the no-pooling model. ``trace_no_pool`` and
    ``ppc`` are InferenceData objects (pm.sample() and
    pm.sample_posterior_predictive() in PyMC 5). The per-state slopes and
    intercepts come from the posterior; the predictive band for the
    observed outcome comes from the posterior predictive samples.
    """
    # Initialize one subplot for each state
    _, ax = plt.subplots(
        8,
        6,
        figsize = (12, 16),
    #     sharex=True,
    #     sharey=True,
        constrained_layout=True
    )

    # Flattens the array from 'ax' to make iterating easier
    ax = np.ravel(ax)

    # Just defining a range of values to put our estimator line on
    x_range = np.linspace(-8, 4, 10)

    alpha_samples = _flat_posterior(trace_no_pool.posterior, 'alpha')
    beta_samples = _flat_posterior(trace_no_pool.posterior, 'beta')
    votes_pp = _flat_predictive(ppc, 'votes')

    state_idx = np.asarray(state_idx)
    spend_std = np.asarray(spend_std)
    vote_std = np.asarray(vote_std)

    for i in range(n_states):

        mask = state_idx == i

        ax[i].set_xlim((-4, 4))
        ax[i].set_ylim((-4, 4))

        # Create a scatterplot of the data from each state
        ax[i].scatter(spend_std[mask], vote_std[mask])

        alpha_m = alpha_samples[:, i].mean()
        beta_m = beta_samples[:, i].mean()

        ax[i].plot(
            x_range,
            alpha_m + beta_m * x_range, # This is our linear model
            c='k',
        )

        ax[i].set_title(state_cat.categories[i])

        if mask.sum() > 1:
            mu_pp = (
                alpha_samples[:, i]
                + beta_samples[:, i] * spend_std[mask][:, None]
                )

            az.plot_hdi(
                spend_std[mask],
                mu_pp.T,
                ax=ax[i],
                fill_kwargs={"alpha": 0.4, "label": "Mean outcome 94% HPD"},
            )

            az.plot_hdi(
                spend_std[mask],
                votes_pp[:, mask],
                ax=ax[i],
                fill_kwargs={"alpha": 0.4, "color": "lightgray", "label": "Outcome 94% HPD"}
            )

        ax[i].set_title(state_cat.categories[i])



def plot_2020_partial_pool(
    partial_pool_model_regularized,
    trace_partial_pool_regularized,
    trace_no_pool,
    n_states,
    state_idx,
    spend_std,
    vote_std,
    ppc,
    state_cat
):
    """
    Plot per-state fits for the regularized partial-pooling model against
    the no-pooling estimates. All traces and ``ppc`` are InferenceData
    objects (PyMC 5).
    """
    _, ax = plt.subplots(
        8,
        6,
        figsize = (12, 16),
    #     sharex=True,
    #     sharey=True,
        constrained_layout=True
    )

    # This just flattens the array from 'ax' so that
    # we can iterate over it with just one iterable
    ax = np.ravel(ax)

    # Just defining a range of values to put our estimator line on
    x_range = np.linspace(-8, 4, 10)

    alpha_np = _flat_posterior(trace_no_pool.posterior, 'alpha')
    beta_np = _flat_posterior(trace_no_pool.posterior, 'beta')
    alpha_pp = _flat_posterior(trace_partial_pool_regularized.posterior, 'alpha')
    beta_pp = _flat_posterior(trace_partial_pool_regularized.posterior, 'beta')
    votes_pp = _flat_predictive(ppc, 'votes')

    state_idx = np.asarray(state_idx)
    spend_std = np.asarray(spend_std)
    vote_std = np.asarray(vote_std)

    # Iterate over the number of states in our data...
    for i in range(n_states):

        mask = state_idx == i

        ax[i].set_xlim((-4, 4))
        ax[i].set_ylim((-4, 4))

        # Create a scatterplot of the data from each state
        # We can use the state_idx variable and an equality statement to produce
        # a mask for our other array-based variables and feed them in
        ax[i].scatter(spend_std[mask], vote_std[mask])

        # The no-pooling estimates, for comparison
        ax[i].plot(
            x_range,
            alpha_np[:, i].mean() + beta_np[:, i].mean() * x_range,
            c='darkgrey',
        )

        # Pull the averaged coefficients for each state from the posterior
        ax[i].plot(
            x_range,
            alpha_pp[:, i].mean() + beta_pp[:, i].mean() * x_range,
            c='k',
        )

        ax[i].set_title(state_cat.categories[i])

        if mask.sum() > 1:
            mu_pp = (
                alpha_pp[:, i]
                + beta_pp[:, i] * spend_std[mask][:, None]
                )

            az.plot_hdi(
                spend_std[mask],
                mu_pp.T,
                ax=ax[i],
                fill_kwargs={"alpha": 0.4, "label": "Mean outcome 94% HPD"},
            )

            az.plot_hdi(
                spend_std[mask],
                votes_pp[:, mask],
                ax=ax[i],
                fill_kwargs={"alpha": 0.4, "color": "lightgray", "label": "Outcome 94% HPD"}
            )

        ax[i].set_title(state_cat.categories[i])
