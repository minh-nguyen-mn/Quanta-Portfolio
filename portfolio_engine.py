"""
Portfolio Analysis Engine
===========================
Core backtesting and portfolio construction logic.
Handles signal aggregation, position building, PnL calculation, and metrics.

Uses:
    - Signal registry from signals.py
    - Configuration from portfolio_config.py
    - Data fetched via Polygon API
"""

import os
import numpy as np
import pandas as pd
import requests
from datetime import datetime


# =========================
# CORE CALCULATION ENGINES
# =========================

def sharpe(returns, ann_factor=252):
    """
    Annualized Sharpe ratio with robustness checks.
    
    Parameters
    ----------
    returns : pd.Series
        Daily returns
    ann_factor : int
        Trading days per year (default 252)
    
    Returns
    -------
    float
        Annualized Sharpe ratio or NaN if insufficient data
    """
    returns = returns.dropna()
    if returns.std() == 0 or len(returns) < 10:
        return np.nan
    return np.sqrt(ann_factor) * returns.mean() / returns.std()


def cagr(returns, periods_per_year=252):
    """Compound Annual Growth Rate"""
    returns = returns.dropna()
    if len(returns) == 0:
        return np.nan
    total = (1 + returns).prod()
    years = len(returns) / periods_per_year
    return total ** (1 / years) - 1


def max_drawdown(returns):
    """Maximum drawdown from peak"""
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    dd = cum / peak - 1
    return dd.min()


def equity_curve(pnl_series):
    """
    Continuous cumulative return curve.
    NEVER resets across train/val/blind.
    """
    pnl_series = pnl_series.fillna(0)
    return (1 + pnl_series).cumprod()


def compute_turnover(position):
    """
    Daily portfolio turnover.
    
    Works for:
        Series  -> scalar per day
        DataFrame -> sums across assets
    """
    to = position.diff().abs().fillna(0)
    if isinstance(to, pd.DataFrame):
        return to.sum(axis=1)
    else:
        return to


def average_turnover(position):
    """Average daily turnover (% of book)"""
    return 100 * compute_turnover(position).mean()


def compute_margin(pnl, position):
    """
    Margin = total PnL / total dollars traded
    Returned in basis points (bps)
    """
    dollars_traded = compute_turnover(position).sum()
    if dollars_traded == 0 or np.isnan(dollars_traded):
        return np.nan
    return 1e4 * pnl.sum() / dollars_traded


def compute_pnl(position, returns, leverage_cap=None):
    """Single-asset PnL with optional leverage clipping"""
    pos = position.copy()
    if leverage_cap is not None:
        pos = pos.clip(-1.0, leverage_cap)
    return pos.shift(1) * returns


def compute_open_pnl(position, df, leverage_cap=None):
    """Open-to-open PnL"""
    pos = position.copy()
    if leverage_cap is not None:
        pos = pos.clip(-1.0, leverage_cap)
    return pos.shift(1) * df["Open"].pct_change()


def compute_portfolio_pnl_with_costs(positions, returns_df, cost_bps=0, leverage_cap=None):
    """
    Cost-aware portfolio PnL.
    
    Parameters
    ----------
    positions : pd.DataFrame
        Daily weights across ETFs
    returns_df : pd.DataFrame
        Daily returns across ETFs
    cost_bps : float
        Round-trip cost in basis points
    leverage_cap : float, optional
        Maximum leverage to apply
    
    Returns
    -------
    pd.Series
        Daily portfolio PnL/returns
    """
    pos = positions.copy()
    if leverage_cap is not None:
        pos = pos.clip(-1.0, leverage_cap)
    
    gross = (pos.shift(1) * returns_df).sum(axis=1)
    
    if cost_bps == 0:
        return gross
    
    turnover = compute_turnover(pos)
    cost = turnover * (cost_bps / 1e4)
    return gross - cost


