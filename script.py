# loading required packages
import ctypes
import numpy as np
from absl import app
from absl import flags


flags.DEFINE_float("s8", 0.8310, "sigma8")
flags.DEFINE_float("om", 0.3156, "omegam")
flags.DEFINE_float("ob", 0.0492, "omegab")
flags.DEFINE_float("h", 0.6727, "h")
flags.DEFINE_float("ns", 0.9645, "ns")
flags.DEFINE_float("w0", -1.0, "w0")
flags.DEFINE_float("wa", 0.0, "wa")

flags.DEFINE_string("n_of_z", "Data/redshift_distributions/shear_photoz_new_0.tab", "filename of redshift distribution")
flags.DEFINE_string("filename", "/gpfsdswork/projects/rech/ykz/ulm75uc/CosMomentum/results.txt", "Output filename")

FLAGS = flags.FLAGS

# os.system("cd cpp_code; make DSS")
lib=ctypes.CDLL("./cpp_code/DSS.so")

# initialising a new universe and its matter content
a_initial = 0.000025
a_final = 1.0

initialise_new_Universe = lib.initialise_new_Universe
initialise_new_Universe.argtypes = [ ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
initialise_new_Universe.restype = None


density_sample_1 = 69.47036304452095/(np.pi*30.0**2) #not used when we compute the shift for galaxy sources
b1_sample_1 = 1.8  #not used when we compute the shift for galaxy sources
b2_sample_1 = 0.0  #not used when we compute the shift for galaxy sources
a0 = 1.26          #not used when we compute the shift for galaxy sources
a1 = 0.28          #not used when we compute the shift for galaxy sources

z = 1.0 # everywhere in this notebook, not used when we compute the shift for galaxy sources


add_projected_galaxy_sample = lib.add_projected_galaxy_sample
add_projected_galaxy_sample.argtypes = [         ctypes.c_int,         ctypes.c_char_p,                    ctypes.c_double,  ctypes.c_double,  ctypes.c_double, ctypes.c_double, ctypes.c_double]
add_projected_galaxy_sample.restype = None

return_lognormal_shift_for_individual_FLASK_bin = lib.return_lognormal_shift_for_individual_FLASK_bin
return_lognormal_shift_for_individual_FLASK_bin.argtypes = [       ctypes.c_double,               ctypes.c_int,            ctypes.c_int]
return_lognormal_shift_for_individual_FLASK_bin.restype = ctypes.c_double




def main(_):
    Omfid = FLAGS.om
    sig8fid = FLAGS.s8
    Obfid = FLAGS.ob
    hfid = FLAGS.h
    nsfid = FLAGS.ns
    w0fid = FLAGS.w0
    wafid = FLAGS.wa
    # Creating second galaxy sample (sources)
    n_of_z_file_str=FLAGS.n_of_z
    n_of_z_file1 = ctypes.c_char_p(n_of_z_file_str.encode('utf-8'))
    initialise_new_Universe(a_initial, a_final, Omfid, Obfid, 0.0, 1.0-Omfid, sig8fid, nsfid, hfid, w0fid, wafid)
    add_projected_galaxy_sample(0, n_of_z_file1, density_sample_1, b1_sample_1, b2_sample_1, a0, a1)
    theta_in_arcmin =1.3223193364400538
    shift_for_sources = return_lognormal_shift_for_individual_FLASK_bin(theta_in_arcmin, 0, 0)
    with open(FLAGS.filename, 'a') as file:
        file.write(str(hfid)+', '+str(Obfid)+', '+ str(nsfid)+' ,'+ str(Omfid)+' , '+ str(sig8fid)+' , '+ str(w0fid)+' ,'+ str(shift_for_sources)+' \n')

if __name__ == "__main__":
    app.run(main)
                   
                  