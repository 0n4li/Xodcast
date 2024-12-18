# Output JSON format
JSON_FORMAT = """
{
    "title": "Topic of the podcast",
    "host_name": "Name of the host",
    "guest_name": "Name of the guest",
    "conversation": [
        {"speaker": "Host", "text": "spoken text"},
        {"speaker": "Guest", "text": "spoken text"}
    ]
}
"""

# Rules for different conversation types
CASUAL_CONVERSATION_RULES = """
- Use a casual, conversational tone
- Include some humor and personality
"""

FORMAL_CONVERSATION_RULES = """
- Use a formal, professional tone
- Include jargon and polished language
"""

IN_DEPTH_CONVERSATION_RULES = """
- Use a deep, nuanced tone
- Focus on complex topics and deep insights
"""

SATIRICAL_CONVERSATION_RULES = """
- Use a satirical, ironic tone
- Include jokes, puns, and satire
"""

# Rules for different conversation modes
QNA_CONVERSATION_RULES = """
- Focus on questions and answers. The host asks the guest a question and the guest answers.
"""

DISCUSSION_CONVERSATION_RULES = """
- Focus on discussion and conversation. Both the host and the guest participate in the discussion.
"""

DEBATE_CONVERSATION_RULES = """
- Focus on debate and argument. Both the host and the guest participate in the debate.
- It is okay for both the host and the guest to disagree.
- It is okay for both the host and the guest to interrupt each other.
"""

# Rules for different conversation lengths
SHORT_CONVERSATION_RULES = """
- The conversation should be short and quick
- Focus on the most important points
- Keep the conversation under 5 minutes
"""

MEDIUM_CONVERSATION_RULES = """
- The conversation should be medium in length
- Focus on a balanced mix of topics and exchanges
- Keep the conversation between 5 and 10 minutes
"""

LONG_CONVERSATION_RULES = """
- The conversation should be long and detailed
- Focus on a deep and in-depth exploration of the topic along with related topics
- Keep the conversation over 10 minutes
"""

# Rules for different emotion levels
EMOTIONS = """
Here's a **comprehensive list of emotions** that can be expressed in speeches, along with the typical words or sounds associated with each. Let me know if anything else needs to be added!

---

### **1. Laughter**
- **Words/Sounds**: Ha ha, He he, Ho ho, LOL, Chuckle, Giggle, Snicker, Teehee.

### **2. Admiration**
- **Words/Sounds**: Wow, Amazing, Incredible, Fantastic, Bravo, Splendid, Astonishing, Outstanding.

### **3. Sadness**
- **Words/Sounds**: Oh no, Sigh, Alas, Sob, Tearful, Heartbreaking, Despair, Downhearted.

### **4. Happiness**
- **Words/Sounds**: Yay, Hooray, Cheers, Woo-hoo, Delightful, Wonderful, Thrilled, Ecstatic, Blissful.

### **5. Passion**
- **Words/Sounds**: Absolutely, Definitely, Fired up, Driven, Committed, Enthusiastic, Let's do this.

### **6. Empathy**
- **Words/Sounds**: I understand, I feel your pain, I'm with you, Oh dear, Truly, Deeply, From the heart.

### **7. Pride**
- **Words/Sounds**: I'm proud, This is remarkable, Accomplishment, Honor, Glory, Dignity, Hail, Celebrate.

### **8. Gratitude**
- **Words/Sounds**: Thank you, I'm grateful, I appreciate it, Bless you, Much obliged, From the bottom of my heart.

### **9. Hope**
- **Words/Sounds**: We can, Believe, Tomorrow, Possibility, Dream, Imagine, Visionary, Optimistic, Inspired.

### **10. Anger**
- **Words/Sounds**: Enough is enough, How dare, Unacceptable, Outrageous, Furious, No more, This ends now.

### **11. Fear or Urgency**
- **Words/Sounds**: Watch out, Beware, We must act, Danger, Emergency, Now, Immediately, Critical, Alarm.

### **12. Determination**
- **Words/Sounds**: I will, We must, Let's go, Commitment, Resolute, Unwavering, Persevere, Stand firm.

### **13. Humor**
- **Words/Sounds**: LOL, Haha, That's funny, Cracked me up, Amusing, Witty, Hilarious, Chuckle.

### **14. Curiosity**
- **Words/Sounds**: Hmm, Interesting, Tell me more, What if, Imagine, Discover, Explore, Why, How.

### **15. Surprise**
- **Words/Sounds**: Wow, Oh my, What, Can't believe it, Shock, Astonished, Unbelievable, Startling.

### **16. Relief**
- **Words/Sounds**: Phew, Finally, Thank goodness, What a relief, Relaxed, At ease, All is well.

### **17. Love or Affection**
- **Words/Sounds**: I adore, I cherish, Love you, My heart, Tender, Warmth, Affection, Devotion.

### **18. Inspiration**
- **Words/Sounds**: Go for it, You can do it, Reach for the stars, Believe in yourself, Encouraging, Uplifting.

### **19. Regret**
- **Words/Sounds**: I'm sorry, I wish, If only, My apologies, Deeply regret, Remorseful, Hindsight.

### **20. Nostalgia**
- **Words/Sounds**: Ah, Remember when, Those were the days, Looking back, Memories, Sentimental, Reflective.

### **21. Disgust**
- **Words/Sounds**: Ew, Ugh, Gross, Yuck, How awful, Revolting, Sickening, Displeased.

### **22. Confusion**
- **Words/Sounds**: Huh, What, I don't understand, Perplexing, Baffling, Strange, Curious, Lost.

### **23. Awe**
- **Words/Sounds**: Wow, Marvelous, Breathtaking, Incredible, Unimaginable, Spectacular, Majestic.

### **24. Sympathy**
- **Words/Sounds**: I'm sorry to hear, My condolences, Heartfelt, Poor thing, Feel for you, Compassionate.

### **25. Excitement**
- **Words/Sounds**: Woohoo, Yay, Can't wait, Pumped up, Awesome, Fired up, Exhilarated, Jubilant.

### **26. Confidence**
- **Words/Sounds**: I can, Watch me, Bring it on, Absolutely, No doubt, Certain, Assurance, Boldly.

---

Feel free to suggest more emotions or sounds/words to expand this list further!

"""

