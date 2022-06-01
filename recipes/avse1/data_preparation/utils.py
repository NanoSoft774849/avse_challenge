# -*- coding: utf-8 -*-
'''
Adapted from original code by Clarity Challenge
https://github.com/claritychallenge/clarity
'''

import os
import scipy
import scipy.io
import numpy as np

SPEECH_FILTER = scipy.io.loadmat(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "speech_weight.mat"
    ),
    squeeze_me=True,
)
SPEECH_FILTER = np.array(SPEECH_FILTER["filt"])

def speechweighted_snr(target, noise):
    """Apply speech weighting filter to signals and get SNR."""
    target_filt = scipy.signal.convolve(
        target, SPEECH_FILTER, mode="full", method="fft"
    )
    noise_filt = scipy.signal.convolve(noise, SPEECH_FILTER, mode="full", method="fft")

    # rms of the target after speech weighted filter
    targ_rms = np.sqrt(np.mean(target_filt ** 2))

    # rms of the noise after speech weighted filter
    noise_rms = np.sqrt(np.mean(noise_filt ** 2))

    if noise_rms==0:
        return np.Inf

    sw_snr = np.divide(targ_rms, noise_rms)
    return sw_snr


def sum_signals(signals):
    """Return sum of a list of signals.

    Signals are stored as a list of ndarrays whose size can vary in the first
    dimension, i.e., so can sum mono or stereo signals etc.
    Shorter signals are zero padded to the length of the longest.

    Args:
        signals (list): List of signals stored as ndarrays

    Returns:
        ndarray: The sum of the signals

    """
    max_length = max(x.shape[0] for x in signals)
    return sum(pad(x, max_length) for x in signals)


def pad(signal, length):
    """Zero pad signal to required length.

    Assumes required length is not less than input length.
    """
    assert length >= signal.shape[0]
    return np.pad(
        signal, [(0, length - signal.shape[0])] + [(0, 0)] * (len(signal.shape) - 1)
    )
