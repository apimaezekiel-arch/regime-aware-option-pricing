# Regime-Aware Volatility Modeling and Option Pricing

**Research portfolio | Ezekiel Apima Onchong'a | MSc Financial Engineering (in progress)**

> **Status: research in development.** The notebook currently uses **synthetic demonstration data**, not observed option trades. No results in this repository should be interpreted as empirical findings.

## Research question
Does the relative performance of GARCH-informed Black–Scholes, Heston stochastic-volatility, and Merton jump-diffusion pricing vary by volatility regime, option maturity, and moneyness?

## Original research angle (to test, not assume)
Compare model pricing errors **out of sample** conditional on market regimes, including volatility asymmetry and potential interactions between jump risk, tenor, and moneyness. Investigate whether additional complexity materially improves results after transaction-cost and calibration-stability considerations.

## Repository map
- `notebooks/01_pricing_basics.ipynb` — runs offline with synthetic illustrative inputs; compares three pricing models.
- `src/pricing.py` — Black–Scholes, Merton jump-diffusion, Heston Monte Carlo.
- `src/evaluation.py` — errors and volatility-regime labels.
- `tests/` — checks against pricing identities and simulation sanity.
- `paper/research_protocol.md` — study design, biases, empirical evaluation plan.
- `data/README.md` — real-data sourcing and licensing notes.

## Quick start
```bash
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
jupyter lab notebooks/01_pricing_basics.ipynb
```
Run from the **repository root**. Notebook code includes a path setup for imports.

## Data policy
Do not commit licensed market-data extracts or personal credentials. The offline notebook uses no external data. A later empirical phase will use legally sourced historical underlying prices, risk-free curves, dividends, and timestamped bid/ask options quotes. Historical options quotes are **not** available in general from `yfinance`'s current-chain endpoint; this requires an appropriate historical options source.

## Proposed evaluation
Walk-forward estimation; no look-ahead; identical observation timestamps; midquote filters and bid-ask-aware evaluation; regimes determined only by *lagged* observables; RMSE/MAE plus paired uncertainty estimates; benchmark model calibration budgets and stability checks. See `paper/research_protocol.md`.

## License & citation
MIT-licensed code. Research manuscript and underlying data may have different rights. See `CITATION.cff`.