def rescale_books(positions, long_target=1.0, short_target=1.0):
    """
    Proportionally rescales daily long/short books.
    
    Ensures:
        sum(long weights)  = long_target
        sum(short weights) = -short_target
    
    Keeps relative weights unchanged.
    """
    pos = positions.copy()
    longs = pos.clip(lower=0)
    shorts = pos.clip(upper=0)
    
    long_sum = longs.sum(axis=1)
    short_sum = -shorts.sum(axis=1)
    
    long_scale = np.where(long_sum > 0, long_target / long_sum, 0)
    short_scale = np.where(short_sum > 0, short_target / short_sum, 0)
    
    scaled = (
        longs.mul(long_scale, axis=0) +
        shorts.mul(short_scale, axis=0)
    )
    return scaled


# =========================
# SIGNAL COMBINATION
# =========================

COMBINE_MODE_OPTIONS = ["equal", "vote", "rank", "zscore"]
COMBINE_MODE = "equal"


def combine_signals(signals_df, mode=COMBINE_MODE, win=63):
    """
    Combine multiple signals for ONE ETF into a discrete direction.
    Output is {-1, 0, +1}.
    
    Parameters
    ----------
    signals_df : pd.DataFrame
        Multiple signal columns for same ETF
    mode : str
        Combination method: "equal", "vote", "rank", or "zscore"
    win : int
        Window for rolling aggregation
    
    Returns
    -------
    pd.Series
        Combined signal {-1, 0, +1}
    """
    if signals_df.shape[1] == 1:
        raw = signals_df.iloc[:, 0]
    
    elif mode == "equal":
        raw = signals_df.mean(axis=1)
    
    elif mode == "vote":
        raw = np.sign(signals_df).sum(axis=1)
    
    elif mode == "rank":
        ranked = (
            signals_df
            .rolling(win)
            .apply(lambda x: x.rank(pct=True).iloc[-1], raw=False)
        )
        raw = ranked.mean(axis=1) - 0.5
    
    elif mode == "zscore":
        mu = signals_df.rolling(win).mean()
        sigma = signals_df.rolling(win).std()
        z = (signals_df - mu) / sigma
        z = z.clip(-3, 3)
        raw = z.mean(axis=1)
    
    else:
        raise ValueError(f"Unknown combine_mode: {mode}")
    
    direction = np.sign(raw)
    direction[raw.abs() < 1e-6] = 0
    return direction


# =========================
# PORTFOLIO CONSTRUCTION
# =========================

PORTFOLIO_MODE_OPTIONS = ["equal", "rank", "zscore", "vol_scaled", "ic_weighted"]
PORTFOLIO_MODE = "equal"


