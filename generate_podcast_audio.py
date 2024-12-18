import json
import os
from google_tts import OutputFormat, generate_audio_from_chunks


default_host_voice = "en-US-Studio-Q"
default_guest_voice = "en-US-Studio-O"


def load_conversation(json_file):
    """Load conversation from JSON file."""
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


def chunk_conversation(
    conversation,
    char_limit=2000,
    host_voice="en-US-Studio-Q",
    guest_voice="en-US-Studio-O",
):
    """Split conversation into chunks under the character limit."""
    chunks = []
    current_chunk = []
    current_length = 0

    for entry in conversation["conversation"]:
        # Count the total length including speaker markup
        speaker_voice = host_voice if entry["speaker"] == "Host" else guest_voice
        markup_length = len(speaker_voice) + 10
        total_length = len(entry["text"]) + markup_length

        # If adding this entry would exceed limit and we have entries in current chunk
        if current_length + total_length > char_limit and current_chunk:
            chunks.append(current_chunk)
            current_chunk = []
            current_length = 0

        # If a single entry is longer than the limit, split it into smaller pieces
        if total_length > char_limit:
            words = entry["text"].split()
            current_text = ""

            for word in words:
                if len(current_text) + len(word) + 1 > (
                    char_limit - markup_length
                ):  # Leave room for speaker markup
                    if current_text:
                        current_chunk.append(
                            {"text": current_text.strip(), "speaker": speaker_voice}
                        )
                        chunks.append(current_chunk)
                        current_chunk = []
                        current_text = word
                        current_length = len(word)
                else:
                    current_text += " " + word if current_text else word
                    current_length = len(current_text)

            if current_text:
                current_chunk.append(
                    {"text": current_text.strip(), "speaker": speaker_voice}
                )
                current_length = len(current_text)
        else:
            current_chunk.append({"text": entry["text"], "speaker": speaker_voice})
            current_length += total_length

    # Add any remaining entries
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_podcast_audio(json_file, settings={}, format=OutputFormat.WAV):
    """Generate podcast audio from JSON file."""
    # Load the conversation
    conversation = load_conversation(json_file)

    # Speaker settings
    host_voice = settings.get("hostVoice", "en-US-Studio-Q")
    guest_voice = settings.get("guestVoice", "en-US-Studio-O")
    multi_speaker = "MultiSpeaker" in host_voice or "MultiSpeaker" in guest_voice

    if "MultiSpeaker" in host_voice and "MultiSpeaker" not in guest_voice:
        raise Exception("Host voice must be multispeaker")

    if "MultiSpeaker" in guest_voice and "MultiSpeaker" not in host_voice:
        raise Exception("Guest voice must be multispeaker")

    # Split into chunks
    chunks = chunk_conversation(
        conversation,
        char_limit=1000,
        host_voice=host_voice,
        guest_voice=guest_voice,
    )

    # Generate audio from chunks using google_tts
    audio_data = generate_audio_from_chunks(chunks, multi_speaker, format)

    yield from audio_data


if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "on-ali-service.json"
    # generate_podcast_audio(
    #    "tomato.json",
    #    "output-studio.wav",
    #    settings={"hostVoice": "en-US-Studio-Q", "guestVoice": "en-US-Studio-O"},
    # )
    voices = [
        "R",
        "S",
        "T",
        "U",
    ]
    for voice1 in voices:
        for voice2 in voices:
            if voice1 == voice2:
                continue
            generate_podcast_audio(
                "potato.json",
                f"output-{voice1}-{voice2}.wav",
                settings={
                    "hostVoice": f"en-US-Studio-MultiSpeaker-{voice1}",
                    "guestVoice": f"en-US-Studio-MultiSpeaker-{voice2}",
                },
            )
