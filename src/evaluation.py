"""Simple evaluation helpers. Regime thresholds must be trained on past data only."""
import numpy as np

def errors(actual, predicted):
    a=np.asarray(actual,dtype=float); p=np.asarray(predicted,dtype=float)
    if a.shape != p.shape or a.size == 0: raise ValueError('Require same nonempty shape')
    return {'mae':float(np.mean(np.abs(a-p))), 'rmse':float(np.sqrt(np.mean((a-p)**2))), 'bias':float(np.mean(p-a))}

def classify_regime(vol, low_cut, high_cut):
    """Cutoffs should be computed on a strictly earlier training window."""
    if low_cut >= high_cut: raise ValueError('low_cut must be smaller than high_cut')
    v=np.asarray(vol,dtype=float)
    return np.where(v < low_cut,'calm',np.where(v < high_cut,'normal','stress'))
