"""
Signals Module
==============
All @register_signal decorated functions for technical analysis.
These are the core signal generators used in portfolio construction.

Contains 15+ signals covering:
- Mean reversion / momentum detection
- Volatility regimes (entropy, convexity, burstiness)
- Market microstructure (volume agreement, path efficiency)
- Liquidity patterns (record rates, time-since-volume-spike)
"""

import numpy as np
import pandas as pd


# =========================
# HELPER OPERATORS
# =========================

def ts_rank(x, window):
    """Time-series percentile rank (0-1)"""
    return x.rolling(window, min_periods=1).apply(
        lambda a: (a.argsort().argsort()[-1] + 1) / len(a), raw=True
    )


def ts_argmin(x, window):
    """Index of minimum value over window"""
    return x.rolling(window, min_periods=1).apply(np.argmin, raw=True)


def ts_mad(x, window):
    """Mean absolute deviation"""
    m = x.rolling(window, min_periods=1).mean()
    return (x - m).abs().rolling(window, min_periods=1).mean()


def ts_percentile(x, window, p):
    """Rolling percentile"""
    return x.rolling(window, min_periods=1).quantile(p)


def volatility(x, window):
    """Rolling volatility (std)"""
    return x.rolling(window, min_periods=2).std()


def ts_mscore(x, window):
    """Mean absolute scaled score"""
    ax = x.abs()
    s = ax.rolling(window, min_periods=1).sum()
    n = ax.rolling(window, min_periods=1).count()
    return ax * n / s


def apply_decay(signal, decay_days=5, mode="linear"):
    """
    Apply time decay to a signal.
    
    Parameters
    ----------
    signal : pd.Series
        Raw signal (e.g. -1, 0, +1)
    decay_days : int
        Number of days over which signal decays
    mode : str
        "linear" or "exponential"
    
    Returns
    -------
    pd.Series
        Decayed signal (point-in-time safe)
    """
    if decay_days <= 1:
        return signal

    if mode == "linear":
        weights = np.linspace(1.0, 0.0, decay_days)
    elif mode == "exponential":
        weights = np.exp(-np.arange(decay_days))
    else:
        raise ValueError("mode must be 'linear' or 'exponential'")

    weights = weights / weights.sum()

    return signal.rolling(
        window=decay_days,
        min_periods=1
    ).apply(lambda x: np.dot(x[::-1], weights[-len(x):]), raw=True)


def scale_signal(x, cap=1.0):
    """Scale signal to {-cap, 0, cap}"""
    return x.replace({1.0: cap, -1.0: -1.0, 0.0: 0.0})


# =========================
# SIGNAL REGISTRY
# =========================

_SIGNAL_REGISTRY = {}


def register_signal(fn):
    """Decorator to register a signal function"""
    _SIGNAL_REGISTRY[fn.__name__] = fn
    return fn


# =========================
# SIGNAL IMPLEMENTATIONS
# =========================

@register_signal
def signal_1(df, rank_window=189):
    """
    Mean reversion detector based on return volatility and ranking.
    Good for: ROM, QQQ, MUNI, FDN
    """
    x = df["Returns"].diff(2)
    x = ts_mad(x, 2)
    x = np.power(1.0 / x - 1.0, 0.5)
    x = ts_rank(x, rank_window) - 0.33
    return np.sign(x)


@register_signal
def signal_3(df, rank_window=189):
    """
    Volatility convexity signal based on high price behavior.
    Good for: SPAB, PZA, FXU, HYG
    """
    x = np.sqrt(df["High"])
    x = volatility(x, 10)
    x = ts_mscore(1.0 / (x - 1.0), 4)
    x = ts_rank(x, rank_window) - 0.2
    return np.sign(x)


@register_signal
def signal_8(df, win=20):
    """
    Low-frequency momentum signal.
    Good for: SHM, XSD, IEF, FXU
    """
    gap = (df["Open"] - df["Close"].shift(1)) / df["Close"].shift(1)
    x = -gap
    x = ts_rank(x, win) - 0.5
    return np.sign(x)


