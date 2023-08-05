#!/usr/bin/python
# coding: UTF-8
#
# Author:   Dawid Laszuk
# Contact:  laszukdawid@gmail.com
#
# Feel free to contact for any information.
"""
.. currentmodule:: EEMD
"""

from __future__ import print_function

import logging
import numpy as np

class EEMD:
    """
    **Ensemble Empirical Mode Decomposition**

    Ensemble empirical mode decomposition (EEMD) [Wu2009]_
    is noise-assisted technique, which is meant to be more robust
    than simple Empirical Mode Decomposition (EMD). The robustness is
    checked by performing many decompositions on signals slightly
    perturbed from their initial position. In the grand average over
    all IMF results the noise will cancel each other out and the result
    is pure decomposition.

    Parameters
    ----------
    trials : int (default: 100)
        Number of trails or EMD performance with added noise.
    noise_width : float (default: 0.05)
        Standard deviation of Gaussian noise (:math:`\hat\sigma`).
        It's relative to absolute amplitude of the signal, i.e.
        :math:`\hat\sigma = \sigma\cdot|\max(S)-\min(S)|`, where
        :math:`\sigma` is noise_width.
    ext_EMD : EMD (default: None)
        One can pass EMD object defined outside, which will be
        used to compute IMF decompositions in each trial. If none
        is passed then EMD with default options is used.

    References
    ----------
    .. [Wu2009] Z. Wu and N. E. Huang, "Ensemble empirical mode decomposition:
        A noise-assisted data analysis method", Advances in Adaptive
        Data Analysis, Vol. 1, No. 1 (2009) 1-41.
    """

    logger = logging.getLogger(__name__)

    noise_kinds_all = ["normal", "uniform"]

    def __init__(self, trials=100, noise_width=0.05, ext_EMD=None, **kwargs):

        # Ensemble constants
        self.trials = trials
        self.noise_width = noise_width

        self.noise_kind = "normal"

        if ext_EMD is None:
            from PyEMD import EMD
            self.EMD = EMD()
        else:
            self.EMD = ext_EMD

        #TODO: Test this!
        # Update based on options
        for key in kwargs.keys():
            if key in self.__dict__.keys():
                self.__dict__[key] = kwargs[key]
            elif key in self.EMD.__dict__.keys():
                self.EMD.__dict__[key] = kwargs[key]

    def __call__(self, S, T=None, max_imf=-1):
        return self.eemd(S, T=T, max_imf=max_imf)

    def generate_noise(self, scale, size):
        """
        Generate noise with specified parameters.

        All distributions are zero centred. For types of distributions
        see :`self.noise_kinds_all`.

        .. py:attribute:: EEMD.noise_kinds_all

        Parameters
        ----------
        scale : float
            Width for the distribution.
        size : int
            Number of generated samples.

        Returns
        -------
        noise : numpy array
            Noise sampled from selected distribution.
        """

        if self.noise_kind=="normal":
            noise = np.random.normal(loc=0, scale=scale, size=size)
        elif self.noise_kind=="uniform":
            noise = np.random.uniform(low=-scale/2, high=scale/2, size=size)
        else:
            raise ValueError("Unsupported noise kind. Please assigned `noise_kind`"
                + " to be one of these: " + str(self.noise_kinds_all))

        return noise

    def eemd(self, S, T=None, max_imf=-1):
        """
        Performs EEMD on provided signal.

        For a large number of iterations defined by `trails` attr
        the method performs :py:meth:`emd` on a signal with added white noise.

        Parameters
        ----------
        S : numpy array,
            Input signal on which EEMD is performed.
        T : numpy array, (default: None)
            If none passed samples are numerated.
        max_imf : int, (default: -1)
            Defines up to how many IMFs each decomposition should
            be performed. By default (negative value) it decomposes
            all IMFs.

        Returns
        -------
        eIMF : numpy array
            Set of ensemble IMFs produced from input signal. In general,
            these do not have to be, and most likely will not be, same as IMFs
            produced using EMD.
        """
        if T is None: T = np.arange(len(S), dtype=S.dtype)

        N = len(S)
        E_IMF = np.zeros((1,N))

        scale = self.noise_width*np.abs(np.max(S)-np.min(S))

        # For trail number of iterations perform EMD on a signal
        # with added white noise
        for trial in range(self.trials):
            self.logger.debug("trial: "+str(trial))

            # Generate noise
            noise = self.generate_noise(scale, N)

            IMFs = self.emd(S+noise, T, max_imf)
            imfNo = IMFs.shape[0]

            # If new decomposition has more IMFs than any previous
            # then add empty rows (holders)
            while(E_IMF.shape[0] < imfNo):
                E_IMF = np.vstack((E_IMF, np.zeros(N)))

            E_IMF[:imfNo] += IMFs

        E_IMF /= self.trials

        return E_IMF

    def emd(self, S, T, max_imf=-1):
        """Reference to emd method of passed EMD class."""
        return self.EMD.emd(S, T, max_imf)

###################################################
## Beginning of program

if __name__ == "__main__":

    import pylab as plt

    # Logging options
    logging.basicConfig(level=logging.INFO)

    # EEMD options
    PLOT = 0
    INTERACTIVE = 1
    REPEATS = 1

    max_imf = -1

    # Signal options
    N = 500
    tMin, tMax = 0, 2*np.pi
    T = np.linspace(tMin, tMax, N)

    S = 3*np.sin(4*T) + 4*np.cos(9*T) + np.sin(8.11*T+1.2)

    # Prepare and run EEMD 
    eemd = EEMD()
    eemd.trials = 50

    E_IMFs = eemd.eemd(S, T, max_imf)
    imfNo  = E_IMFs.shape[0]

    # Plot results in a grid
    c = np.floor(np.sqrt(imfNo+1))
    r = np.ceil( (imfNo+1)/c)

    plt.ioff()
    plt.subplot(r,c,1)
    plt.plot(T, S, 'r')
    plt.xlim((tMin, tMax))
    plt.title("Original signal")

    for num in range(imfNo):
        plt.subplot(r,c,num+2)
        plt.plot(T, E_IMFs[num],'g')
        plt.xlim((tMin, tMax))
        plt.title("Imf "+str(num+1))

    plt.show()
