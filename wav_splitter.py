# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


def split_wav(file_name):

    # Load your audio.
    audio_wav = AudioSegment.from_wav(file_name)

    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    chunks = split_on_silence(
        # Use the loaded audio.
        audio_wav,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len=1000,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh=-35
    )

    target_length = 3 * 1000
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            # if the last output chunk is longer than the target length,
            # we can start a new one
            output_chunks.append(chunk)

    # Process each chunk with your parameters
    for i, chunk in enumerate(output_chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=250)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        #chunk longer than 3sec
        if len(normalized_chunk) > 3000:
            # Export the audio chunk with new bitrate.
            print("Exporting chunk{0}.wav.".format(i))
            normalized_chunk.export(
                "temp_fragment/chunk{0}.wav".format(i),
                bitrate="192k",
                format="wav"
            )


