import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

import os

current_dir = os.path.dirname(os.path.abspath(__file__))
plot_folder = os.path.join(current_dir, "..", "results", "plots")

if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)
    print(f"Klasör oluşturuldu: {plot_folder}")

#----------------------------
# Functions for Data Pipeline
#----------------------------

def symbol_generator(M, N):
    # Generate N random symbol stream from the numbers between [0, M-1]
    return np.random.randint(0, M, N)

def constellation_mapping(M, E_b, symbols):
    # Map the symbols to PSK constellation points
    E_s = E_b * np.log2(M) # Energy per symbol
    complex_baseband_symbol = np.sqrt(E_s) * np.exp(1j * 2 * np.pi * symbols / M)
    return complex_baseband_symbol

def awgn_channel(symbols, sigma):
    # Add AWGN noise to the symbol streams
    w_noise = np.random.normal(0, sigma, symbols.shape) + 1j * np.random.normal(0, sigma, symbols.shape)
    return symbols + w_noise

def receiver_mpsk(M, E_b, received_complex_symbols):
    
    E_s = E_b * np.log2(M) # Energy per symbol
    ideal_indices = np.arange(M)
    ideal_constellation_points = constellation_mapping(M, E_b, ideal_indices)
    # minimum distance detection
    decoded_symbols_closest = np.zeros(len(received_complex_symbols))

    received_complex_symbols_row_vec = received_complex_symbols.reshape(1, -1) # reshape for broadcasting
    ideal_constellation_points_column_vec = ideal_constellation_points.reshape(-1, 1) # reshape for broadcasting
    
    distance_matrix = np.abs(received_complex_symbols_row_vec - ideal_constellation_points_column_vec)
    decoded_symbols_closest = np.argmin(distance_matrix, axis=0) # find min dist for each column of 8x100000 matrix

    return decoded_symbols_closest

def theoretical_SER_psk(M, gamma_s):
    SERs = erfc(np.sqrt(gamma_s)*np.sin(np.pi/M))
    return SERs

def symbols_to_bits_converter(M, symbols):
    k = int(np.log2(M))
    # I tried with for loops but this is more preactical way:

    # We want to extract bits from MSB to LSB
    # For M=8, shifts = [2, 1, 0]
    shifts = np.arange(k - 1, -1, -1)
    
    # Broadcast symbols against shifts:
    # 1. Reshape symbols to (N, 1)
    # 2. Right-shift by each value in 'shifts'
    # 3. AND with 1 to get the bit value

    # & 1 operation is like a filter: for example 4 is actually ...0000100. & 1 masks all of the zeros
    bits_matrix = (symbols.reshape(-1, 1) >> shifts) & 1
    
    # Flatten to get a 1D array of bits for Step 8 comparison
    return bits_matrix.flatten()

#-----------------------
# Parameters and Mapping
#-----------------------

N = int(1e5)

E_b = 1 # I chose amplitude 1 for simplicity.
E_s_8 = E_b * np.log2(8) # Energy per symbol for 8-PSK
E_s_16 = E_b * np.log2(16) # Energy per symbol for 16-PSK

SNR_dB_range = np.arange(0, 31, 1)

# Gray Mapping:

binary_mapping = np.array([
    [0,0,0], [0,0,1], [0,1,0], [0,1,1], 
    [1,0,0], [1,0,1], [1,1,0], [1,1,1]
])
gray_mapping = np.array([
    [0,0,0], # s0
    [0,0,1], # s1
    [0,1,1], # s2
    [0,1,0], # s3
    [1,1,0], # s4
    [1,1,1], # s5
    [1,0,1], # s6
    [1,0,0]  # s7
])

# Step 8:
hamming_dist_binary = np.zeros((8, 8))
hamming_dist_gray = np.zeros((8, 8))
for i in range (8):
    for j in range(8):
        hamming_dist_binary[i, j] = np.sum(binary_mapping[i] != binary_mapping[j])
        hamming_dist_gray[i, j] = np.sum(gray_mapping[i] != gray_mapping[j])

#----------------
# Simulation Part
#----------------

empirical_ser_8psk = []
empirical_ser_16psk = []
theoretical_ser_8psk = []
theoretical_ser_16psk = []

expected_ber_binary_8psk = []
expected_ber_gray_8psk = []


