import numpy as np


def li_ma_significance(n_on, n_off, alpha=0.2):
    '''
    Calculate the Li&Ma significance for given
    observations data

    Parameters
    ----------
    n_on: integer or array like
        Number of events for the on observations
    n_off: integer of array like
        Number of events for the off observations
    alpha: float
        Scaling factor for the off observations, for wobble observations
        this is 1 / number of off regions
    '''

    scalar = np.isscalar(n_on)

    n_on = np.array(n_on, copy=False, ndmin=1)
    n_off = np.array(n_off, copy=False, ndmin=1)

    with np.errstate(divide='ignore', invalid='ignore'):
        p_on = n_on / (n_on + n_off)
        p_off = n_off / (n_on + n_off)

        t1 = n_on * np.log(((1 + alpha) / alpha) * p_on)
        t2 = n_off * np.log((1 + alpha) * p_off)

        ts = (t1 + t2)
        significance = np.sqrt(ts * 2)

    significance[np.isnan(significance)] = 0
    significance[n_on < alpha * n_off] = 0

    if scalar:
        return significance[0]

    return significance
