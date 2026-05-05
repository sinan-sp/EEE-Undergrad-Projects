import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from scipy.linalg import toeplitz

import os

# ========================================
# Prepare the necessary files / functions
# ========================================

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data")

try:
    df_small = pd.read_csv(os.path.join(data_dir, 'dataset_small.csv'))
    df_large = pd.read_csv(os.path.join(data_dir, 'dataset_large.csv'))
    df_test = pd.read_csv(os.path.join(data_dir, 'dataset_test.csv'))
    print("Datasets loaded successfully via relative paths.")
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure CSV files are in the ../data/ directory.")

# B. Theoretical Autocorrelation Function (r_k)
def get_theoretical_rk(k):
    """
    Calculates the theoretical autocorrelation by using Sinc Function.
    It depends on only the k value in a WSS process.
    """
    if k == 0:
        return 1.0
    numerator = np.sin(0.1 * np.pi * k)
    denominator = 0.1 * np.pi * k
    return numerator / denominator

# C. Empirical Autocorrelation Function (r_k)
def estimate_rk(df):
    """
    Estimate r_k k=[0, 6] from the given dataset.
    It takes the average of appropriate pairs by assuming WSS.
    """
    n_features = 7
    rk_estimates = []
    
    # Calculate for each k lag
    for k in range(n_features):
        pairs_sum = 0
        count = 0
        
        # Sum all X_i * X_{i+k} pairs in the vector:
        for i in range(1, n_features - k + 1):
            col_a = f'X{i}'
            col_b = f'X{i+k}'
            pairs_sum += (df[col_a] * df[col_b]).sum()
            count += len(df)
            
        rk_estimates.append(pairs_sum / count)
        
    return np.array(rk_estimates)

# D. LMMSE weights calculator:
def compute_lmmse_weights(rk_sequence, n):
    """
    Calculates LMMSE weights for n observations.
    rk_sequence: r0, r1, ..., r6
    """
    # 1. RY Matrix from (Observations: X2, X3, ..., Xn+1)
    # n=1   =>  [r0],   n=2   =>  [[r0, r1], [r1, r0]]
    first_col = rk_sequence[:n]
    RY = toeplitz(first_col)
    # 2. rX1Y vector from (X1 and X2...Xn+1 correlation)
    # Distances are like 1, 2, ..., n   =>  it starts from r1.
    rX1Y = rk_sequence[1:n+1]
    # 3. Wiener-Hopf solution:  (RY * a = rX1Y)
    a_vector = np.linalg.solve(RY, rX1Y)
    return a_vector

# ==================================
# Part 1: Autocorrelation Estimation
# ==================================

# We need r for k = [0, 6].
k_values = np.arange(0, 7)
theoretical_correlations = [get_theoretical_rk(k) for k in k_values]

print("\nTheoretical r_k values for k = [0, 6]:")
for k, val in enumerate(theoretical_correlations):
    print(f"r_{k}: {val:.4f}")

# Check the small dataset:
print(f"\nSmall Dataset dimensions: {df_small.shape}")
print("First 5 rows of [X1, X7]:")
print(df_small.head())

# 1a) Calculate the estimates
r_hat_small = estimate_rk(df_small)

# 1b) Calculate large dataset
r_hat_large = estimate_rk(df_large)


# Show the comparison results:
print("\nLag (k) | Theoretical | Empirical (Small)")
print("-" * 45)
for k in range(7):
    theory = theoretical_correlations[k]
    small = r_hat_small[k]
    print(f"  {k}     |   {theory:7.4f}   |   {small:7.4f}")

# 1c) Plotting the Results

plt.figure(figsize=(6, 6)) # Square figure

plt.plot(k_values, theoretical_correlations, label='True Sequence', 
         marker='o', linestyle='-', linewidth=2, color='black')

plt.plot(k_values, r_hat_small, label='Small Dataset Estimate', 
         marker='s', linestyle='--', alpha=0.8)

plt.plot(k_values, r_hat_large, label='Large Dataset Estimate', 
         marker='^', linestyle='--', alpha=0.8)

plt.xlabel('Lag (k)')
plt.ylabel('Autocorrelation ($r_k$)')
plt.xticks(k_values)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()

plot_path = os.path.join(plot_dir, "part1c_autocorrelation_comparison.png")
plt.savefig(plot_path)
print(f"Grafik kaydedildi: {plot_path}")

# ===================================
# Part 2: Data-Driven LMSE Estimation
# ===================================
# Save the weights for each.
# For example a_r_large_dict[n] gives the REAL weights from n observations.

a_r_large_dict = {}

