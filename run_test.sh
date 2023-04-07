#!/bin/bash
module load gsl/2.5
for i in {0..4}
do
  python script.py --om=0.049200 --n_of_z="Data/redshift_distributions/shear_photoz_new_${i}.tab"  --filename="shift_dep_test${i}.txt" 
done
