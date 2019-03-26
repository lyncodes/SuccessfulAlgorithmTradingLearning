import pandas as pd
import numpy as np


def create_sharpe_ratio(returns, periods=252):
    """

    :param returns: period percentage returns
    :param periods: daily(252) hourly(252*6.5)
    :return:
    """
    return np.sqrt(periods) * (np.mean(returns) / np.std(returns))


def create_drawdowns(pnl):
    """
    calculate the largest drawdown and the duration
    :param pnl: pandas series representing period percentage returns
    :return: drawdown,duration,highest peak-to-trough drawdown and duration
    """
    hwm = [0]
    # hwm for high water mark
    idx = pnl.index
    drawdown = pd.Series(index=idx)
    duration = pd.Series(index=idx)
    for t in range(1, len(idx)):
        hwm.append(max(hwm[t - 1], pnl[t]))
        drawdown[t] = (hwm[t] - pnl[t])
        duration[t] = (0 if drawdown[t] == 0 else duration[t - 1] + 1)

    return drawdown, drawdown.max(), duration.max()
