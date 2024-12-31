import os
import google.generativeai as genai
import json
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from prompts import (
    SYSTEM_PROMPT,
    ERROR_CORRECTION_PROMPT,
    JSON_FORMAT,
    PODCAST_DETAILS,
    prompt_mapping,
)

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
model = genai.GenerativeModel(GEMINI_MODEL)

# Rate limiting configuration
RATE_LIMIT_WINDOW = timedelta(hours=1)
last_request_time = None
requests_in_window = 0
MAX_REQUESTS_PER_WINDOW = 60  # Adjust based on your API limits

# Cache configuration
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)
CACHE_DURATION = timedelta(days=7)  # Cache responses for 7 days
CACHE_TIME_LIMIT = timedelta(minutes=5)  # Cache time limit


def extract_json_from_text(text):
    """Extract JSON object from text, handling potential formatting issues."""
    print("Raw response:", text)

    # Try to find JSON object in the text
    json_match = re.search(r"\{[\s\S]*\}", text)
    if not json_match:
        raise ValueError("No JSON object found in the response")

    json_str = json_match.group(0)
    print("Extracted JSON string:", json_str)

    try:
        # Try to parse the JSON directly
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Initial JSON parsing failed: {e}")

        # Clean up common formatting issues
        cleaned_json = json_str
        # Replace single quotes with double quotes
        cleaned_json = cleaned_json.replace("'", '"')
        # Fix unquoted keys
        cleaned_json = re.sub(r"(\w+)(?=\s*:)", r'"\1"', cleaned_json)
        # Fix trailing commas
        cleaned_json = re.sub(r",(\s*[}\]])", r"\1", cleaned_json)

        print("Cleaned JSON string:", cleaned_json)

        try:
            return json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON after cleaning: {e}")


def validate_conversation_json(data):
    """Validate that the JSON has the required structure."""
    required_keys = ["title", "host_name", "guest_name", "conversation"]
    if not all(key in data for key in required_keys):
        missing_keys = [key for key in required_keys if key not in data]
        raise ValueError(f"Missing required keys in JSON structure: {missing_keys}")

    if not isinstance(data["conversation"], list):
        raise ValueError("Conversation must be a list")

    if not data["conversation"]:  # Check if conversation is empty
        raise ValueError("Conversation list cannot be empty")

    for i, entry in enumerate(data["conversation"]):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry {i} must be an object")
        if "speaker" not in entry or "text" not in entry:
            raise ValueError(f"Entry {i} missing speaker or text")
        if entry["speaker"] not in ["Host", "Guest"]:
            raise ValueError(
                f"Entry {i} speaker must be 'Host' or 'Guest', got '{entry['speaker']}'"
            )
        if not entry["text"].strip():  # Check for empty text
            raise ValueError(f"Entry {i} has empty text")


def check_rate_limit():
    """Check if we're within rate limits."""
    global last_request_time, requests_in_window

    current_time = datetime.now()

    # First request or window expired
    if (
        last_request_time is None
        or current_time - last_request_time > RATE_LIMIT_WINDOW
    ):
        last_request_time = current_time
        requests_in_window = 0
        return True

    # Check if we're still within limits
    if requests_in_window >= MAX_REQUESTS_PER_WINDOW:
        time_until_reset = (
            last_request_time + RATE_LIMIT_WINDOW - current_time
        ).total_seconds()
        raise Exception(
            f"Rate limit exceeded. Please try again in {int(time_until_reset/60)} minutes."
        )

    requests_in_window += 1
    return True


def get_cache_key(topic, settings):
    """Generate a cache key from the topic and settings."""
    settings_str = json.dumps(settings, sort_keys=True)
    return hashlib.md5((topic + settings_str).encode()).hexdigest()


