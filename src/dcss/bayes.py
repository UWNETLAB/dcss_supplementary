import pandas as pd
pd.set_option("display.notebook_repr_html", False)
import numpy as np
import seaborn as sns
import pymc3 as pm
import arviz as az

import matplotlib as mpl
from matplotlib import pyplot as plt

from dcss.plotting import custom_seaborn
custom_seaborn()

import warnings
warnings.filterwarnings('ignore')




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
    g = sns.scatterplot(x=spend_std, y=vote_std, alpha=.8)
    g.set(xlim = (-10, 5))
    g.set(ylim = (-3, 4))
    g.axhline(y=0, color='grey')
    g.axvline(x=0, color='grey')
    x_range = np.linspace(-10, 4, 10)

    alpha_m = trace_pool['alpha'].mean()
    beta_m = trace_pool['beta'].mean()

    g.plot(
        x_range,
        alpha_m + beta_m * x_range, # This is our linear model
        c='k',
    )

    mu_pool = (
        ppc['alpha']
        + ppc['beta'] * np.array(spend_std)[:, None]
        )

    az.plot_hdi(
        spend_std,
        mu_pool.T,
        ax = g,
        fill_kwargs={"alpha": 0.4, "label": "Mean outcome 94% HPD"},
    )

    az.plot_hdi(
        spend_std,
        ppc['votes'],
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


    with no_pool_model:

        for i in range(n_states):

            ax[i].set_xlim((-4, 4))
            ax[i].set_ylim((-4, 4))

            # Create a scatterplot of the data from each state
            ax[i].scatter(spend_std[state_idx == i], vote_std[state_idx == i])

            alpha_m = trace_no_pool['alpha'][:, i].mean()
            beta_m = trace_no_pool['beta'][:, i].mean()

            ax[i].plot(
                x_range,
                alpha_m + beta_m * x_range, # This is our linear model
                c='k',
            )

            ax[i].set_title(state_cat.categories[i])

            if len(spend_std[state_idx == i]) > 1:
                mu_pp = (
                    ppc['alpha'][:,i]
                    + ppc['beta'][:,i] * np.array(spend_std[state_idx == i])[:, None]
                    )

                az.plot_hdi(
                    spend_std[state_idx == i],
                    mu_pp.T,
                    ax=ax[i],
                    fill_kwargs={"alpha": 0.4, "label": "Mean outcome 94% HPD"},
                )

                az.plot_hdi(
                    spend_std[state_idx == i],
                    ppc['votes'][:, state_idx == i],
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


    with partial_pool_model_regularized:

        # Iterate over the number of states in our data...
        for i in range(n_states):

            ax[i].set_xlim((-4, 4))
            ax[i].set_ylim((-4, 4))

            # Create a scatterplot of the data from each state
            # We can use the state_idx variable and an equality statement to produce
            # a mask for our other array-based variables and feed them in
            ax[i].scatter(spend_std[state_idx == i], vote_std[state_idx == i])

            alpha_m = trace_no_pool['alpha'][:, i].mean()
            beta_m = trace_no_pool['beta'][:, i].mean()

            ax[i].plot(
                x_range,
                alpha_m + beta_m * x_range, # This is just our linear model
                c='darkgrey',
            )

            # Pull the averaged coefficients for each state from the trace
            alpha_m = trace_partial_pool_regularized['alpha'][:, i].mean()
            beta_m = trace_partial_pool_regularized['beta'][:, i].mean()

            ax[i].plot(
                x_range,
                alpha_m + beta_m * x_range, # This is just our linear model
                c='k',
            )

            ax[i].set_title(state_cat.categories[i])

            if len(spend_std[state_idx == i]) > 1:
                mu_pp = (
                    ppc['alpha'][:,i]
                    + ppc['beta'][:,i] * np.array(spend_std[state_idx == i])[:, None]
                    )

                az.plot_hdi(
                    spend_std[state_idx == i],
                    mu_pp.T,
                    ax=ax[i],
                    fill_kwargs={"alpha": 0.4, "label": "Mean outcome 94% HPD"},
                )

                az.plot_hdi(
                    spend_std[state_idx == i],
                    ppc['votes'][:, state_idx == i],
                    ax=ax[i],
                    fill_kwargs={"alpha": 0.4, "color": "lightgray", "label": "Outcome 94% HPD"}
                )

            ax[i].set_title(state_cat.categories[i])
