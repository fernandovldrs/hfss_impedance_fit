import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c
from scipy.optimize import curve_fit

L = 6e-3 # Transmission line length in meters
def zin_function(f, Z0, epsilonr):
    return -Z0 / np.tan(2*np.pi/c*np.sqrt(epsilonr) * f * L)

f = open("z_in.txt", "r")
f_str = f.read()

data_lines = f_str.split('\n')[7:]
freq_list = []
imag_zin_list = []
for data_line in data_lines:
    split_data_line = data_line.split()
    if len(split_data_line) > 0:
        freq_list.append(float(split_data_line[0])*1e9)
        imag_zin_list.append(float(split_data_line[2]))
    
guess = [120, 3.3]
params, covariance = curve_fit(zin_function, freq_list[:400], imag_zin_list[:400], p0=guess)
print(params)

plt.scatter(np.array(freq_list)/1e9, np.abs(imag_zin_list), s=2)
plt.plot(np.array(freq_list)/1e9, [np.abs(zin_function(f, *params)) for f in freq_list], label = f"Z0 = {params[0]:.1f} Ohm\n epsilonr = {params[1]:.2f}")
plt.yscale('log')
plt.ylabel("|Zin| (Ohm)")
plt.xlabel("Frequency (GHz)")
plt.grid()
plt.legend()
plt.show()