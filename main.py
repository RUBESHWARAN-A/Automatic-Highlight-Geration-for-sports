import tkinter as tk
from tkinter import filedialog, messagebox
import librosa 
import numpy as np
import pandas as pd
import os
import shutil
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class HighlightExtractorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Highlight Extractor")
        master.configure(bg="#f0f0f0")

        self.label = tk.Label(master, text="Welcome to Highlight Extractor!", font=("Helvetica", 18), bg="#f0f0f0")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.select_audio_button = tk.Button(master, text="Select Audio File", command=self.select_audio, font=("Helvetica", 14), bg="#007bff", fg="white")
        self.select_audio_button.grid(row=1, column=0, pady=10, padx=5)

        self.extract_highlights_button = tk.Button(master, text="Extract Highlights", command=self.extract_highlights, font=("Helvetica", 14), bg="#28a745", fg="white")
        self.extract_highlights_button.grid(row=1, column=1, pady=10, padx=5)

        self.energy_threshold_label = tk.Label(master, text="Energy Threshold:", font=("Helvetica", 14), bg="#f0f0f0")
        self.energy_threshold_label.grid(row=2, column=0, pady=5, padx=5, sticky='e')
        self.energy_threshold_slider = tk.Scale(master, from_=0, to=1000, orient=tk.HORIZONTAL, font=("Helvetica", 14), bg="#f0f0f0")
        self.energy_threshold_slider.grid(row=2, column=1, pady=5, padx=5, sticky='w')

        self.clip_duration_label = tk.Label(master, text="Clip Duration (seconds):", font=("Helvetica", 14), bg="#f0f0f0")
        self.clip_duration_label.grid(row=3, column=0, pady=5, padx=5, sticky='e')
        self.clip_duration_entry = tk.Entry(master, font=("Helvetica", 14))
        self.clip_duration_entry.grid(row=3, column=1, pady=5, padx=5, sticky='w')

        self.graph_frame = tk.Frame(master, bg="#ffffff")
        self.graph_frame.grid(row=4, column=0, columnspan=3, pady=10, padx=5)

    def select_audio(self):
        self.audio_filename = filedialog.askopenfilename(title="Select Audio File")
        if self.audio_filename:
            self.label.config(text=f"Selected Audio File: {os.path.basename(self.audio_filename)}")

    def extract_highlights(self):
        if not hasattr(self, 'audio_filename') or not self.audio_filename:
            messagebox.showerror("Error", "Please select an audio file.")
            return

        energy_threshold = self.energy_threshold_slider.get()
        clip_duration = int(self.clip_duration_entry.get())

        try:
            vid, sample_rate = librosa.load(self.audio_filename, sr=16000)
            duration_minutes = librosa.get_duration(y=vid, sr=sample_rate) / 60

            chunk_size = 5 
            window_length = chunk_size * sample_rate

            energy = np.array([sum(abs(vid[i:i+window_length]**2)) for i in range(0, len(vid), window_length)])

            df = pd.DataFrame(columns=['energy', 'start', 'end'])
            row_index = 0
            for i in range(len(energy)):
                value = energy[i]
                if value >= energy_threshold:
                    i = np.where(energy == value)[0]
                    df.loc[row_index, 'energy'] = value
                    df.loc[row_index, 'start'] = i[0] * chunk_size
                    df.loc[row_index, 'end'] = (i[0] + 1) * chunk_size
                    row_index += 1

            temp = []
            i, j, n = 0, 0, len(df) - 1
            while i < n:
                j = i + 1
                while j <= n:
                    if df['end'][i] == df['start'][j]:
                        df.loc[i, 'end'] = df.loc[j, 'end']
                        temp.append(j)
                        j += 1
                    else:
                        i = j
                        break  
            df.drop(temp, axis=0, inplace=True)

            cwd = os.getcwd()
            sub_folder = os.path.join(cwd, "Subclips")
            if os.path.exists(sub_folder):
                shutil.rmtree(sub_folder)
            os.mkdir(sub_folder)

            for i in range(len(df)):
                start_lim = max(0, df['start'][i] - 5)
                end_lim = min(len(vid)/sample_rate, df['end'][i])  # Ensure end_lim does not exceed audio duration
                filename = f"highlight{i+1}.mp4"
                ffmpeg_extract_subclip("video.mp4", start_lim, end_lim, targetname=os.path.join(sub_folder, filename))
            
            messagebox.showinfo("Success", "Highlights extracted successfully.")
            
            # Display graphical representation
            fig = plt.figure(figsize=(10, 5))
            plt.subplot(2, 1, 1)
            plt.plot(vid)
            plt.title('Audio Waveform')
            plt.xlabel('Sample')
            plt.ylabel('Amplitude')

            plt.subplot(2, 1, 2)
            plt.hist(energy) 
            plt.title('Short Time Energy Distribution')
            plt.xlabel('Energy')
            plt.ylabel('Frequency')

            representations_folder = os.path.join(cwd, "representations")
            if not os.path.exists(representations_folder):
                os.mkdir(representations_folder)
            fig_path = os.path.join(representations_folder, "graphical_representation.png")
            plt.savefig(fig_path)

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            toolbar = NavigationToolbar2Tk(canvas, self.graph_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # Display spectrogram
            fig_spectrogram = plt.figure(figsize=(10, 5))
            plt.specgram(vid, Fs=sample_rate)
            plt.title('Spectrogram')
            plt.xlabel('Time (s)')
            plt.ylabel('Frequency')
            plt.colorbar(format='%+2.0f dB')

            fig_spectrogram_path = os.path.join(representations_folder, "spectrogram_representation.png")
            plt.savefig(fig_spectrogram_path)

            canvas_spectrogram = FigureCanvasTkAgg(fig_spectrogram, master=self.graph_frame)
            canvas_spectrogram.draw()
            canvas_spectrogram.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            toolbar_spectrogram = NavigationToolbar2Tk(canvas_spectrogram, self.graph_frame)
            toolbar_spectrogram.update()
            canvas_spectrogram.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
app = HighlightExtractorGUI(root)
root.mainloop()
