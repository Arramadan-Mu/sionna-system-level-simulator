# visualization/plots.py

import matplotlib.pyplot as plt
import numpy as np


def get_cdf(values):
    """
    Computes the Cumulative Distribution Function (CDF) of the input
    """
    values = np.array(values).flatten()
    n = len(values)
    sorted_val = np.sort(values)
    cumulative_prob = np.arange(1, n+1) / n
    return sorted_val, cumulative_prob


def plot_performance_metrics(results_avg, bler_target):
    """
    Plot performance metrics with CDFs
    """
    metrics = list(results_avg.keys())
    
    fig, axs = plt.subplots(3, 3, figsize=(8, 6.5))
    fig.suptitle('Per-user performance metrics', y=.99)

    for ii in range(3):
        for jj in range(3):
            ax = axs[ii, jj]
            metric = metrics[3*ii+jj]
            ax.plot(*get_cdf(results_avg[metric]))
            if metric == 'TBLER':
                # Visualize BLER target
                ax.plot([bler_target]*2, [0, 1], '--k', label='target')
                ax.legend()
            if metric == 'TX power [dBm]':
                # Avoid plotting artifacts
                ax.set_xlim(ax.get_xlim()[0]-.5, ax.get_xlim()[1]+.5)
            ax.set_xlabel(metric)
            ax.grid()
            ax.set_ylabel('CDF')

    fig.tight_layout()
    return fig


def pairplot(dict, keys, suptitle=None, figsize=2.5):
    """
    Create a pairplot for selected metrics
    """
    fig, axs = plt.subplots(len(keys), len(keys),
                            figsize=[len(keys)*figsize]*2)
    for row, key_row in enumerate(keys):
        for col, key_col in enumerate(keys):
            ax = axs[row, col]
            ax.grid()
            if row == col:
                ax.hist(dict[key_row], bins=30,
                        color='skyblue', edgecolor='k',
                        linewidth=.5)
            elif col > row:
                fig.delaxes(ax)
            else:
                ax.scatter(dict[key_col], dict[key_row],
                           s=16, color='skyblue', alpha=0.9,
                           linewidths=.5, edgecolor='k')
            ax.set_ylabel(key_row)
            ax.set_xlabel(key_col)
    if suptitle is not None:
        fig.suptitle(suptitle, y=1, fontsize=17)
    fig.tight_layout()
    return fig, axs


def plot_sinr_mcs_throughput(results_avg):
    """
    Plot SINR, MCS, and throughput relationship
    """
    fig, axs = pairplot(results_avg,
                        ['Effective SINR [dB]', 'MCS', '# decoded bits / slot'],
                        suptitle='MCS, SINR, and throughput')
    return fig, axs


def plot_bler_mcs_olla(results_avg, bler_target):
    """
    Plot BLER, MCS, and OLLA offset relationship
    """
    fig, axs = pairplot(results_avg,
                        ['TBLER', 'MCS', 'OLLA offset'],
                        suptitle='TBLER, MCS, and OLLA offset')
    for ii in range(3):
        axs[ii, 0].plot([bler_target]*2, axs[ii, 0].get_ylim(), '--k')
    return fig, axs


def plot_pf_resources_mcs(results_avg):
    """
    Plot PF metric, allocated resources, and MCS relationship
    """
    fig, axs = pairplot(results_avg,
                        ['# allocated REs / slot', 'PF metric', 'MCS'],
                        suptitle='PF metric, allocated resources, and MCS')
    return fig, axs


def show_network_topology(sls):
    """
    Show the network topology with user positions
    """
    fig = sls.grid.show()
    ax = fig.get_axes()
    ax[0].plot(sls.ut_loc[0, :, 0], sls.ut_loc[0, :, 1],
               'xk', label='user position')
    ax[0].legend()
    return fig
