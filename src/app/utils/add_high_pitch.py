import concurrent.futures
from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

def add_high_pitch_note(input_file, frequency=19000, output_file=None):
    # Load the input audio file
    audio = AudioSegment.from_file(input_file)
    desired_sample_rate = 44100  # Example: 44.1 kHz
    audio = audio.set_frame_rate(desired_sample_rate)
    audio = audio.set_channels(1)
    

    # Convert the input audio to a NumPy array
    samples = np.array(audio.get_array_of_samples())

    # Get the sample rate of the input audio
    sample_rate = audio.frame_rate

    audio_duration = len(samples) / sample_rate  # Duration based on the length of input audio

    # Generate the high-pitched sound as a Sine wave
    high_pitch_duration = 3  # seconds
    high_pitch_sound = Sine(frequency).to_audio_segment(duration=high_pitch_duration * 1000, volume=-5)  # Convert to milliseconds

    # Define the time range for high-pitch effect (first 3 seconds and last 3 seconds)
    start_time = 0
    end_time = audio_duration - high_pitch_duration
    print(audio_duration, end_time)

    # Add high pitch in the first 3 seconds
    output_audio = audio.overlay(high_pitch_sound, position=start_time)

    # Add high pitch in the last 3 seconds
    output_audio = output_audio.overlay(high_pitch_sound, position=end_time * 1000)

    # Save the new audio to the same file
    if output_file is None:
        output_file = input_file
    output_audio.export(output_file, format="wav")
    
def process_audio_list(audio_list, frequency=19000):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for audio_file in audio_list:
            executor.submit(add_high_pitch_note, audio_file, frequency, output_file=audio_file[:-4] + "_embed.wav")

# Example usage:
audio_list = ["anhoiolai.mp3", "songxaanhchangdedang_1.mp3", "noinaycoem.mp3"]
# process_audio_list(audio_list, frequency=19000)  # Provide the desired high-pitched frequency

add_high_pitch_note("anhoiolai.mp3", 19000, output_file="test.wav")
