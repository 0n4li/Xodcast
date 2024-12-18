from io import BytesIO
from google.cloud import texttospeech
from pydub import AudioSegment

locales = {
    "de-DE": "German (Germany)",
    "en-AU": "English (Australia)",
    "en-GB": "English (UK)",
    "en-IN": "English (India)",
    "en-US": "English (US)",
    "es-ES": "Spanish (Spain)",
    "es-US": "Spanish (US)",
    "fr-CA": "French (Canada)",
    "fr-FR": "French (France)",
    "it-IT": "Italian (Italy)",
}

model_names = ["Journey", "Studio"]
model_ids = {"Journey": ["D", "F", "O"], "Studio": ["A", "B", "C", "D", "F", "O", "Q"]}

# Mapping between model IDs and genders
model_id_to_gender = {
    "A": "FEMALE",
    "B": "MALE",
    "C": "FEMALE",
    "D": "MALE",
    "F": "FEMALE",
    "O": "FEMALE",
    "Q": "MALE",
}

voices = {
    "de-DE-Journey-D": {
        "Gender": "MALE",
        "Language": "German (Germany)",
        "Voice type": "Journey",
        "Name": "Klaus",
    },
    "de-DE-Journey-F": {
        "Gender": "FEMALE",
        "Language": "German (Germany)",
        "Voice type": "Journey",
        "Name": "Greta",
    },
    "de-DE-Journey-O": {
        "Gender": "FEMALE",
        "Language": "German (Germany)",
        "Voice type": "Journey",
        "Name": "Hanna",
    },
    "de-DE-Studio-B": {
        "Gender": "MALE",
        "Language": "German (Germany)",
        "Voice type": "Studio",
        "Name": "Markus",
    },
    "de-DE-Studio-C": {
        "Gender": "FEMALE",
        "Language": "German (Germany)",
        "Voice type": "Studio",
        "Name": "Lena",
    },
    "en-AU-Journey-D": {
        "Gender": "MALE",
        "Language": "English (Australia)",
        "Voice type": "Journey",
        "Name": "Jack",
    },
    "en-AU-Journey-F": {
        "Gender": "FEMALE",
        "Language": "English (Australia)",
        "Voice type": "Journey",
        "Name": "Olivia",
    },
    "en-AU-Journey-O": {
        "Gender": "FEMALE",
        "Language": "English (Australia)",
        "Voice type": "Journey",
        "Name": "Isla",
    },
    "en-GB-Journey-D": {
        "Gender": "MALE",
        "Language": "English (UK)",
        "Voice type": "Journey",
        "Name": "Oliver",
    },
    "en-GB-Journey-F": {
        "Gender": "FEMALE",
        "Language": "English (UK)",
        "Voice type": "Journey",
        "Name": "Amelia",
    },
    "en-GB-Journey-O": {
        "Gender": "FEMALE",
        "Language": "English (UK)",
        "Voice type": "Journey",
        "Name": "Emily",
    },
    "en-GB-Studio-B": {
        "Gender": "MALE",
        "Language": "English (UK)",
        "Voice type": "Studio",
        "Name": "Harry",
    },
    "en-GB-Studio-C": {
        "Gender": "FEMALE",
        "Language": "English (UK)",
        "Voice type": "Studio",
        "Name": "Jessica",
    },
    "en-IN-Journey-D": {
        "Gender": "MALE",
        "Language": "English (India)",
        "Voice type": "Journey",
        "Name": "Arjun",
    },
    "en-IN-Journey-F": {
        "Gender": "FEMALE",
        "Language": "English (India)",
        "Voice type": "Journey",
        "Name": "Aanya",
    },
    "en-IN-Journey-O": {
        "Gender": "FEMALE",
        "Language": "English (India)",
        "Voice type": "Journey",
        "Name": "Saanvi",
    },
    "en-US-Journey-D": {
        "Gender": "MALE",
        "Language": "English (US)",
        "Voice type": "Journey",
        "Name": "Liam",
    },
    "en-US-Journey-F": {
        "Gender": "FEMALE",
        "Language": "English (US)",
        "Voice type": "Journey",
        "Name": "Emma",
    },
    "en-US-Journey-O": {
        "Gender": "FEMALE",
        "Language": "English (US)",
        "Voice type": "Journey",
        "Name": "Olivia",
    },
    "en-US-Studio-O": {
        "Gender": "FEMALE",
        "Language": "English (US)",
        "Voice type": "Studio",
        "Name": "Sophia",
    },
    "en-US-Studio-Q": {
        "Gender": "MALE",
        "Language": "English (US)",
        "Voice type": "Studio",
        "Name": "James",
    },
    "es-ES-Journey-D": {
        "Gender": "MALE",
        "Language": "Spanish (Spain)",
        "Voice type": "Journey",
        "Name": "Hugo",
    },
    "es-ES-Journey-F": {
        "Gender": "FEMALE",
        "Language": "Spanish (Spain)",
        "Voice type": "Journey",
        "Name": "Lucía",
    },
    "es-ES-Journey-O": {
        "Gender": "FEMALE",
        "Language": "Spanish (Spain)",
        "Voice type": "Journey",
        "Name": "Sofía",
    },
    "es-ES-Studio-C": {
        "Gender": "FEMALE",
        "Language": "Spanish (Spain)",
        "Voice type": "Studio",
        "Name": "Martina",
    },
    "es-ES-Studio-F": {
        "Gender": "MALE",
        "Language": "Spanish (Spain)",
        "Voice type": "Studio",
        "Name": "Daniel",
    },
    "es-US-Journey-D": {
        "Gender": "MALE",
        "Language": "Spanish (US)",
        "Voice type": "Journey",
        "Name": "Mateo",
    },
    "es-US-Journey-F": {
        "Gender": "FEMALE",
        "Language": "Spanish (US)",
        "Voice type": "Journey",
        "Name": "Isabella",
    },
    "es-US-Journey-O": {
        "Gender": "FEMALE",
        "Language": "Spanish (US)",
        "Voice type": "Journey",
        "Name": "Valentina",
    },
    "es-US-Studio-B": {
        "Gender": "MALE",
        "Language": "Spanish (US)",
        "Voice type": "Studio",
        "Name": "Sebastián",
    },
    "fr-CA-Journey-D": {
        "Gender": "MALE",
        "Language": "French (Canada)",
        "Voice type": "Journey",
        "Name": "William",
    },
    "fr-CA-Journey-F": {
        "Gender": "FEMALE",
        "Language": "French (Canada)",
        "Voice type": "Journey",
        "Name": "Emma",
    },
    "fr-CA-Journey-O": {
        "Gender": "FEMALE",
        "Language": "French (Canada)",
        "Voice type": "Journey",
        "Name": "Léa",
    },
    "fr-FR-Journey-D": {
        "Gender": "MALE",
        "Language": "French (France)",
        "Voice type": "Journey",
        "Name": "Gabriel",
    },
    "fr-FR-Journey-F": {
        "Gender": "FEMALE",
        "Language": "French (France)",
        "Voice type": "Journey",
        "Name": "Louise",
    },
    "fr-FR-Journey-O": {
        "Gender": "FEMALE",
        "Language": "French (France)",
        "Voice type": "Journey",
        "Name": "Jade",
    },
    "fr-FR-Studio-A": {
        "Gender": "FEMALE",
        "Language": "French (France)",
        "Voice type": "Studio",
        "Name": "Alice",
    },
    "fr-FR-Studio-D": {
        "Gender": "MALE",
        "Language": "French (France)",
        "Voice type": "Studio",
        "Name": "Raphaël",
    },
    "it-IT-Journey-D": {
        "Gender": "MALE",
        "Language": "Italian (Italy)",
        "Voice type": "Journey",
        "Name": "Leonardo",
    },
    "it-IT-Journey-F": {
        "Gender": "FEMALE",
        "Language": "Italian (Italy)",
        "Voice type": "Journey",
        "Name": "Sofia",
    },
    "it-IT-Journey-O": {
        "Gender": "FEMALE",
        "Language": "Italian (Italy)",
        "Voice type": "Journey",
        "Name": "Giulia",
    },
}

