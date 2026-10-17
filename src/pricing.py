"""Baseline European call/put pricing models for educational/research use."""
import math
import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, q=0.0, kind="call"):
    """European Black–Scholes–Merton value with continuous dividend yield."""
    if min(S, K) <= 0 or T < 0 or sigma < 0:
        raise ValueError("Invalid price, strike, time or volatility")
    if kind not in ("call", "put"):
        raise ValueError("kind must be 'call' or 'put'")
    if T == 0:
        return max(S-K, 0) if kind == "call" else max(K-S, 0)
    if sigma == 0:
        f = S*math.exp((r-q)*T)
        return math.exp(-r*T)*(max(f-K, 0) if kind == "call" else max(K-f, 0))
    d1=(math.log(S/K)+(r-q+0.5*sigma*sigma)*T)/(sigma*math.sqrt(T))
    d2=d1-sigma*math.sqrt(T)
    call=S*math.exp(-q*T)*norm.cdf(d1)-K*math.exp(-r*T)*norm.cdf(d2)
    return float(call if kind == 'call' else call-S*math.exp(-q*T)+K*math.exp(-r*T))

def merton_jump(S, K, T, r, sigma, jump_intensity, jump_mean, jump_vol, q=0.0, kind='call', nmax=120):
    """Merton lognormal jumps: log jump ~ Normal(jump_mean,jump_vol^2)."""
    if jump_intensity < 0 or jump_vol < 0 or nmax < 1: raise ValueError('Invalid jump parameter')
    if T == 0: return black_scholes(S,K,0,r,sigma,q,kind)
    kappa=math.exp(jump_mean+0.5*jump_vol**2)-1
    lt=jump_intensity*T
    if lt == 0: return black_scholes(S,K,T,r,sigma,q,kind)
    # Poisson recurrence, suitable for moderate lambda*T; check truncation mass.
    weight=math.exp(-lt); out=0.; total=0.
    for n in range(nmax):
        sig_n=math.sqrt(sigma*sigma+n*jump_vol*jump_vol/T)
        # Risk-neutral log drift adjustment; use modified q to retain S*exp(-qT) terms.
        q_n=q+jump_intensity*kappa-n*(jump_mean+0.5*jump_vol**2)/T
        out+=weight*black_scholes(S,K,T,r,sig_n,q_n,kind)
        total+=weight
        weight*=lt/(n+1)
    if 1-total>1e-8: raise ValueError('Poisson tail not captured: increase nmax')
    return float(out)

def heston_mc(S, K, T, r, v0, kappa, theta, xi, rho, q=0.0, kind='call', paths=25000, steps=252, seed=42):
    """Full-truncation Euler Heston Monte Carlo; biased at finite dt; for baseline only.
    Returns (estimated price, standard error). Validate convergence before inference.
    """
    if not (-1 <= rho <= 1) or min(v0,kappa,theta,xi) < 0 or T < 0 or paths < 2 or steps < 1:
        raise ValueError('Invalid Heston parameter')
    if T == 0: return black_scholes(S,K,0,r,0,q,kind),0.
    rng=np.random.default_rng(seed)
    dt=T/steps; sqrt_dt=np.sqrt(dt)
    log_s=np.full(paths,np.log(S)); v=np.full(paths,float(v0))
    for _ in range(steps):
        z1=rng.standard_normal(paths); zind=rng.standard_normal(paths)
        z2=rho*z1+np.sqrt(max(0.,1-rho*rho))*zind
        vp=np.maximum(v,0)
        log_s+=(r-q-0.5*vp)*dt+np.sqrt(vp)*sqrt_dt*z1
        v+=kappa*(theta-vp)*dt+xi*np.sqrt(vp)*sqrt_dt*z2
    st=np.exp(log_s)
    payoff=np.maximum(st-K,0) if kind=='call' else np.maximum(K-st,0)
    discounted=np.exp(-r*T)*payoff
    return float(discounted.mean()),float(discounted.std(ddof=1)/np.sqrt(paths))
