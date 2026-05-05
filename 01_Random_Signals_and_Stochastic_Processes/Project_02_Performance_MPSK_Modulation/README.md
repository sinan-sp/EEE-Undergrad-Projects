{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # M-PSK Communication System Performance over AWGN Channel\
\
## Project Overview\
This project simulates the performance of **8-PSK** and **16-PSK** modulation schemes in a digital communication system. The study focuses on evaluating the **Symbol Error Rate (SER)** and **Bit Error Rate (BER)** under varying Signal-to-Noise Ratio (SNR) conditions in an **AWGN channel**.\
\
## Key Technical Objectives\
*   **Constellation Mapping:** Implementation of M-PSK mapping in complex baseband.\
*   **Minimum Distance Detection:** Developing a receiver that utilizes Euclidean distance for symbol decoding.\
*   **Comparative Analysis:** Validating empirical simulation results against theoretical SER formulas using the complementary error function (`erfc`).\
*   **Coding Gain Investigation:** Analyzing the impact of **Gray Coding** versus **Natural Binary Coding** on bit error probability.\
\
## Methodology\
The simulation follows a standard digital communication pipeline:\
1.  **Symbol Generation:** Uniformly distributed random integers representing digital data.\
2.  **Channel Modeling:** Noise power is calculated based on $E_s/N_0$ derived from the target SNR (dB).\
3.  **Hamming Distance Matrix:** A systematic approach to calculate BER by analyzing the transition probabilities between symbols ($P_\{ij\}$) and their respective bit distances.\
\
## Key Insights\
*   **Complexity vs. Performance:** As $M$ increases (from 8 to 16), the distance between constellation points decreases, leading to higher SER for the same SNR.\
*   **Gray Coding Advantage:** The simulation demonstrates that Gray mapping significantly reduces BER at high SNR by ensuring that the most probable symbol errors (adjacent points) result in only a single bit error.\
\
## Technologies Used\
*   **Python 3.x**\
*   **NumPy:** For vectorized matrix operations and distance calculations.\
*   **SciPy:** For theoretical performance verification (`scipy.special.erfc`).\
*   **Matplotlib:** For technical plotting on logarithmic scales.\
\
*Visual comparisons of SER and BER curves can be found in the `results/plots` directory.*}