print("--- Weights ---")
for n in range(1, 7):
    a_r_large_dict[n] = compute_lmmse_weights(r_hat_large, n)
    print(f"weights for n={n}: {a_r_large_dict[n]}")

# Convert the dataset test.csv. to matrix form for simplicity:
# Columns' names:   X1, X2, ..., X7
X_test_matrix = df_test[[f'X{i}' for i in range(1, 8)]].values

# Real X1 values:
X1_true = X_test_matrix[:, 0]

# Observation vectors from X2 to X7:     Y(n) = [X2, ..., Xn+1]
Y_test_full = X_test_matrix[:, 1:]

empirical_mse_large = []

print("\n--- Empirical MSE (for the Large Estimator) ---")

for n in range(1, 7):
    # Take the weigths from Part 2b:
    a_n = a_r_large_dict[n]
    
    # Take the n observations (first n columns)
    # Y_test.shape: (1000, n)
    Y_n = Y_test_full[:, :n]
    
    # Prediction: X_hat = Y * a
    X1_pred = Y_n @ a_n
    
    # Calculate MSE: mean((X1 - X1_hat)^2)
    mse = np.mean((X1_true - X1_pred)**2)
    empirical_mse_large.append(mse)
    
    print(f"n={n} for Test MSE: {mse:.6e}")

# Store the results:
mse_results = {
    'n': np.arange(1, 7),
    'empirical_mse_large': empirical_mse_large
}

# ===================================
# Part 3: Ideal LMSE Estimation
# ===================================

# 3a) Derive exact optimal filter weights a(n) using true rk
a_ideal_dict = {}
for n in range(1, 7):
    a_ideal_dict[n] = compute_lmmse_weights(theoretical_correlations, n)

# 3b-c) Apply weights to test data and calculate empirical MSE
empirical_mse_ideal = []

print("\n--- Part 3c: Empirical MSE (Ideal Estimator) ---")
for n in range(1, 7):
    a_n_ideal = a_ideal_dict[n]
    Y_n = Y_test_full[:, :n] # use the converted matrix from dataset test.csv.
    
    # Estimate X1 using ideal weights
    X1_pred_ideal = Y_n @ a_n_ideal
    
    # Calculate MSE
    mse_ideal = np.mean((X1_true - X1_pred_ideal)**2)
    empirical_mse_ideal.append(mse_ideal)
    print(f"n={n} for Ideal Test MSE: {mse_ideal:.6e}")

mse_results['empirical_mse_ideal'] = empirical_mse_ideal

# ==========================================
# Part 4: Theoretical vs. Empirical Analysis
# ==========================================

# 4a) Calculate the exact theoretical MSE eL*(n)
# Formula: eL*(n) = r0 - R_XY^T * inv(R_Y) * R_XY
theoretical_mse_bounds = []

r0 = theoretical_correlations[0]

for n in range(1, 7):
    # Construct true RY and rX1Y
    first_col = theoretical_correlations[:n]
    RY_true = toeplitz(first_col)
    rX1Y_true = np.array(theoretical_correlations[1:n+1])
    
    # eL*(n) Calculation
    # Note: R_XY^T * inv(RY) * R_XY is equivalent to rX1Y^T * a_ideal
    min_mse = r0 - rX1Y_true.T @ a_ideal_dict[n]
    theoretical_mse_bounds.append(min_mse)

# 4b) Final Plotting
plt.figure(figsize=(6, 6))

n_axis = np.arange(1, 7)

# 1. Theoretical Bound
plt.plot(n_axis, theoretical_mse_bounds, label='Theoretical MSE', 
         color='black', marker='o', linewidth=2)

# 2. Empirical MSE with True Stats (Part 3)
plt.plot(n_axis, empirical_mse_ideal, label='Empirical MSE using True Autoorrelation Seq.', 
         linestyle='--', marker='x', color='red')

# 3. Empirical MSE with Estimated Stats (Part 2)
plt.plot(n_axis, empirical_mse_large, label='Empirical MSE using Estimated Autoorrelation Seq.', 
         linestyle='-.', marker='s', color='blue')

# Formatting according to general rules
plt.yscale('log')
plt.ylim(bottom=1e-10) # Set minimum y-axis limit to 10^-10 
plt.xlabel('Number of Observations (n)')
plt.ylabel('Mean Square Error ($e_L$)')
plt.grid(True, which="both", linestyle=':', alpha=0.6) # Enable grid
plt.legend()
plt.tight_layout()

final_plot_path = os.path.join(plot_dir, "part4b_mse_comparison.png")
plt.savefig(final_plot_path)
print(f"\nFinal comparison plot saved: {final_plot_path}")



