{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Central Limit Theorem and Variance Convergence Analysis\
\
## Project Overview\
This project provides a computational verification of the **Central Limit Theorem (CLT)** and the **Law of Large Numbers**. By simulating various random variables, it demonstrates how the distribution of sample means tends toward a Gaussian distribution regardless of the original distribution's shape, provided the sample size ($n$) is sufficiently large[cite: 2].\
\
## Key Technical Objectives\
*   **Empirical Variance Analysis:** Investigating how the variance of the sample mean ($Var[M_n]$) scales with sample size $n$, comparing it against the theoretical $1/n$ relationship[cite: 2].\
*   **CLT Visualization:** Plotting histograms of sample means for different repetition counts ($N$) to observe the convergence to a Normal distribution[cite: 2].\
*   **Probabilistic Bounds:** Evaluating the accuracy of **Chebyshev\'92s Inequality** and Gaussian-based confidence intervals in predicting the behavior of sample means[cite: 2].\
\
## Methodology & Implementations\
The simulation uses three distinct probability distributions, all configured with a mean ($\\mu$) of 2 and variance ($\\sigma^2$) of 4[cite: 2]:\
1.  **Gaussian Distribution:** $N(2, 4)$[cite: 2]\
2.  **Exponential Distribution:** $\\lambda = 0.5$[cite: 2]\
3.  **Uniform Distribution:** Specifically scaled to match the target mean and variance[cite: 2].\
\
### Key Python Implementations:\
*   **Vectorized Sampling:** Utilizing `scipy.stats` for efficient generation of $n \\times N$ sample matrices[cite: 2].\
*   **Statistical Validation:** Checking the percentage of sample means falling within the $\\pm 1.96\\sigma$ interval to verify the 95% confidence level predicted by CLT[cite: 2].\
*   **Automated Reporting:** Calculating empirical percentages for each distribution type to compare robustness[cite: 2].\
\
## Technologies Used\
*   **Python 3.x**[cite: 2]\
*   **NumPy:** For matrix operations and sample generation[cite: 2].\
*   **SciPy (stats):** For probability density functions (PDF) and random variable simulations[cite: 2].\
*   **Matplotlib:** For generating comparative histograms and variance convergence plots[cite: 2].\
\
## Results & Insights\
*   **Variance Decay:** As expected from the Law of Large Numbers, the estimation variance decreases linearly with $1/n$[cite: 2].\
*   **Convergence:** For $n=100$, even the highly skewed Exponential distribution's sample mean distribution is visually and statistically indistinguishable from a Gaussian PDF[cite: 2].\
*   **Chebyshev vs. CLT:** While Chebyshev's inequality provides a guaranteed lower bound (~74% for $k=1.96$), the CLT provides a much tighter and more accurate prediction (~95%) for large $n$[cite: 2].\
\
*Visual results (Histograms and Variance Plots) are located in the `results/plots` directory.*}