for each_db in SNR_dB_range:
    # 1. Calculate Sigma properly
    gamma_s = 10**(each_db/10)
    # n0 = Es / SNR_linear (which is gamma_s)
    sigma_8 = np.sqrt(E_s_8 / (2 * gamma_s))
    sigma_16 = np.sqrt(E_s_16 / (2 * gamma_s))
    
    # --- Part A: SER Analysis for both M=8 and M=16 ---
    transmitted_symbols_8 = symbol_generator(8, N)
    transmitted_symbols_16 = symbol_generator(16, N)

    modulated_symbols_8 = constellation_mapping(8, E_b, transmitted_symbols_8)
    modulated_symbols_16 = constellation_mapping(16, E_b, transmitted_symbols_16)

    noisy_symbols_8 = awgn_channel(modulated_symbols_8, sigma_8)
    noisy_symbols_16 = awgn_channel(modulated_symbols_16, sigma_16)
    
    decoded_symbols_8 = receiver_mpsk(8, E_b, noisy_symbols_8)
    decoded_symbols_16 = receiver_mpsk(16, E_b, noisy_symbols_16)
    
    empirical_symbol_errors_8 = np.sum(decoded_symbols_8 != transmitted_symbols_8)
    empirical_symbol_errors_16 = np.sum(decoded_symbols_16 != transmitted_symbols_16)
    
    empirical_ser_8psk.append(empirical_symbol_errors_8 / N)
    empirical_ser_16psk.append(empirical_symbol_errors_16 / N)

    theoretical_symbol_errors_8 = theoretical_SER_psk(8, gamma_s)
    theoretical_symbol_errors_16 = theoretical_SER_psk(16, gamma_s)

    theoretical_ser_8psk.append(theoretical_symbol_errors_8)
    theoretical_ser_16psk.append(theoretical_symbol_errors_16)


    # Step 6:
    transmit_symbol_zeros = np.zeros(N)
    symbol_zeros_complex_baseband = constellation_mapping(8, E_b, transmit_symbol_zeros)
    noisy_symbol_zeros_complex_baseband = awgn_channel(symbol_zeros_complex_baseband, sigma_8)
    received_symbol_zeros_complex = receiver_mpsk(8, E_b, noisy_symbol_zeros_complex_baseband)

    # Here I calculated only for s_0 since The probability of mistaking 
    # s_0 for its neighbor s_1 is exactly the same as mistaking s_1 for its neighbor s_2
        
    P_0j = np.zeros(8)

    for j in range(8):
        P_0j[j] = np.sum(received_symbol_zeros_complex == j) / N

    # Step 7:
    P_ij = np.zeros((8, 8))

    for i in range(8):
        P_ij[i, :] = np.roll(P_0j, i)

    expected_ber_binary = np.sum(P_ij * hamming_dist_binary) / (3 * 8)
    expected_ber_gray = np.sum(P_ij * hamming_dist_gray) / (3 * 8)

    expected_ber_binary_8psk.append(expected_ber_binary)
    expected_ber_gray_8psk.append(expected_ber_gray)

#-----------------
#  Part A Plots
#-----------------

plt.figure(figsize=(8, 8))

# 1. Theoretical SER
plt.semilogy(SNR_dB_range, theoretical_ser_8psk, 'ko', label='Theoretical SER M=8', markersize=4)
plt.semilogy(SNR_dB_range, theoretical_ser_16psk, 'ro', label='Theoretical SER M=16', markersize=4)

# 2. Empirical SER
plt.semilogy(SNR_dB_range, empirical_ser_8psk, 'k-', label='Empirical SER M=8', linewidth=1.5)
plt.semilogy(SNR_dB_range, empirical_ser_16psk, 'r-', label='Empirical SER M=16', linewidth=1.5)

plt.grid(True, which='both', linestyle='--')
plt.xlabel('SNR (dB)')
plt.ylabel('Error Rate') # PDF uses "Error Rate"
plt.ylim([1e-5, 1.2]) 
plt.xlim([0, 30])

# Place legend without blocking data
plt.legend(loc='best')

# Save and Show
plot_path = os.path.join(plot_folder, "PartA_SER_Comparison.png")
plt.savefig(plot_path)

#-----------------
#  Part B Plots
#-----------------

# 1. 8-PSK Expected BERs

plt.figure(figsize=(8, 8))

plt.semilogy(SNR_dB_range, expected_ber_binary_8psk, 'ko', label='Binary Code Mapping BER', markersize=4)
plt.semilogy(SNR_dB_range, expected_ber_gray_8psk, 'rs', label='Gray Code Mapping BER', markersize=4)

plt.grid(True, which='both', linestyle='--')
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.legend()
plt.ylim([1e-5, 1.2])
plt.xlim([0, 30])

plt.savefig(os.path.join(plot_folder, "PartB_BER_Comparison_Mappings.png"))


