import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
filename = 'video.wav'  # Replace 'video.wav' with your audio file
vid, sample_rate = librosa.load(filename, sr=16000)

# Calculate the duration of the audio
duration_minutes = librosa.get_duration(y=vid, sr=sample_rate) / 60
print(f"Duration of audio: {duration_minutes:.2f} minutes")

# Breaking down the audio into chunks of 5 seconds to analyze energy
chunk_size = 5
window_length = chunk_size * sample_rate

# Normalize the waveform to a smaller range
normalized_waveform = vid / np.max(np.abs(vid)) * 0.5  # Normalize to range [-0.5, 0.5]

# Compute the spectrogram
spec, freqs, times, im = plt.specgram(vid, Fs=sample_rate)

# Calculate the mean and standard deviation of the audio waveform
mean_waveform = np.mean(vid)
std_waveform = np.std(vid)

# Calculate the dynamic threshold (e.g., mean + 3 * std)
dynamic_threshold = mean_waveform + 3 * std_waveform

# Print the dynamic threshold value
print(f"Dynamic Threshold: {dynamic_threshold:.2f}")

# Plot the audio waveform and spectrogram
plt.figure(figsize=(12, 10))

# Plot the normalized waveform
plt.subplot(3, 1, 1)
plt.plot(normalized_waveform, color='b')
plt.axhline(dynamic_threshold, color='r', linestyle='--', label='Dynamic Threshold')
plt.title('Figure 1: Normalized Audio Waveform with Dynamic Threshold')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Plot the spectrogram
plt.subplot(3, 1, 2)
plt.imshow(10 * np.log10(spec + 1e-10), origin='lower', aspect='auto', extent=[times.min(), times.max(), freqs.min(), freqs.max()])
plt.colorbar(format='%+2.0f dB')
plt.title('Figure 2: Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')

# Show the plots
plt.tight_layout()
plt.show()
