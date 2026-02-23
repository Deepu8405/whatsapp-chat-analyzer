# =============================================================================
# agent.py — AI Chat Agent Class
# Inherits from Base — builds personality from chat patterns
# and powers multi turn conversation using Google Gemini
# =============================================================================

import re
import pandas as pd
from collections import Counter
from core.base import Base
from google import genai
from google.genai import types

class Agent(Base):
    """
    AI Chat Agent that mimics a specific person's WhatsApp chat style.
    Inherits shared utilities from Base superclass.

    Covers:
    - Chat pattern extraction per user
    - Dynamic system prompt generation
    - Multi turn conversation with memory
    - Model listing and rate limit tracking
    """

    # Models that work well for chat — filtered from Gemini API
    SUPPORTED_MODELS = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2-flash",
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
    ]

    # Known rate limits for free tier models
    MODEL_LIMITS = {
        "gemini-2.5-flash-lite":   {"rpm": 10, "rpd": 250},
        "gemini-2.5-flash":        {"rpm": 5,  "rpd": 20},
        "gemini-2-flash":          {"rpm": 15, "rpd": 200},
        "gemini-1.5-flash":        {"rpm": 15, "rpd": 200},
        "gemini-1.5-flash-latest": {"rpm": 15, "rpd": 200},
    }

    def __init__(self, api_key: str, df: pd.DataFrame):
        """
        Initialize Agent with Gemini API key and chat DataFrame.

        :param api_key: Google Gemini API key
        :param df: Sentiment scored DataFrame from Sentiment class
        """
        if not self.validate_dataframe(df):
            raise ValueError("Invalid or empty DataFrame provided.")

        # Configure Gemini
        self.client = genai.Client(api_key=api_key)

        self.api_key      = api_key
        self.df           = df
        self.patterns     = {}
        self.session      = None
        self.active_user  = None
        self.active_model = None
        self.active_user_role = None
        self.chat_history = []

        # Extract patterns for all users on init
        self._extract_all_patterns()

    # ------------------------------------------------------------------ #
    #  Model Management                                                    #
    # ------------------------------------------------------------------ #

    def get_available_models(self) -> list:
            """
            Fetch available Gemini models for the provided API key.
            Returns list of dicts with model info and rate limits.

            :return: List of model info dicts
            """
            try:
                available = []

                for m in self.client.models.list():
                    # Extract clean model name
                    name = m.name.replace("models/", "")

                    # Only include our supported chat models
                    if not any(s in name for s in self.SUPPORTED_MODELS):
                        continue

                    limits = self.MODEL_LIMITS.get(name, {
                        "rpm": "?", "rpd": "?"
                    })

                    available.append({
                        "name":    name,
                        "display": f"{name}  |  RPM: {limits['rpm']}  |  RPD: {limits['rpd']}",
                        "rpm":     limits["rpm"],
                        "rpd":     limits["rpd"],
                    })

                # Fallback if nothing matches
                if not available:
                    available = [{
                        "name":    "gemini-2.5-flash-lite",
                        "display": "gemini-2.5-flash-lite  |  RPM: 10  |  RPD: 250",
                        "rpm":     10,
                        "rpd":     250,
                    }]

                return available

            except Exception:
                return [{
                    "name":    "gemini-2.5-flash-lite",
                    "display": "gemini-2.5-flash-lite  |  RPM: 10  |  RPD: 250",
                    "rpm":     10,
                    "rpd":     250,
                }]
    # ------------------------------------------------------------------ #
    #  Pattern Extraction                                                  #
    # ------------------------------------------------------------------ #

    def _extract_all_patterns(self):
        """
        Extract chat patterns for all users in the DataFrame.
        Called automatically on initialization.
        """
        for user in self.df["username"].unique():
            self.patterns[user] = self._extract_user_pattern(user)

    def _extract_user_pattern(self, username: str) -> dict:
        """
        Extract detailed chat pattern and writing style for a user.

        :param username: The user whose pattern to extract
        :return: Dictionary of extracted patterns
        """
        user_df = self.df[self.df["username"] == username].copy()
        text_df = self.filter_text_messages(user_df)

        # ---- Basic Stats ----
        total_messages = len(user_df)
        avg_words      = round(text_df["word_count"].mean(), 2)
        avg_msg_length = round(text_df["message"].str.len().mean(), 2)

        # ---- Most Active Time ----
        most_active_hour = int(user_df["hour"].mode()[0])
        most_active_day  = user_df["day"].mode()[0]

        # ---- Vocabulary ----
        stopwords_set = self.load_stopwords()
        words         = self.extract_words(text_df["message"], stopwords_set)
        top_words     = [w for w, _ in Counter(words).most_common(15)]

        # ---- Emoji Usage ----
        emoji_counter = self.count_emojis(user_df["message"])
        top_emojis    = [e for e, _ in emoji_counter.most_common(5)]
        total_emojis  = sum(emoji_counter.values())
        emoji_per_msg = round(total_emojis / total_messages, 3)

        # ---- Common Short Phrases ----
        phrases = []
        for message in text_df["message"]:
            words_list = message.lower().split()
            for i in range(len(words_list) - 1):
                phrases.append(f"{words_list[i]} {words_list[i+1]}")
        top_phrases = [p for p, _ in Counter(phrases).most_common(10)]

        # ---- Tone Detection ----
        informal_markers = [
            "yaar", "bhai", "yrr", "bro", "yr", "haha",
            "lol", "hehe", "acha", "okay", "ok", "hmm"
        ]
        informal_count = sum(
            1 for msg in text_df["message"]
            for word in msg.lower().split()
            if word in informal_markers
        )
        tone = "Informal/Casual" if informal_count > 5 else "Neutral/Formal"

        # ---- Sentiment Profile ----
        dominant_sentiment = "Neutral"
        mood_score         = 5.0

        if "sentiment_label" in user_df.columns:
            sentiment_counts   = user_df["sentiment_label"].value_counts()
            dominant_sentiment = sentiment_counts.index[0]
            avg_compound       = user_df["sentiment_compound"].mean()
            mood_score         = round((avg_compound + 1) * 5, 2)

        # ---- Question & Caps Frequency ----
        question_count = text_df["message"].str.contains(r'\?').sum()
        question_ratio = round(question_count / total_messages * 100, 2)

        return {
            "username":           username,
            "total_messages":     total_messages,
            "avg_words_per_msg":  avg_words,
            "avg_msg_length":     avg_msg_length,
            "most_active_hour":   most_active_hour,
            "most_active_day":    most_active_day,
            "top_words":          top_words,
            "top_emojis":         top_emojis,
            "emoji_per_msg":      emoji_per_msg,
            "top_phrases":        top_phrases,
            "tone":               tone,
            "dominant_sentiment": dominant_sentiment,
            "mood_score":         mood_score,
            "question_ratio":     question_ratio,
        }

    def get_pattern(self, username: str) -> dict:
        """
        Get extracted pattern for a specific user.

        :param username: Username to get pattern for
        :return: Pattern dictionary
        """
        if username not in self.patterns:
            raise ValueError(f"No pattern found for user: {username}")
        return self.patterns[username]

    def get_all_patterns(self) -> dict:
        """Return all extracted patterns."""
        return self.patterns

    # ------------------------------------------------------------------ #
    #  System Prompt                                                       #
    # ------------------------------------------------------------------ #

    def _build_system_prompt(self, ai_pattern: dict, 
                                user_pattern: dict) -> str:
            """
            Build dynamic system prompt from both AI and user patterns.
            AI knows who it is AND who it is talking to.

            :param ai_pattern: Pattern of person AI will impersonate
            :param user_pattern: Pattern of person user is playing as
            :return: System prompt string
            """
            ai_top_words   = ", ".join(ai_pattern["top_words"][:10])
            ai_top_emojis  = " ".join(ai_pattern["top_emojis"])
            ai_top_phrases = ", ".join(ai_pattern["top_phrases"][:5])

            user_top_words   = ", ".join(user_pattern["top_words"][:5])
            user_top_emojis  = " ".join(user_pattern["top_emojis"])

            return f"""
    You are roleplaying as {ai_pattern['username']} in a WhatsApp group chat.
    You are talking to {user_pattern['username']}.
    Respond EXACTLY like {ai_pattern['username']} based on their real chat patterns.

    === YOUR PERSONALITY ({ai_pattern['username']}) ===
    - Tone             : {ai_pattern['tone']}
    - Mood             : {ai_pattern['dominant_sentiment']} (Mood Score: {ai_pattern['mood_score']}/10)
    - Avg Words/Reply  : {ai_pattern['avg_words_per_msg']} words (keep replies SHORT)
    - Question Style   : Asks questions {ai_pattern['question_ratio']}% of the time
    - Frequently used words : {ai_top_words}
    - Favourite emojis      : {ai_top_emojis}
    - Common phrases        : {ai_top_phrases}
    - Emoji frequency       : {ai_pattern['emoji_per_msg']} emojis per message

    === PERSON YOU ARE TALKING TO ({user_pattern['username']}) ===
    - Their tone          : {user_pattern['tone']}
    - Their common words  : {user_top_words}
    - Their emojis        : {user_top_emojis}
    - Their mood          : {user_pattern['mood_score']}/10

    === STRICT RULES ===
    1. Always reply in Hinglish (mix of Hindi and English)
    2. Keep replies SHORT — max {int(ai_pattern['avg_words_per_msg']) + 5} words
    3. Use YOUR favourite emojis naturally
    4. Use YOUR common words and phrases
    5. Never break character — you ARE {ai_pattern['username']}
    6. Match casual informal WhatsApp chat vibe
    7. Never use formal language or long paragraphs
    8. If unsure reply casually like "pata nahi yaar 😂"
    9. Be aware of who you are talking to and respond naturally

    You are NOT an AI assistant.
    You are {ai_pattern['username']} chatting with {user_pattern['username']} on WhatsApp.
    """.strip()

    # ------------------------------------------------------------------ #
    #  Chat Session                                                        #
    # ------------------------------------------------------------------ #

    def start_session(self, ai_username: str, 
                        user_username: str, model_name: str):
            """
            Start a new chat session with two roles defined.
            AI impersonates ai_username talking to user_username.

            :param ai_username: The user the AI will impersonate
            :param user_username: The user the human is playing as
            :param model_name: Gemini model name to use
            """
            ai_pattern   = self.get_pattern(ai_username)
            user_pattern = self.get_pattern(user_username)

            system_prompt = self._build_system_prompt(
                ai_pattern, user_pattern
            )

            # Initialize Gemini model with system prompt
            self.system_prompt = system_prompt
            self.model_name    = model_name
            self.session       = []
            self.active_user  = ai_username
            self.active_model = model_name
            self.chat_history = []

    def chat(self, user_message: str) -> str:
        """
        Send a message and get response in the style of the person.

        :param user_message: Message from the user
        :return: Agent response string
        """
        if self.session is None:
            raise ValueError(
                "No active session. Call start_session() first."
            )

        # Send message to Gemini
        # Build messages list with history
        messages = []
        for h in self.session:
            messages.append(
                types.Content(
                    role=h["role"],
                    parts=[types.Part(text=h["content"])]
                )
            )
        messages.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
        )

        # Call Gemini API
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                max_output_tokens=150,
                temperature=0.85,
            )
        )
        reply = response.text.strip()

        # Update session history
        self.session.append({
            "role": "user", "content": user_message
        })
        self.session.append({
            "role": "model", "content": reply
        })

        # Track history manually for display
        self.chat_history.append({
            "role":    "user",
            "content": user_message
        })
        self.chat_history.append({
            "role":    "agent",
            "content": reply
        })

        return reply

    def reset_session(self):
            """Clear conversation and restart session."""
            if self.active_user and self.active_model:
                # Store user role before reset
                user_role = getattr(self, 'active_user_role', self.active_user)
                self.start_session(
                    ai_username=self.active_user,
                    user_username=user_role,
                    model_name=self.active_model
                )

    def get_chat_history(self) -> list:
        """Return full conversation history."""
        return self.chat_history

    def get_users(self) -> list:
        """Return list of users available for impersonation."""
        return list(self.patterns.keys())