def build_long_short_portfolio(
    signal_df,
    returns_df=None,
    portfolio_mode=PORTFOLIO_MODE,
    win=63,
    long_leverage=1.0,
    short_leverage=1.0
):
    """
    Build daily long-short portfolio across ETFs.
    
    Parameters
    ----------
    signal_df : pd.DataFrame
        Daily signals {-1, 0, +1} per ETF
    returns_df : pd.DataFrame, optional
        Daily returns (required for vol_scaled, ic_weighted modes)
    portfolio_mode : str
        Weight allocation method
    win : int
        Rolling window for ranking/smoothing
    long_leverage : float
        Leverage applied to long book
    short_leverage : float
        Leverage applied to short book
    
    Returns
    -------
    pd.DataFrame
        Daily portfolio weights
    """
    positions = pd.DataFrame(0.0, index=signal_df.index, columns=signal_df.columns)
    
    for t in signal_df.index:
        sig = signal_df.loc[t]
        longs = sig[sig > 0].index
        shorts = sig[sig < 0].index
        
        if len(longs) == 0 and len(shorts) == 0:
            continue
        
        # RAW WEIGHTS
        if portfolio_mode == "equal":
            w_long = pd.Series(1.0, index=longs)
            w_short = pd.Series(1.0, index=shorts)
        
        elif portfolio_mode == "rank":
            ranks = signal_df.loc[:t].rank(axis=1, pct=True).iloc[-1]
            w_long = ranks.loc[longs]
            w_short = 1 - ranks.loc[shorts]
        
        elif portfolio_mode == "zscore":
            mu = signal_df.loc[:t].rolling(win).mean().iloc[-1]
            sd = signal_df.loc[:t].rolling(win).std().iloc[-1]
            z = (signal_df.loc[t] - mu) / sd
            w_long = z.loc[longs].clip(lower=0)
            w_short = (-z.loc[shorts]).clip(lower=0)
        
        elif portfolio_mode == "vol_scaled":
            if returns_df is None:
                raise ValueError("returns_df required for vol_scaled mode")
            vols = returns_df.loc[:t].rolling(win).std().iloc[-1]
            w_long = 1 / vols.loc[longs]
            w_short = 1 / vols.loc[shorts]
        
        elif portfolio_mode == "ic_weighted":
            if returns_df is None:
                raise ValueError("returns_df required for ic_weighted mode")
            ic = (
                signal_df
                .rolling(win)
                .corr(returns_df)
                .shift(1)
                .iloc[-1]
            )
            w_long = ic.loc[longs].clip(lower=0)
            w_short = (-ic.loc[shorts]).clip(lower=0)
        
        else:
            raise ValueError(f"Unknown portfolio_mode: {portfolio_mode}")
        
        # NORMALIZE BOOKS
        if len(w_long) > 0:
            w_long = w_long / w_long.sum() * long_leverage
        
        if len(w_short) > 0:
            w_short = w_short / w_short.sum() * short_leverage
        
        positions.loc[t, w_long.index] = w_long
        positions.loc[t, w_short.index] = -w_short
    
    return positions


# =========================
# MULTI-ETF BACKTEST ENGINE
# =========================

CACHE_DIR = "data_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
_ETF_CACHE = {}  # Session cache


