import os
import librosa
import numpy as np
import soundfile as sf
import librosa.display
import matplotlib.pyplot as plt
from multiprocessing import Pool
import itertools

# Define paths
input_base_dir = "Data/genres_noisy/genres_original"
img_output_base_dir = "Data/spectrogram_images"

# Create a function to generate spectrogram
def generate_spectrogram(params):    
    genre_dir, audio_file = params
    genre = genre_dir.split('/')[-1]
    audio_path = os.path.join(genre_dir, audio_file)
    y, sr = librosa.load(audio_path)
    
    # Compute the spectrogram
    D = librosa.amplitude_to_db(abs(librosa.stft(y)), ref=np.max)
    
    # Plot the spectrogram
    plt.figure(figsize=(4, 3))
    librosa.display.specshow(D, sr=sr)
    plt.axis('off')  # Remove axes
    plt.tight_layout()
    
    # Save the figure as an image
    output_genre_dir = os.path.join(img_output_base_dir, genre)
    if not os.path.exists(output_genre_dir):
        os.makedirs(output_genre_dir)
    output_image_path = os.path.join(output_genre_dir, audio_file.replace('.wav', '.png'))
    plt.savefig(output_image_path)

    # Close the figure to free up memory
    plt.close()

if __name__ == '__main__':

    # Ensure the output directory exists
    if not os.path.exists(img_output_base_dir):
        os.makedirs(img_output_base_dir)

    # Prepare the set of parameters for processes
    params = []
    for genre_dir in os.listdir(input_base_dir):
        genre_path = os.path.join(input_base_dir, genre_dir)
        if os.path.isdir(genre_path):
            for audio_file in os.listdir(genre_path):
                params.append([genre_path, audio_file])

    # Generate spectrograms in parallel
    with Pool() as p:
        p.map(generate_spectrogram, params)

    print("Spectrogram images generated successfully!")