multi_speaker_voices = {
    "en-US-Studio-MultiSpeaker-R": {
        "Gender": "FEMALE",
        "Language": "English (US)",
        "Voice type": "MultiSpeaker",
        "Name": "Rosie",
    },
    "en-US-Studio-MultiSpeaker-S": {
        "Gender": "MALE",
        "Language": "English (US)",
        "Voice type": "MultiSpeaker",
        "Name": "Sam",
    },
    "en-US-Studio-MultiSpeaker-T": {
        "Gender": "MALE",
        "Language": "English (US)",
        "Voice type": "MultiSpeaker",
        "Name": "Tom",
    },
    "en-US-Studio-MultiSpeaker-U": {
        "Gender": "MALE",
        "Language": "English (US)",
        "Voice type": "MultiSpeaker",
        "Name": "Ulysses",
    },
}


class OutputFormat:
    WAV = "wav"
    MP3 = "mp3"

    def get_encoding(format):
        return {
            OutputFormat.WAV: wav_encoding,
            OutputFormat.MP3: mp3_encoding,
        }[format]


wav_encoding = texttospeech.AudioEncoding.LINEAR16
mp3_encoding = texttospeech.AudioEncoding.MP3


def synthesize_input(synthesis_input, voice_params, format=OutputFormat.WAV):
    """Synthesize a single chunk of conversation and yield audio content."""
    client = texttospeech.TextToSpeechClient()

    audio_config = texttospeech.AudioConfig(
        audio_encoding=OutputFormat.get_encoding(format),
        sample_rate_hertz=24000,
        speaking_rate=1.0,
        pitch=0.0,
        volume_gain_db=0.0,
        effects_profile_id="",
    )

    voice = texttospeech.VoiceSelectionParams(**voice_params)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    yield response.audio_content


