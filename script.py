# loading required packages
import ctypes
import numpy as np
from absl import app
from absl import flags


flags.DEFINE_float("s8", 0.8, "sigma8")
flags.DEFINE_float("om", 0.3, "omegam")
flags.DEFINE_string("n_of_z", "Data/redshift_distributions/shear_photoz_stack.tab", "filename of redshift distribution")
flags.DEFINE_string("filename", "/gpfsdswork/projects/rech/ykz/ulm75uc/CosMomentum/results.txt", "Output filename")

FLAGS = flags.FLAGS

# os.system("cd cpp_code; make DSS")
lib=ctypes.CDLL("./cpp_code/DSS.so")

# initialising a new universe and its matter content
a_initial = 0.000025
a_final = 1.0

initialise_new_Universe = lib.initialise_new_Universe
# initialise_new_Universe          (double a_initial,  double a_final,  double Omega_m,  double Omega_b,  double Omega_r,  double Omega_L,  double sigma_8,      double n_s,    double h_100,       double w0,       double w1)
initialise_new_Universe.argtypes = [ ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
initialise_new_Universe.restype = None

# Fiducial cosmology
Omfid = 0.3075
Obfid = 0.0486 
hfid = 0.6774 
nsfid = 0.9667 
sig8fid = 0.8159


density_sample_1 = 69.47036304452095/(np.pi*30.0**2)
b1_sample_1 = 1.8
b2_sample_1 = 0.0
a0 = 1.26
a1 = 0.28

z = 1.0 # everywhere in this notebook


add_projected_galaxy_sample = lib.add_projected_galaxy_sample
add_projected_galaxy_sample.argtypes = [         ctypes.c_int,         ctypes.c_char_p,                    ctypes.c_double,  ctypes.c_double,  ctypes.c_double, ctypes.c_double, ctypes.c_double]
add_projected_galaxy_sample.restype = None

return_lognormal_shift_for_individual_FLASK_bin = lib.return_lognormal_shift_for_individual_FLASK_bin
return_lognormal_shift_for_individual_FLASK_bin.argtypes = [       ctypes.c_double,               ctypes.c_int,            ctypes.c_int]
return_lognormal_shift_for_individual_FLASK_bin.restype = ctypes.c_double

# Creating first galaxy sample (lenses)
n_of_z_file_str = 'Data/redshift_distributions/pofz_Y1_redMaGiC_bin4.dat'
n_of_z_file1 = ctypes.c_char_p(n_of_z_file_str.encode('utf-8'))



def main(_):
    Omfid = FLAGS.om
    sig8fid = FLAGS.s8
    # Creating second galaxy sample (sources)
    n_of_z_file_str=FLAGS.n_of_z
    n_of_z_file2 = ctypes.c_char_p(n_of_z_file_str.encode('utf-8'))
    initialise_new_Universe(a_initial, a_final, Omfid, Obfid, 0.0, 1.0-Omfid, sig8fid, nsfid, hfid, -1.0, 0.0)
    add_projected_galaxy_sample(0, n_of_z_file1, density_sample_1, b1_sample_1, b2_sample_1, a0, a1)
    add_projected_galaxy_sample(0, n_of_z_file2, density_sample_1, b1_sample_1, b2_sample_1, a0, a1)
    l_max = 10000
    theta_in_arcmin = 5.0
    bias = 2.0
    r = 0.95
    index_of_lens_sample = 0
    index_of_source_sample = 1

    shift_for_sources = return_lognormal_shift_for_individual_FLASK_bin(theta_in_arcmin, 1, 0)
    with open(FLAGS.filename, 'a') as file:
        file.write(str(Omfid)+', '+str(sig8fid)+', '+ str(shift_for_sources)+' \n')

if __name__ == "__main__":
    app.run(main)