@register_signal
def signal_9(df, ret_win=21, vol_win=21):
    """
    Return-to-volatility ratio signal.
    Good for: GDX, EWL, XBI, XLP
    """
    ret = df["Returns"].rolling(ret_win).sum()
    vol_chg = df["Returns"].rolling(vol_win).std().diff()
    x = ret * vol_chg
    x = ts_rank(x, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_autocorr(df, win=42):
    """
    Serial correlation regime detector.
    Trendy assets -> long
    Mean reverting -> short
    Good for: IGV, XBI, SH, IJK, ITA
    """
    r = df["Returns"]
    ac = r.rolling(win).apply(
        lambda x: pd.Series(x).autocorr(lag=1),
        raw=False
    )
    return np.sign(ac)


@register_signal
def signal_entropy(df, win=40):
    """
    Entropy-based directionality detector.
    Lower entropy = more directional = trend friendly
    Good for: TMF, DHS, XLV, IWC, XLK
    """
    r = df["Returns"]
    probs = (r > 0).rolling(win).mean()
    entropy = -(
        probs*np.log(probs+1e-9) +
        (1-probs)*np.log(1-probs+1e-9)
    )
    x = -ts_rank(entropy, 252) + 0.5
    return np.sign(x)


@register_signal
def signal_convexity_gap_adjusted(df, win=20):
    """
    Convexity + overnight gap structure.
    Better aligned with open execution.
    """
    gap = (df["Open"] - df["Close"].shift(1)) / df["Close"].shift(1)
    hist_price = df["Close"].shift(1)
    accel = hist_price.diff().diff()
    combo = accel + 0.5 * gap
    combo = combo.rolling(5).mean()
    x = ts_rank(combo, 252) - 0.5
    return -np.sign(x)


@register_signal
def signal_run_length(df, win=40):
    """
    Streak length indicator.
    Detects regime changes in return sign persistence.
    """
    r = np.sign(df["Returns"])
    run = (r != r.shift()).cumsum()
    streak = r.groupby(run).cumcount()
    avg_streak = streak.rolling(win).mean()
    x = -ts_rank(avg_streak, 252) + 0.5
    return np.sign(x)


@register_signal
def signal_record_rate(df, win=120):
    """
    Frequency of new highs in recent history.
    Good for uptrends.
    """
    price = df["Close"]
    rec_high = price == price.cummax()
    rate = rec_high.rolling(win).mean()
    x = ts_rank(rate, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_time_since_volume_spike(df, win=60):
    """
    Days since last volume spike.
    Identifies fresh liquidity regimes.
    """
    vol = df["Volume"]
    spike = vol > vol.rolling(win).quantile(0.9)
    days = (~spike).cumsum() - (~spike).cumsum().where(spike).ffill().fillna(0)
    x = ts_rank(days, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_return_iqr(df, win=40):
    """
    Interquartile range of returns.
    Identifies tight/loose realization of price action.
    """
    r = df["Returns"]
    q75 = r.rolling(win).quantile(0.75)
    q25 = r.rolling(win).quantile(0.25)
    iqr = q75 - q25
    x = -ts_rank(iqr, 252) + 0.5
    return np.sign(x)


@register_signal
def signal_burstiness(df, win=40):
    """
    Volatility of volatility indicator.
    Detects bunched / explosive moves.
    Good for: IGV, EDV, EPP
    """
    r = df["Returns"].abs()
    mean = r.rolling(win).mean()
    std = r.rolling(win).std()
    burst = std / (mean + 1e-9)
    x = -ts_rank(burst, 252) + 0.5
    return -np.sign(x)


@register_signal
def signal_signed_volume_agreement(df, win=40):
    """
    Alignment between return direction and volume change.
    """
    sign = np.sign(df["Returns"])
    vol = df["Volume"].pct_change()
    agree = (sign * vol > 0).astype(int)
    score = agree.rolling(win).mean()
    return -np.sign(score - 0.5)


@register_signal
def signal_path_efficiency(df, win=40):
    """
    Directional path efficiency.
    High efficiency = trending, Low = noisy/mean reverting.
    Good for: FXU, ICLN, IDU, XBI, SH
    """
    disp = (df["Close"] - df["Close"].shift(win)).abs()
    dist = df["Close"].diff().abs().rolling(win).sum()
    eff = disp / (dist + 1e-9)
    x = ts_rank(eff, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_vol_of_vol(df, win=30):
    """
    Volatility of volatility (vol clustering detector).
    """
    r = df["Returns"]
    vol = r.rolling(win).std()
    vov = vol.rolling(win).std()
    x = ts_rank(vov, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_return_conviction(df, win=30):
    """
    Absolute return per unit of daily range.
    Identifies high-conviction moves.
    """
    r = df["Returns"]
    intraday = (df["High"] - df["Low"]) / df["Close"]
    conviction = r.abs() / (intraday + 1e-9)
    x = ts_rank(conviction.rolling(win).mean(), 252) - 0.5
    return np.sign(x)


@register_signal
def signal_price_volume_phase(df, win=40):
    """
    Lagged price-volume correlation.
    Detects leading/lagging microstructure patterns.
    """
    r = df["Returns"]
    dv = df["Volume"].pct_change()
    phase = (r.shift(1) * dv).rolling(win).mean()
    x = ts_rank(phase, 252) - 0.5
    return -np.sign(x)


@register_signal
def signal_vol_compression_ratio(df, win=30):
    """
    Short-term vs long-term volatility compression.
    Identifies volatility regime changes.
    """
    r = df["Returns"]
    short = r.rolling(10).std()
    long = r.rolling(win).std()
    ratio = short / (long + 1e-9)
    x = ts_rank(ratio, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_liquidity_persistence(df, win=40):
    """
    Persistence of volume shocks.
    Identifies liquidity regimes.
    """
    v = df["Volume"]
    shock = v / (v.rolling(win).mean() + 1e-9)
    persistence = shock.rolling(win).mean()
    x = ts_rank(persistence, 252) - 0.5
    return np.sign(x)


@register_signal
def signal_vol_drift_imbalance(df, win=40):
    """
    Volatility drift vs. return drift imbalance detector.
    Identifies when volatility and return regimes diverge.
    Good for: XBI, DGS, ICLN, EWG, DBC, DEM, IGF, VPU
    
    Parameters
    ----------
    df : pd.DataFrame
        Price data with ['Returns', 'Open', 'High', 'Low', 'Close', 'Volume']
    win : int
        Rolling window for volatility/drift calculation (default 40)
    
    Returns
    -------
    np.ndarray
        Discrete signal: {-1, 0, +1}
    """
    r = df["Returns"]
    vol = r.rolling(win).std()
    vol_drift = vol.diff()
    drift = r.rolling(win).mean()
    score = drift - vol_drift
    x = ts_rank(score, 252) - 0.5
    return np.sign(x)