def synthesize_text(text, voice_params, format=OutputFormat.WAV):
    """Synthesize a single chunk of conversation."""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    for audio_content in synthesize_input(synthesis_input, voice_params, format):
        yield audio_content


def synthesize_multi_speaker_chunk(chunk, voice_params, format=OutputFormat.WAV):
    """Synthesize a single chunk of conversation."""
    turns = map(
        lambda x: texttospeech.MultiSpeakerMarkup.Turn(
            text=x["text"], speaker=x["speaker"].split("-")[-1]
        ),
        chunk,
    )
    turns = list(turns)
    print(turns)

    multi_speaker_markup = texttospeech.MultiSpeakerMarkup(turns=turns)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(
        multi_speaker_markup=multi_speaker_markup
    )

    for audio_content in synthesize_input(synthesis_input, voice_params, format):
        yield audio_content


def combine_audio_files(audio_files, output_file, format=OutputFormat.WAV):
    """Combine multiple audio files into a single file."""
    combined = AudioSegment.empty()
    for audio_file in audio_files:
        segment = AudioSegment.from_file(audio_file, format=format)
        combined += segment

    combined.export(output_file, format=format)


def get_supported_stream(
    audio_file_path,
    format=OutputFormat.WAV,
    supported_stream_type='audio/webm; codecs="opus"',
    is_first_chunk=False,
    webm_params=None,
):
    """
    Opens an audio file and reads its content into a BytesIO stream.

    Args:
        audio_file_path (str): Path to the audio file.
        format (OutputFormat): Format of the audio file.
        supported_stream_type (str): MIME type of the stream to be generated.
        is_first_chunk (bool): Whether this is the first chunk of a streaming response.
        webm_params (dict): Optional dictionary of parameters for WebM encoding.

    Returns:
        bytes: The audio content of the file in the specified format.
    """
    if webm_params is None:
        webm_params = {
            "cluster_size_limit": "2048",
            "cluster_time_limit": "5000",
            "dash": "1",
        }

    """
    Opens an audio file and reads its content into a BytesIO stream.

    Args:
        audio_file_path (str): Path to the audio file.
        format (OutputFormat): Format of the audio file.
        supported_stream_type (str): MIME type of the stream to be generated.
        is_first_chunk (bool): Whether this is the first chunk of a streaming response.

    Returns:
        bytes: The audio content of the file in the specified format.
    """
    with open(audio_file_path, "rb") as f:
        segment = AudioSegment.from_file(f, format=format)

    stream = BytesIO()

    if supported_stream_type == 'audio/webm; codecs="opus"':
        # Construct parameters for WebM encoding
        params = [
            "-cluster_size_limit",
            webm_params["cluster_size_limit"],
            "-cluster_time_limit",
            webm_params["cluster_time_limit"],
        ]
        if not is_first_chunk:
            params.extend(["-dash", webm_params["dash"]])

        # Export with WebM header (if first chunk) or without (subsequent chunks)
        segment.export(stream, format="webm", codec="libopus", parameters=params)
    elif supported_stream_type == "audio/mpeg":
        segment.export(stream, format="mpeg")
    elif supported_stream_type == 'audio/mp4; codecs="mp4a.40.2"':
        segment.export(stream, format="mp4", codec="mp4a.40.2")
    else:
        raise Exception("Unsupported stream type")

    stream.seek(0)
    return stream.read()


def generate_audio_from_chunks(chunks, multi_speaker=False, format=OutputFormat.WAV):
    """Generate audio from chunks and combine into a single file."""
    # Yield audio data for each chunk
    for i, chunk in enumerate(chunks):
        if multi_speaker is False:
            for j, chunk_entry in enumerate(chunk):
                current_speaker = chunk_entry["speaker"]
                current_text = chunk_entry["text"]
                voice_params = {
                    "language_code": "-".join(current_speaker.split("-")[:2]),
                    "name": current_speaker,
                }
                for audio_content in synthesize_text(
                    current_text, voice_params, format
                ):
                    yield audio_content
                print(f"Generated chunk {i+1}-{j+1} / {len(chunks)}")
        else:
            # Hard code for now
            voice_params = {
                "language_code": "en-US",
                "name": "en-US-Studio-MultiSpeaker",
            }
            for audio_content in synthesize_multi_speaker_chunk(
                chunk, voice_params, format
            ):
                yield audio_content
            print(f"Generated chunk {i+1} / {len(chunks)}")