def fetch_etf(ticker, api_key, start_date="2000-01-01"):
    """
    Fetch ETF data from Polygon API.
    
    Parameters
    ----------
    ticker : str
        ETF symbol
    api_key : str
        Polygon API key
    start_date : str
        Start date (YYYY-MM-DD)
    
    Returns
    -------
    pd.DataFrame or None
        OHLCV data with Returns column, indexed by Date
    """
    end = datetime.today().strftime("%Y-%m-%d")
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end}"
    params = {
        "adjusted": True,
        "sort": "asc",
        "limit": 50000,
        "apiKey": api_key
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        results = r.json().get("results")
        if not results:
            print(f"Warning: No data found for {ticker} from Polygon API.")
            return None
        
        df = pd.DataFrame(results)
        df["Date"] = pd.to_datetime(df["t"], unit="ms")
        df = df.set_index("Date").sort_index()
        
        df = df.rename(columns={
            "o": "Open", "h": "High", "l": "Low",
            "c": "Close", "v": "Volume"
        })
        
        df["Returns"] = df["Close"].pct_change()
        return df[["Open", "High", "Low", "Close", "Volume", "Returns"]]
    
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None


def load_price_data(trading_universe, api_key, force_reload=False):
    """
    Load price data with caching.
    
    Ensures:
        • Each ETF fetched at most once per session
        • No duplicate API calls
        • Safe to rerun cells
        • SPY always included
    """
    required = sorted(set(trading_universe) | {"SPY"})
    data = {}
    hits = []
    fetched = []
    failed = []
    
    print("\nLoading ETF data...\n")
    
    for ticker in required:

        cache_file = os.path.join(CACHE_DIR, f"{ticker}.pkl")

        # 1️⃣ Session cache
        if ticker in _ETF_CACHE and not force_reload:
            data[ticker] = _ETF_CACHE[ticker]
            hits.append(ticker)
            continue

        # 2️⃣ Disk cache
        if os.path.exists(cache_file) and not force_reload:
            try:
                df = pd.read_pickle(cache_file)
                _ETF_CACHE[ticker] = df
                data[ticker] = df
                hits.append(ticker)
                continue
            except Exception:
                print(f"Cache corrupted for {ticker}, refetching")

        # 3️⃣ Fetch from API
        df = fetch_etf(ticker, api_key)

        if df is not None:
            try:
                df.to_pickle(cache_file)
            except Exception:
                pass

            _ETF_CACHE[ticker] = df
            data[ticker] = df
            fetched.append(ticker)

        else:
            failed.append(ticker)
    
    if hits:
        print(f"✓ Cache hits   ({len(hits)}): {hits[:5]}{'...' if len(hits) > 5 else ''}")
    if fetched:
        print(f"↓ Fetched new ({len(fetched)}): {fetched[:5]}{'...' if len(fetched) > 5 else ''}")
    if failed:
        print(f"✗ Failed      ({len(failed)}): {failed[:5]}{'...' if len(failed) > 5 else ''}")
    
    print()
    return data


def run_period(
    start,
    end,
    price_data,
    signal_functions,
    combine_mode=COMBINE_MODE,
    portfolio_mode=PORTFOLIO_MODE,
    win=63,
    long_leverage=1.0,
    short_leverage=1.0,
    signal_map=None,
    etf_universe=None
):
    """
    Run backtest for a time period.
    
    Supports 3 modes:
    1) None -> all signals on all ETFs
    2) {ETF: [signals]} -> per-ETF signals
    3) {signal: [ETFs]} -> per-signal portfolios
    
    Parameters
    ----------
    start : str
        Start date (YYYY-MM-DD)
    end : str
        End date (YYYY-MM-DD)
    price_data : dict
        {ticker: dataframe} loaded price data
    signal_functions : list
        Registered signal callables
    combine_mode : str
        How to combine signals per ETF
    portfolio_mode : str
        How to weight across ETFs
    win : int
        Rolling window
    long_leverage : float
        Long book leverage
    short_leverage : float
        Short book leverage
    signal_map : dict, optional
        Signal-to-ETF or ETF-to-signal mapping
    etf_universe : list, optional
        Active ETF universe
    
    Returns
    -------
    tuple
        (pnl, positions, returns_df, individual_etf_pnls)
    """
    
    # Detect signal map mode
    if signal_map is None or len(signal_map) == 0:
        map_mode = "none"
    else:
        first_key = next(iter(signal_map.keys()))
        map_mode = "signal_to_etf" if callable(first_key) else "etf_to_signal"
    
    # MODE 3: signal -> ETF mapping
    if map_mode == "signal_to_etf":
        pnl_list = []
        pos_list = []
        all_etfs = sorted({etf for lst in signal_map.values() for etf in lst})
        valid_etfs = [e for e in all_etfs if e in price_data]
        
        if len(valid_etfs) == 0:
            raise ValueError("No ETFs found in price_data for Mode 3")
        
        returns_df = pd.DataFrame({
            etf: price_data[etf].loc[start:end]["Returns"]
            for etf in valid_etfs
        })
        master_index = returns_df.index
        
        for signal_fn, etfs in signal_map.items():
            cols = [e for e in etfs if e in price_data]
            if len(cols) == 0:
                continue
            
            signal_df = pd.DataFrame({
                etf: signal_fn(price_data[etf].loc[start:end])
                for etf in cols
            }).reindex(master_index)
            
            pos = build_long_short_portfolio(
                signal_df,
                returns_df=returns_df[cols],
                portfolio_mode=portfolio_mode,
                win=win,
                long_leverage=long_leverage,
                short_leverage=short_leverage
            )
            
            pnl = compute_portfolio_pnl_with_costs(
                pos,
                returns_df[cols],
                cost_bps=0
            )
            
            pos_list.append(pos)
            pnl_list.append(pnl)
        
        if len(pnl_list) == 0:
            raise ValueError("All signals empty in Mode 3")
        
        n = len(pnl_list)
        positions = sum(
            p.reindex(columns=valid_etfs, fill_value=0)
            for p in pos_list
        ) / n
        pnl = sum(pnl_list) / n
        individual_etf_pnls = positions.shift(1) * returns_df
        
        return pnl, positions, returns_df, individual_etf_pnls
    
    # MODE 1 + 2: original logic
    signal_matrix = {}
    returns_matrix = {}
    
    active_universe = etf_universe if etf_universe else \
                      list(signal_map.keys()) if signal_map else \
                      list(price_data.keys())
    
    for etf in active_universe:
        if etf not in price_data:
            continue
        
        df = price_data[etf].loc[start:end]
        
        if signal_map is not None and etf in signal_map:
            etf_signals = signal_map[etf]
        else:
            etf_signals = signal_functions
        
        if len(etf_signals) == 0:
            signal_matrix[etf] = pd.Series(0.0, index=df.index)
        else:
            sig_df = pd.concat([fn(df) for fn in etf_signals], axis=1)
            signal_matrix[etf] = combine_signals(sig_df, mode=combine_mode, win=win)
        
        returns_matrix[etf] = df["Returns"]
    
    signal_df = pd.DataFrame(signal_matrix)
    returns_df = pd.DataFrame(returns_matrix)
    
    positions = build_long_short_portfolio(
        signal_df,
        returns_df=returns_df,
        portfolio_mode=portfolio_mode,
        win=win,
        long_leverage=long_leverage,
        short_leverage=short_leverage
    )
    
    pnl = compute_portfolio_pnl_with_costs(positions, returns_df, cost_bps=0)
    individual_etf_pnls = positions.shift(1) * returns_df
    
    return pnl, positions, returns_df, individual_etf_pnls


# =========================
# PERFORMANCE REPORTING
# =========================

def perf_stats(pnl_df, pos_df, price_data):
    """Compute per-ETF performance statistics"""
    stats = {}
    for etf in pnl_df.columns:
        r = pnl_df[etf]
        p = pos_df[etf]
        df = price_data[etf]
        
        open_r = compute_open_pnl(p, df)
        bh_r = df["Returns"]
        bh_open_r = df["Open"].pct_change()
        
        stats[etf] = {
            "Sharpe": sharpe(r),
            "OpenSharpe": sharpe(open_r),
            "BHSharpe": sharpe(bh_r),
            "BHOpenSharpe": sharpe(bh_open_r),
            "CAGR": cagr(r),
            "BHCAGR": cagr(bh_r),
            "Vol": r.std() * np.sqrt(252),
            "MaxDD": max_drawdown(r),
            "Turnover": average_turnover(p),
            "Margin": compute_margin(r, p)
        }
    return pd.DataFrame(stats).T


def portfolio_row(pnl_series, pos_df, price_data, start, end):
    """Generate portfolio performance row"""
    r = pnl_series
    
    open_returns = pd.DataFrame({
        etf: price_data[etf].loc[start:end]["Open"].pct_change()
        for etf in pos_df.columns
    })
    
    open_r = (pos_df.shift(1) * open_returns).sum(axis=1)
    portfolio_total_daily_turnover = pos_df.diff().abs().sum(axis=1)
    avg_portfolio_turnover = 100 * portfolio_total_daily_turnover.mean()
    portfolio_margin_val = compute_margin(r, pos_df)
    
    return pd.Series({
        "Sharpe": sharpe(r),
        "OpenSharpe": sharpe(open_r),
        "CAGR": cagr(r),
        "Vol": r.std() * np.sqrt(252),
        "MaxDD": max_drawdown(r),
        "Turnover": avg_portfolio_turnover,
        "Margin": portfolio_margin_val
    })
