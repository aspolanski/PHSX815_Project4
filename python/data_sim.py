#!/usr/bin/env python3

#Default Modules:
import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import os, glob, sys
from tqdm import tqdm
from astropy import units as u

#Other Modules:
import radvel
##### Author: Alex Polanski #####
##### Script to simulate RV data #####


if __name__ == "__main__":

    # Input stuff

    if '-tc' in sys.argv:
        p = sys.argv.index('-tc')
        tc = float(sys.argv[p+1])

    if '-per' in sys.argv:
        p = sys.argv.index('-per')
        per = float(sys.argv[p+1])

    if '-k' in sys.argv:
        p = sys.argv.index('-k')
        k = float(sys.argv[p+1])

    if '-e' in sys.argv:
        p = sys.argv.index('-e')
        e = float(sys.argv[p+1])

    if '-sigma' in sys.argv:
        p = sys.argv.index('-sigma')
        sigma = float(sys.argv[p+1])

    if '-fname' in sys.argv:
        p = sys.argv.index('-fname')
        fname = str(sys.argv[p+1])


    # generate the data
    
    np.random.seed(2021) #For reproducibility 

    x_rv = np.sort(np.random.uniform(low=1,high=100,size=25))

    yerr_rv = sigma


    synth_params = radvel.Parameters(1,basis='per tc e w k')
    synth_params['per1'] = radvel.Parameter(value = per)
    synth_params['tc1'] = radvel.Parameter(value = tc)
    synth_params['e1'] = radvel.Parameter(value = e)
    synth_params['w1'] = radvel.Parameter(value = 0.0)
    synth_params['k1'] = radvel.Parameter(value = k)

    synth_params['dvdt'] = radvel.Parameter(value=0)
    synth_params['curv'] = radvel.Parameter(value=0)

    synth_model = radvel.RVModel(params=synth_params)
    y_rv = synth_model(x_rv)
    np.random.seed(2021) #For reproducibility
    y_rv += yerr_rv * np.random.randn(len(y_rv))


    data = pd.DataFrame({'time':x_rv,'mnvel':y_rv,'errvel':yerr_rv})
    data.to_csv(f"./data/{fname}.csv", index=False)

