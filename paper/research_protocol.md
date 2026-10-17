# Research protocol — draft, not completed research

## Main question
Does volatility regime, moneyness, and tenor alter the *out-of-sample* ranking of pricing models?

## Testable hypotheses
- H1: model ranking differs in calm versus stressed periods.
- H2: jump/stochastic-volatility models improve relative accuracy for out-of-the-money contracts during high-volatility regimes.
- H3: gains differ across short and long expiries; complexity is not universally beneficial.
All may be rejected.

## Data specification
Historically timestamped SPY underlying prices; market option bid, ask, strike, expiry, contract type, trade date and time; distributions/dividends, relevant Treasury/OIS risk-free zero rates. Confirm quote permissions and survivorship/selection issues.

## Design
1. Verify data quality; exclude stale, crossed, nonpositive or implausibly wide quotes; log every filter.
2. Specify observable regimes using only information available by each pricing timestamp (lagged realized volatility, VIX if licensed, or an ex-ante state model).
3. Form walk-forward training/testing partitions with an explicit embargo if features overlap.
4. Calibrate each model using only information available at that time; GARCH fit returns only through time t; Heston/Merton calibrations use option observations from training/calibration window, not the held-out contract quotes.
5. Use a consistent discount/dividend convention and parity checks; compare midquote error and bid-ask-adjusted losses separately.
6. Stratify by log moneyness, days to expiry, and regime. Compute MAE, RMSE, absolute percentage error only when well-defined, and error relative to spreads.
7. Report uncertainty through date-clustered block bootstrap or other justified dependence-aware paired comparison; pre-specify multiple-testing control.
8. Include transaction costs, optimizer failures, runtime, parameter instability and sensitivity to filtering choices.

## Important caveats
- SPY **American** options (and dividends) are not exactly priced by the European closed-form baselines. Either explicitly measure this approximation, use compatible European index options or implement American exercise treatment. Never attribute early-exercise error solely to volatility model failure.
- The offline example is synthetic and has no evidential value.
- Historic options quotes are generally not provided through yfinance's current-option-chain interface.
- Full-truncation Euler Heston simulation introduces time discretization bias; production research should use better schemes and documented convergence checks.
- Real option markets reflect volatility risk premia, not simply historical return variance forecasts.

## Outputs
A standalone paper, reproducible scripts, unit tests, model calibration figures, regime-conditional error tables, and transparent negative findings.
