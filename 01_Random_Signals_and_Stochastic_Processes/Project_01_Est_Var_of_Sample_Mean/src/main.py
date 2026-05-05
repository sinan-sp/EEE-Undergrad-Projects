import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import os

current_dir = os.path.dirname(os.path.abspath(__file__))


plot_folder = os.path.join(current_dir, "..", "results", "plots")

if not os.path.exists(plot_folder):
    os.makedirs(plot_folder)
    print(f"Klasör oluşturuldu: {plot_folder}")

distributions = {
    'Gaussian': stats.norm(loc=2, scale=2),
    'Exponential': stats.expon(scale=2),
    'Uniform': stats.uniform(loc=2 - np.sqrt(48)/2, scale=np.sqrt(48))
}


distribution_names = ['Gaussian', 'Exponential', 'Uniform'] # in order to access the dictionary above
n_values = np.array([10, 20, 30, 50, 70, 100]) # Sample sizes as array
N_values = np.array([10, 100, 1000, 10000]) # Number of repetitions as array

# Storages of the for loop below

empirical_variances = np.zeros((len(distribution_names), len(n_values), len(N_values))) # (Distributions, n-sample_sizes, N-repetitions)
theoretical_variances = np.zeros(len(n_values)) # for each sample size
sample_means_size100 = np.empty((len(distribution_names), len(N_values)), dtype=object) # sample size 100 için storage

for d_idx, d_name in enumerate(distribution_names):
    distribution = distributions[d_name]
    
    for n_idx, n in enumerate(n_values):
        theoretical_variances[n_idx] = 4 / n #store it above
        
        for N_idx, N in enumerate(N_values):
                
            # Generate samples as n x N matrices
            samples = distribution.rvs(size=(n, N))
            
            # Calculate mean of each column
            sample_means = samples.mean(axis=0)
            if n == 100:
                sample_means_size100[d_idx, N_idx] = sample_means #store it above

            empirical_variances[d_idx, n_idx, N_idx] = np.var(sample_means) #store it above

#-------
# Step 7
#-------

# Constants for n=100
mu = 2
var_Mn = 4 / 100
std_Mn = np.sqrt(var_Mn) # 0.2

# Define the interval limits (1.96 standard deviations for 95% confidence)
k = 1.96 
lower_bound = mu - k * std_Mn # 1.608
upper_bound = mu + k * std_Mn # 2.392

# If we wouldnt know the exact distributions of N repetitions yields Gaussian, then by Chebyshev Inequality:
chebyshev_bound = (1 - (1 / (k**2))) * 100
print(f"Theoretical Chebyshev Lower Bound: > {chebyshev_bound:.2f}%\n")

# From Central Limit Theorem we can use Gaussian:
for d_idx, d_name in enumerate(distribution_names):
    data = sample_means_size100[d_idx, 2] # Accessing the N=1000 array
    
    # Count how many means fall within the [1.608, 2.392] interval
    inside_interval = (data >= lower_bound) & (data <= upper_bound)
    empirical_percentage = np.mean(inside_interval) * 100
    
    print(f"{d_name} Empirical % in Interval: {empirical_percentage:.2f}%")

#-----------------
#   PLOTTING
#-----------------

#   -------
#   Part A
#   -------

for d_idx, d_name in enumerate(distribution_names):
    # For each distribution (e.g., Gaussian) crete the Figures:
    plt.figure(num=d_idx, figsize=(6, 6))

    for N_idx, N_val in enumerate(N_values):
        plt.plot(n_values, empirical_variances[d_idx, :, N_idx], label=f'N={N_val}') # sample size vs. Empirical Variance

    plt.plot(n_values, theoretical_variances, 'ko', label='Theoretical (4/n)') # add theoretical values

    plt.xlabel('Sample Size ($n$)')
    plt.ylabel(f'Estimation Variance ($Var[M_n]$) of {d_name} RV')
    plt.legend(loc='best')
    plt.grid(True)
    
    file_name = f"Variance_Plot_{d_name}.png"
    save_path = os.path.join(plot_folder, file_name)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

#   -------
#   Part B
#   -------

for d_idx, d_name in enumerate(distribution_names):
    # For each distribution (e.g., Gaussian) crete the Figures:
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten() # Convert the matrix into a 1D list for easy looping

    for N_idx, N_val in enumerate(N_values):
        
        ax = axes[N_idx]
        
        ax.hist(sample_means_size100[d_idx, N_idx], bins=30, density=True, alpha=0.6, color='skyblue')
        
        x_range = np.linspace(1, 3, 200)

        theoretical_gaussian_pdf = stats.norm.pdf(x_range, loc=2, scale=0.2) # this is the pdf for EV 2 and standart error 0.2
        ax.plot(x_range, theoretical_gaussian_pdf, 'r-', lw=2, label='Theoretical Gaussian')
        ax.set_xlim(1.2, 2.8)

        # 5. Legend for each subplot
        ax.set_xlabel('Sample Mean ($M_n$)')
        ax.set_ylabel('Probability Density')
        ax.legend(fontsize='small')      
    
        # 3. Add labels and grid
        ax.set_title(f'N = {N_val}')
        ax.grid(True)

    plt.tight_layout()
    file_name = f"Histogram_{d_name}.png"
    save_path = os.path.join(plot_folder, file_name)

    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