LOW_EMOTIONALITY_RULES = """
- There should be no emphasis on emotion in the speech.
- The speech should be neutral and objective.
"""

MEDIUM_EMOTIONALITY_RULES = """
- There should be some emphasis on emotion in the speech.
- You can use words or phrases to express emotion based on below:
    ```{EMOTIONS}```
"""

HIGH_EMOTIONALITY_RULES = """
- There should be a lot of emphasis on emotion in the speech.
- You can use words or phrases to express emotion based on below:
    ```{EMOTIONS}```
"""

# Rules for use of stutter
LOW_STUTTER_RULES = """
- There should be no stuttering in the speech.
- There should be minimum repetition of words or phrases.
- The speech of both the host and the guest should be clear and articulate.
"""

MEDIUM_STUTTER_RULES = """
- There should be some stuttering in the speech.
- There should be moderate repetition of words or phrases.
- The speech of both the host and the guest should be mostly clear and articulate with some thoughtful pauses.
"""

HIGH_STUTTER_RULES = """
- There should be a lot of stuttering in the speech.
- There should be a lot of repetition of words or phrases.
- The speech of both the host and the guest should be mostly clear and articulate with lots of thoughtful pauses.
"""

# Podcast Details
PODCAST_DETAILS = """
- **Podcast Name**: {podcast_name}
- **Host**: {host_name}
- **Host Gender**: {host_gender}
- **Guest**: {guest_name}
- **Guest Gender**: {guest_gender}
- **Below is the Topic on which the podcast is based**:
    ```{topic}```
"""

# System Prompt
SYSTEM_PROMPT = """
You are an expert podcast conversation generator.
Generate a natural, engaging conversation between a Host and a Guest on the given topic.

Follow these rules:

# General Instructions:
- Do not use any markdown in the conversation text.
- Use ONLY "Host" or "Guest" as speaker values.
- Include all required fields.
- Return ONLY the JSON object specified in the Output Format.

# Conversation Tone and Type:
{conversation_rules}

# Conversation Mode:
{conversation_mode}

# Conversation Length:
{conversation_length}

# Emotion Level:
{emotion_level}

# Use of Stutter:
{stutter_level}

# Podcast Details:
{podcast_details}

# Output Format:
- Format the response EXACTLY as a JSON object with this structure (no markdown, no extra text):
    ```{json_format}```
- IMPORTANT: Return ONLY the JSON object, no other text or formatting."""

# Error Correction Prompt
ERROR_CORRECTION_PROMPT = """
Your previous response did not match the required JSON structure.
Please format your response EXACTLY as shown below, with no additional text or formatting:
    ```{json_format}```

Previous error: {error}

Remember:
1. Use ONLY "Host" or "Guest" as speaker values
2. Include all required fields
3. Return ONLY the JSON object
4. Use proper JSON formatting with double quotes
"""

# Mapping
prompt_mapping = {
    "conversationType": {
        "casual": CASUAL_CONVERSATION_RULES,
        "formal": FORMAL_CONVERSATION_RULES,
        "in-depth": IN_DEPTH_CONVERSATION_RULES,
        "satirical": SATIRICAL_CONVERSATION_RULES,
    },
    "conversationMode": {
        "qna": QNA_CONVERSATION_RULES,
        "discussion": DISCUSSION_CONVERSATION_RULES,
        "debate": DEBATE_CONVERSATION_RULES,
    },
    "conversationLength": {
        1: SHORT_CONVERSATION_RULES,
        2: MEDIUM_CONVERSATION_RULES,
        3: LONG_CONVERSATION_RULES,
    },
    "emotionSlider": {
        1: LOW_EMOTIONALITY_RULES,
        2: MEDIUM_EMOTIONALITY_RULES,
        3: HIGH_EMOTIONALITY_RULES,
    },
    "stutterSlider": {
        1: LOW_STUTTER_RULES,
        2: MEDIUM_STUTTER_RULES,
        3: HIGH_STUTTER_RULES,
    },
}
