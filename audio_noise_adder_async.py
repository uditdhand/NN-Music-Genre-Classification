import os
import librosa
import numpy as np
import soundfile as sf
import librosa.display
from multiprocessing import Pool
import itertools

# Define paths
input_base_dir = "Data/genres_original"
aud_output_base_dir = "Data/genres_noisy"

def add_noise_to_signal(signal, noise_factor):
    noise = np.random.randn(len(signal))
    augmented_signal = signal + noise_factor * noise
    # Cast back to same data type
    augmented_signal = augmented_signal.astype(type(signal[0]))
    return augmented_signal

# Create a function to generate spectrogram
def generate_noisy_wavs(params):
    genre_dir, audio_file = params
    genre = genre_dir.split('/')[-1]
    audio_path = os.path.join(genre_dir, audio_file)

    # Load the clean audio file
    clean_audio_data, clean_audio_data_sr = librosa.load(audio_path)
    clean_audio_data = clean_audio_data[:clean_audio_data_sr * 10]
    
    # Add white noise to the audio data
    noisy_audio_data = add_noise_to_signal(clean_audio_data, 0.005)

    # Load the noise audio file
    noise_data, noise_data_sr = librosa.load('Data/noise.wav')
    noise_data = noise_data[:noise_data_sr * 10]
    
    # # Mix audio and noise, scaling down to prevent clipping
    real_world_audio_data = clean_audio_data + 0.3 * noise_data

    # # Save the figure as an image
    output_genre_dir = os.path.join(aud_output_base_dir, genre)
    if not os.path.exists(output_genre_dir):
        os.makedirs(output_genre_dir)
    output_aud_path = os.path.join(output_genre_dir, audio_file)

    # Save the noisy data to a new .wav file
    sf.write(output_aud_path, real_world_audio_data, clean_audio_data_sr)
    
    # Now generate spectrogram
    # generate_spectrogram(params)

if __name__ == '__main__':

    # Ensure the output directory exists
    if not os.path.exists(aud_output_base_dir):
        os.makedirs(aud_output_base_dir)

    # Prepare the set of parameters for processes
    params = []
    for genre_dir in os.listdir(input_base_dir):
        genre_path = os.path.join(input_base_dir, genre_dir)
        if os.path.isdir(genre_path):
            for audio_file in os.listdir(genre_path):
                params.append([genre_path, audio_file])

    # Generate spectrograms in parallel
    with Pool() as p:
        p.map(generate_noisy_wavs, params)

    print("Clipped and added noise successfully!")