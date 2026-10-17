import math
from src.pricing import black_scholes, merton_jump, heston_mc
from src.evaluation import errors, classify_regime

def test_put_call_parity():
    S,K,T,r,q,sigma=100,105,1.2,0.04,0.01,0.25
    c=black_scholes(S,K,T,r,sigma,q,'call')
    p=black_scholes(S,K,T,r,sigma,q,'put')
    assert abs(c-p-(S*math.exp(-q*T)-K*math.exp(-r*T)))<1e-10

def test_zero_jumps_equals_bs():
    a=black_scholes(100,100,1,.03,.2)
    b=merton_jump(100,100,1,.03,.2,0,-.1,.2)
    assert abs(a-b)<1e-12

def test_heston_near_bs_when_variance_constant():
    bs=black_scholes(100,100,1,.03,.2)
    mc,se=heston_mc(100,100,1,.03,.04,2,.04,0,-.5,paths=10000,steps=24,seed=10)
    assert abs(mc-bs)<5*se+.10

def test_error_metrics():
    z=errors([1,2,3],[1,3,2])
    assert z['mae']==2/3
    assert list(classify_regime([.1,.2,.3],.15,.25))==['calm','normal','stress']
