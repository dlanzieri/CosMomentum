#!/bin/bash

module load gsl/2.5

for i in {0..4}
do
    for om in  0.1 0.18888889 0.27777778 0.36666667 0.45555556 0.54444444 0.63333333 0.72222222 0.81111111 0.9 
    do
       for s8 in 0.3 0.41111111 0.52222222 0.63333333 0.74444444 0.85555556 0.96666667 1.07777778 1.18888889 1.3  
       do 
          for w0 in -0.33 -0.51555556 -0.70111111 -0.88666667 -1.07222222 -1.25777778 -1.44333333, -1.62888889 -1.81444444 -2.
          do
              python script.py --om=$om --s8=$s8 --w0=$w0 --n_of_z="Data/redshift_distributions/shear_photoz_new_${i}.tab"  --filename="results_${i}.txt" 
          done
       done
    done
done

