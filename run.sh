#!/bin/bash
module load gsl/2.5
for i in {1..5}
do
    for om in  0.2  0.22857143 0.25714286 0.28571429 0.31428571 0.34285714 0.37142857 0.4 
    do
       for s8 in 0.6  0.65714286 0.71428571 0.77142857 0.82857143 0.88571429 0.94285714 1. 
       do 
          python script.py --om=$om --s8=$s8 --n_of_z="Data/redshift_distributions/shear_photoz_stack_${i}.tab"  --filename="results_${i}.txt" 
       done
    done
done