def get_cached_response(topic, settings):
    """Get cached response for a topic if it exists, is not expired, and matches settings."""
    cache_key = get_cache_key(topic, settings)
    cache_file = CACHE_DIR / f"{cache_key}.json"

    if not cache_file.exists():
        print("Cache file does not exist")
        return None

    try:
        with open(cache_file) as f:
            cached_data = json.load(f)

        # Check if cache is expired
        cache_time = datetime.fromisoformat(cached_data.get("timestamp", 0))
        if datetime.now() - cache_time > CACHE_DURATION:
            print("Cache is expired")
            return None

        # Check if cache usage is enabled in settings
        if settings.get("useCache", True):
            # Check if cache is within the time limit specified in settings
            cache_time_limit = timedelta(minutes=int(settings.get("cacheTimeLimit", 5)))
            if datetime.now() - cache_time <= cache_time_limit:
                # Check if other settings match
                print("Cache is within time limit")
                if cached_data.get("settings") == settings:
                    return cached_data["response"]
                print("Cache settings do not match")
        return None
    except Exception as e:
        print(f"Error reading cache: {e}")
        return None


def save_to_cache(topic, settings, response):
    """Save a successful response to cache."""
    cache_key = get_cache_key(topic, settings)
    cache_file = CACHE_DIR / f"{cache_key}.json"

    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "settings": settings,
        "response": response,
    }

    try:
        with open(cache_file, "w") as f:
            json.dump(cache_data, f)
    except Exception as e:
        print(f"Error saving to cache: {e}")


def generate_prompt(topic, settings={}):
    conversation_rules = prompt_mapping["conversationType"][
        settings.get("conversationType", "casual")
    ]
    conversation_mode = prompt_mapping["conversationMode"][
        settings.get("conversationMode", "qna")
    ]
    conversation_length = prompt_mapping["conversationLength"][
        settings.get("conversationLength", 2)
    ]
    emotion_level = prompt_mapping["emotionSlider"][settings.get("emotionSlider", 2)]
    stutter_level = prompt_mapping["stutterSlider"][settings.get("stutterSlider", 2)]

    podcast_details = PODCAST_DETAILS.format(
        podcast_name=settings.get("podcastName", "Podcast Name"),
        host_name=settings.get("hostName", "John Doe"),
        host_gender=settings.get("hostGender", "male"),
        guest_name=settings.get("guestName", "Jane Doe"),
        guest_gender=settings.get("guestGender", "female"),
        podcast_title=settings.get("podcastTitle", "Podcast Title"),
        topic=topic,
    )

    return SYSTEM_PROMPT.format(
        topic=topic,
        conversation_rules=conversation_rules,
        conversation_mode=conversation_mode,
        conversation_length=conversation_length,
        emotion_level=emotion_level,
        stutter_level=stutter_level,
        podcast_details=podcast_details,
        json_format=JSON_FORMAT,
    )


def generate_error_correction_prompt(last_error):
    return ERROR_CORRECTION_PROMPT.format(json_format=JSON_FORMAT, error=last_error)


def generate_conversation(topic, settings={}, max_retries=2):
    """Generate a podcast conversation about the given topic."""
    # First check cache
    cached_response = get_cached_response(topic, settings)
    if cached_response:
        print("Using cached response")
        return cached_response

    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            # Check rate limit before making request
            check_rate_limit()

            # Use error correction prompt if this is a retry
            if attempt == 0:
                prompt = generate_prompt(topic, settings)
            else:
                prompt = generate_error_correction_prompt(last_error)

            print("Prompt:", prompt)

            print(f"Attempt {attempt + 1}/{max_retries + 1}")
            response = model.generate_content(prompt)
            conversation_json = extract_json_from_text(response.text)
            validate_conversation_json(conversation_json)

            # Cache successful response
            save_to_cache(topic, settings, conversation_json)

            return conversation_json

        except Exception as e:
            error_message = str(e).lower()
            print(f"Error in attempt {attempt + 1}: {error_message}")

            # If it's a rate limit error, propagate it immediately
            if "rate limit" in error_message:
                raise Exception(
                    "Rate limit exceeded. Please try again in about an hour."
                )

            last_error = e
            attempt += 1

            if attempt > max_retries:
                raise Exception(
                    f"Failed to generate valid conversation after {max_retries + 1} attempts. Last error: {str(e)}"
                )
