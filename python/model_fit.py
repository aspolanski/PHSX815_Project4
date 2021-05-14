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
from scipy import optimize
##### Author: Alex Polanski #####
#####  #####



if __name__ == "__main__":

    #input stuff

    if '-fname' in sys.argv:
        p = sys.argv.index('-fname')
        fname = str(sys.argv[p+1])

    #read in the data

    data = pd.read_csv(f"./data/{fname}.csv")
    

    def initialize_model(e):
        time_base = 0.0
        params = radvel.Parameters(1,basis='per tp e w k')
        params['per1'] = radvel.Parameter(value=6)
        params['tp1'] = radvel.Parameter(value=2)
        params['e1'] = radvel.Parameter(value=e)
        params['w1'] = radvel.Parameter(value=0.0)
        params['k1'] = radvel.Parameter(value=10.1)
    
        mod = radvel.RVModel(params, time_base=time_base)
        mod.params['dvdt'] = radvel.Parameter(value=-0.0)
        mod.params['curv'] = radvel.Parameter(value=0.0)
        return mod






    #Initialize a likelihood function

    mod = initialize_model(0.5)

    like = radvel.likelihood.RVLikelihood(mod, data['time'], data['mnvel'], data['errvel'])

    like.params['gamma'] = radvel.Parameter(value=0.0, vary=False)
    like.params['jit'] = radvel.Parameter(value=1.0,vary=True)

    like.params['per1'].vary = True
    like.params['tp1'].vary = True
    like.params['k1'].vary = True
    like.params['e1'].vary = True
    like.params['w1'].vary = False


    like.params['dvdt'] = radvel.Parameter(value=0.0, vary=False)
    like.params['curv'] = radvel.Parameter(value=0.0, vary=False)

    post = radvel.posterior.Posterior(like)
    post.priors += [radvel.prior.EccentricityPrior(1, upperlims=0.99)]
    
    res  = optimize.minimize(
        post.neglogprob_array,
        post.get_vary_params(),
        method='Nelder-Mead',
        )
    
    print(post)
    #print(like.aic())
    ecc_aic = like.aic()


    # Now do the same for an orbit with eccentricity fixed at 0.

    mod = initialize_model(0.0)

    like = radvel.likelihood.RVLikelihood(mod, data['time'], data['mnvel'], data['errvel'])

    like.params['gamma'] = radvel.Parameter(value=0.0, vary=False)
    like.params['jit'] = radvel.Parameter(value=1.0,vary=True)

    like.params['per1'].vary = True
    like.params['tp1'].vary = True
    like.params['k1'].vary = True
    like.params['e1'].vary = False
    like.params['w1'].vary = False

    like.params['dvdt'] = radvel.Parameter(value=0.0, vary=False)
    like.params['curv'] = radvel.Parameter(value=0.0, vary=False)
    
    post = radvel.posterior.Posterior(like)
    #post.priors += [radvel.prior.EccentricityPrior(1, upperlims=0.99)]
    res  = optimize.minimize(
        post.neglogprob_array,
        post.get_vary_params(),
        method='Nelder-Mead',
        )

    print(post)
    #print(like.aic())
    circ_aic = like.aic()

    print(f'Model Comparison:\nWith Eccentricity: {ecc_aic:0.4} \nNo Eccentricity: {circ_aic:0.4} \nDelta AIC:{np.abs(circ_aic-ecc_aic):0.4}')




