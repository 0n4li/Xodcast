import re


def apply_emotional_ssml(text):
    """
    Applies emotional cues to text using SSML tags based on keywords,
    punctuation, and context.

    Args:
        text: The input text string.

    Returns:
        The text with SSML tags for emotional cues.
    """

    # --- Emotion Keyword Dictionaries ---
    laughter_keywords = ["haha", "hehe", "lol", "chuckle", "giggle", "bwahaha", "lmao"]
    crying_keywords = [
        "sob",
        "sniffle",
        "waaah",
        "tears",
        "heartbroken",
        "devastated",
        "grief",
    ]
    joyful_keywords = [
        "happy",
        "joyful",
        "excited",
        "thrilled",
        "delighted",
        "wonderful",
        "fantastic",
    ]
    angry_keywords = ["angry", "furious", "mad", "irritated", "frustrated", "outraged"]
    serious_keywords = [
        "serious",
        "important",
        "crucial",
        "essential",
        "fundamental",
        "solemn",
    ]

    # --- Punctuation Patterns ---
    exclamation_pattern = r"!"
    question_pattern = r"\?"
    pause_pattern = r"\.\.\."

    # --- Helper function to apply prosody ---
    def apply_prosody(text, pitch=None, rate=None, volume=None):
        ssml = "<prosody"
        if pitch:
            ssml += f' pitch="{pitch}"'
        if rate:
            ssml += f' rate="{rate}"'
        if volume:
            ssml += f' volume="{volume}"'
        ssml += f">{text}</prosody>"
        return ssml

    sentences = re.split(
        r"(?<=[.!?])\s+", text
    )  # Split into sentences based on punctuation
    ssml_text = "<speak>"

    for sentence in sentences:
        lower_sentence = sentence.lower()

        # --- Emotion Detection ---
        if any(keyword in lower_sentence for keyword in laughter_keywords):
            ssml_text += apply_prosody(sentence, pitch="+2st", rate="+20%") + " "
        elif any(keyword in lower_sentence for keyword in crying_keywords):
            ssml_text += (
                apply_prosody(sentence, pitch="-2st", rate="-15%", volume="soft") + " "
            )
        elif any(keyword in lower_sentence for keyword in joyful_keywords):
            ssml_text += apply_prosody(sentence, pitch="+1.5st", rate="+15%") + " "
        elif any(keyword in lower_sentence for keyword in angry_keywords):
            ssml_text += (
                apply_prosody(sentence, pitch="-1st", rate="-5%", volume="loud") + " "
            )
        elif any(keyword in lower_sentence for keyword in serious_keywords):
            ssml_text += apply_prosody(sentence, pitch="-1st", rate="-10%") + " "
        # --- Punctuation-Based Emotion ---
        elif re.search(exclamation_pattern, sentence):
            ssml_text += apply_prosody(sentence, pitch="+1st", rate="+10%") + " "
        elif re.search(question_pattern, sentence):
            ssml_text += apply_prosody(sentence, pitch="+0.5st", rate="+5%") + " "
        elif re.search(pause_pattern, sentence):
            ssml_text += (
                apply_prosody(sentence.replace("...", ""), rate="-20%")
                + '<break time="1s"/>'
                + " "
            )  # Reduced rate and added break for dramatic pause
        # --- Context-Based Emotion (Example - Parentheticals)---
        elif "(" in sentence and ")" in sentence:
            # Assuming parentheticals often indicate tone or action
            content_in_parenthesis = sentence[
                sentence.find("(") + 1 : sentence.find(")")
            ]
            if any(
                keyword in content_in_parenthesis.lower()
                for keyword in laughter_keywords + ["warm smile"]
            ):
                ssml_text += (
                    apply_prosody(
                        sentence.replace(f"({content_in_parenthesis})", ""),
                        pitch="+1st",
                        rate="+10%",
                    )
                    + " "
                )  # Apply to the sentence not just the parenthesis
            elif any(
                keyword in content_in_parenthesis.lower()
                for keyword in crying_keywords + ["deep sigh", "shake of the head"]
            ):
                ssml_text += (
                    apply_prosody(
                        sentence.replace(f"({content_in_parenthesis})", ""),
                        pitch="-2st",
                        rate="-10%",
                    )
                    + " "
                )

        else:
            ssml_text += sentence + " "

    ssml_text += "</speak>"
    return ssml_text
