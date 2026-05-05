{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Linear Minimum Mean Square Error (LMMSE) Estimation & Statistical Analysis\
\
## Project Overview\
This project implements a **Linear Minimum Mean Square Error (LMMSE)** estimator for a zero-mean **Wide Sense Stationary (WSS)** random process. The core objective is to estimate a hidden variable $X_1$ using a sequence of observations $Y(n) = [X_2, \\dots, X_\{n+1\}]^T$ and to analyze how empirical statistical inaccuracies affect the theoretical error bounds.\
\
## Key Features\
*   **Autocorrelation Estimation:** Comparison between theoretical sinc-function based autocorrelation ($r_k$) and empirical estimates derived from datasets of varying sizes.\
*   **Wiener-Hopf Implementation:** Solving $R_Y \\mathbf\{a\} = \\mathbf\{r\}_\{X_1Y\}$ to derive optimal filter weights using the **Toeplitz** structure of WSS processes.\
*   **MSE Performance Analysis:** Evaluation of the Mean Square Error (MSE) floor when using mismatched statistics versus ideal theoretical bounds.\
*   **Data Visualization:** Automated plotting of autocorrelation convergence and log-scale MSE comparisons.\
\
## Mathematical Foundation\
The optimal weights $\\mathbf\{a\}$ are calculated using:\
$$\\mathbf\{a\} = R_Y^\{-1\} \\mathbf\{r\}_\{X_1Y\}$$\
The theoretical minimum error is defined as:\
$$e_L^*(n) = r_0 - \\mathbf\{r\}_\{X_1Y\}^T R_Y^\{-1\} \\mathbf\{r\}_\{X_1Y\}$$\
\
## Technologies Used\
*   **Python 3.x**\
*   **NumPy & SciPy:** For linear algebra (Toeplitz matrices) and statistical functions.\
*   **Pandas:** For handling and processing large observation datasets.\
*   **Matplotlib:** For high-quality technical plotting.\
\
## Results\
The analysis demonstrates that as the number of observations ($n$) increases, the theoretical MSE drops significantly (reaching $\\approx 10^\{-10\}$). However, estimators using empirical statistics (even from large datasets) hit a performance floor around $10^\{-4\}$ due to sub-optimal weight derivation.\
\
| Lag (k) | Theoretical $r_k$ | Empirical (Small) |\
| :--- | :--- | :--- |\
| 0 | 1.0000 | 0.9490 |\
| 1 | 0.9836 | 0.9252 |\
| 2 | 0.9355 | 0.8752 |\
\
*Detailed plots can be found in the `results/` directory.*}