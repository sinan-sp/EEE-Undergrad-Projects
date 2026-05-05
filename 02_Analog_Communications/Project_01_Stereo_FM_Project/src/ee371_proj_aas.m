clc; clear; close all;

%*************
% Step 0: Loading the doc
%*************

load('fm_signal.mat');

fs = 240000; % Sampling Frequency

%*************
% Step 1: Plotting Spectrum
%*************

y = band_pass_signal; % Sinyalim
N = length(y); % Sample sayım (data boyutum)
t = (0:N-1) / fs; % Time eksenim

% Freq Domainim

Y_fft = fft(y); %fft aldım
Y_shifted = fftshift(Y_fft); % frekasnı ortaladım
f = linspace(-fs/2, fs/2, N); % -120k ile 120k arası generate ettim
mag_Y = abs(Y_shifted)/N;

% Amplitude Spectrum Plotting
figure;
plot(f/1000, mag_Y);
title('Amplitude Spectrum of Received Baseband Signal');
xlabel('Frequency [kHz]');
ylabel('Magnitude [V]');
grid on; axis square;
legend('Received FM Signal');

%*************
% Step 2: FM Demodulation
%*************

z = hilbert(y); % Hilbert Transformu aldım
inst_phase = unwrap(angle(z)); % instantaneous phase = angle of z
% inst_freq = (1/2pi) * (d(Phase)/dt) : diff fonksiyonu ile yan yana iki eleman farkını aldım.
inst_freq_total = diff(inst_phase)*fs/(2*pi);

demodulated_signal = inst_freq_total - fc; % basebande döndük

% fft of demodulated_signal
N_demod = length(demodulated_signal);
Y_demod = fft(demodulated_signal);
Y_demod_shifted = fftshift(Y_demod);

% yeni freq eksenim
f_demod = linspace(-fs/2, fs/2, N_demod);
mag_demod = abs(Y_demod_shifted)/N_demod;
% plot demodulated signal

figure;
plot(f_demod/1000, mag_demod);
title('Spectrum of Demodulated FM Signal');
xlabel('Frequency [kHz]');
ylabel('Frequency Deviation [Hz]');
xlim([0,60]);
grid on; axis square;

xline(19, '--r', 'Pilot Tone (19k)'); % Pilot Tone çizgisi
text(2, max(mag_demod)*0.3, 'Mono Audio (L+R)', 'FontSize', 10, 'Color', 'blue');
text(38, max(mag_demod)*0.1, 'Mono Audio (L-R)', 'FontSize', 10, 'Color', 'blue');
legend('Demodulated Spectrum', 'Pilot Marker');

%*************
% Step 3-4: Mono Extraction via LPF
%*************

% Filter parameters
f_cutoff_lpf = 16000; % cutoff freq
nyquist = fs/2; % Nyquist freq = 120 kHz 
Wn = f_cutoff_lpf / nyquist; % normalize frekans 0-1 arasına
filter_order = 5; % 5th Ordr Filter

% Calculate Filter Coefficients
[b, a] = butter(filter_order, Wn, 'low');

% Apply the filter
mono_sig = filtfilt(b, a, demodulated_signal);

% Spectrum of filterlenmiş sinyal

Y_mono = fft(mono_sig);
Y_mono_shifted = fftshift(Y_mono);
mag_mono = abs(Y_mono_shifted)/N_demod;

figure;
plot(f_demod/1000, mag_mono);
title('Spectrum of Extracted Mono (L + R) Signal');
xlabel('Frequency [kHz]');
ylabel('Frequency Deviation [Hz]');
xlim([0, 30]);
grid on; axis square;

xline(16, '--g', 'Cut-off (16k)'); 
xline(19, ':r', 'Suppressed Pilot');
legend('Filtered Mono Signal', 'LPF Cut-off', 'Suppressed Pilot Location');


%*************
% Step 5: De_emphasis Block (Filter)
%*************

%design the filter
tau = 50e-6;
fc_deemp = 1 / (2*pi*tau); %cutoffu

Wn_deemp = fc_deemp / (fs/2); %Normalize frekans

[b_de, a_de] = butter(1, Wn_deemp); % 1. Derece Butterworth filtresi

y_deemphasis = filter(b_de, a_de, mono_sig); %filterla

Y_de = fft(y_deemphasis);
Y_de_shifted = fftshift(Y_de);
mag_deemp = abs(Y_de_shifted)/N_demod;

figure;
plot(f_demod/1000, mag_deemp);
title('Spectrum after De-emphasis');
xlabel('Frequency [kHz]');
ylabel('Frequency Deviation [Hz]');
xlim([0,15]);
grid on; axis square;

text(8, max(mag_deemp)*0.1, '\leftarrow High Freq Attenuation', 'FontSize', 8);
legend('De-emphasized Signal');

%*************
% Step 6: Downsampling ve WAV Kaydı
%*************

% 1. Downsampling (Decimation)
downsample_factor = 5;
y_downsampled = decimate(y_deemphasis, downsample_factor);

% yeni sampling frekansım:
fs_new = fs / downsample_factor;

N_new = length(y_downsampled);
f_new = linspace(-fs_new/2, fs_new/2, N_new);
Y_Downsampled = fftshift(fft(y_downsampled));
mag_new = abs(Y_Downsampled)/N_new;

figure;
plot(f_new/1000, mag_new);
title('Amplitude Spectrum of Final Audio Signal');
xlabel('Frequency [kHz]');
ylabel('Frequency Deviation [Hz]');
xlim([0 20]);
grid on; axis square;
legend('Final Audio (48 kHz)');

% Sesi Normalize Edip ve Kaydetme
y_downsampled_norm = 0.95 * (y_downsampled / max(abs(y_downsampled)));

% Dosyayı kaydet
audiowrite('recovered_audio.wav', y_downsampled_norm, fs_new);


sound(y_downsampled_norm, fs_new);