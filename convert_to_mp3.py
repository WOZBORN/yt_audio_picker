import os
from pydub import AudioSegment

# Directory containing the .webm audio files
directory = 'temp'

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.webm'):
        # Get the full path of the input file
        input_path = os.path.join(directory, filename)

        # Construct the output file path by replacing the extension
        output_path = os.path.splitext(input_path)[0] + '.mp3'

        # Load the audio file
        audio = AudioSegment.from_file(input_path, format='webm')

        # Export the audio as an .mp3 file
        audio.export(output_path, format='mp3')