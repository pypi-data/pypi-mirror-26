from matplotlib import pyplot as pp
import numpy
import msmexplorer as msme


def plot_spawns(inds, tica_trajs, ax=None, obs=(0, 1), color='red'):
    if ax is None:
        ax = pp.gca()

    for traj_i, frame_i in inds:
        ax.scatter(
            tica_trajs[traj_i][frame_i, obs[0]],
            tica_trajs[traj_i][frame_i, obs[1]],
            color=color
        )
    return ax


def plot_tica_landscape(tica_trajs, ax=None, figsize=(7, 5), obs=(0, 1)):
    if ax is None:
        f, ax = pp.subplots(figsize=figsize)

    txx = numpy.concatenate(list(tica_trajs.values()))
    ax = msme.plot_free_energy(
        txx, ax=ax, obs=obs, alpha=1,
        n_levels=6,
        xlabel='tIC 1', ylabel='tIC 2',
        labelsize=14
    )

    return ax


def plot_clusters(clusterer, ax=None, obs=(0, 1), base_size=1,
                  alpha=0.5, color='yellow'):
    if ax is None:
        ax = pp.gca()

    prune = clusterer.cluster_centers_[:, obs]

    ax.scatter(
        prune[:, 0],
        prune[:, 1],
        s=base_size / 5,
        alpha=1,
        color='black'
    )

    ax.scatter(
        prune[:, 0],
        prune[:, 1],
        s=clusterer.counts_ * base_size,
        alpha=alpha,
        color=color
    )

    return ax
