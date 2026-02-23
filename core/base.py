# =============================================================================
# base.py — Master Base/Super Class
# All shared reusable methods live here
# Every core class inherits from this
# =============================================================================

import pandas as pd
import re
import emoji
from collections import Counter
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
nltk.download("stopwords", quiet=True)
nltk.download("punkt",     quiet=True)


class Base:
    """
    Master superclass for all core classes.
    Contains shared utility methods reused across
    Preprocessor, Analyzer, Sentiment and Agent classes.
    """

    # ------------------------------------------------------------------ #
    #  Text Cleaning                                                       #
    # ------------------------------------------------------------------ #

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean raw message text.
        Removes mentions, special characters and extra spaces.

        :param text: Raw message string
        :return: Cleaned string
        """
        # Remove WhatsApp mentions (@username)
        text = re.sub(r'@\S+', '', text)

        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)

        # Remove special characters but keep letters, numbers, spaces
        text = re.sub(r'[^\w\s]', '', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text.lower()

    # ------------------------------------------------------------------ #
    #  Stopwords                                                           #
    # ------------------------------------------------------------------ #

    @staticmethod
    def load_stopwords() -> set:
        """
        Load combined English + Hinglish stopwords.

        :return: Set of stopwords
        """
        # English stopwords from NLTK
        english_stops = set(stopwords.words("english"))

        # Common Hinglish stopwords
        hinglish_stops = {
            "hai", "hain", "ho", "tha", "thi", "the", "ko", "ka", "ki",
            "ke", "se", "me", "mein", "par", "pe", "bhi", "nahi", "nhi",
            "na", "mat", "kya", "kyu", "kyun", "kyunki", "aur", "ya",
            "toh", "to", "hi", "jo", "jab", "tab", "ab", "abb", "yaar",
            "yar", "bhai", "ek", "koi", "sab", "bahut", "thoda", "phir",
            "fir", "woh", "wo", "wahi", "yahi", "agar", "lekin", "magar",
            "bas", "hua", "hui", "hue", "kar", "karo", "karna", "karte",
            "raha", "rahi", "rahe", "liye", "uska", "uski", "unka",
            "unki", "mera", "meri", "tera", "teri", "hamara", "tumhara",
            "apna", "apni", "media", "omitted", "message", "deleted",
            "missed", "call", "video", "acha", "accha", "okay", "ok",
            "haa", "haan", "han", "are", "bro", "yr", "yrr", "abhi",
            "bilkul", "sahi", "thik", "rha", "rhi", "rhaa", "h", "ha",
            "le", "kr", "ye", "wo", "jo", "de", "lo", "lu", "ja", "aa",
            "mai", "main", "tu", "tum", "hum", "aap", "vo", "is", "us",
            "iss", "usse", "inhe", "unhe", "kuch", "kaafi", "itna",
            "utna", "wala", "wali", "wale", "dono", "teeno", "saare"
        }

        return english_stops.union(hinglish_stops)

    # ------------------------------------------------------------------ #
    #  Emoji Utilities                                                     #
    # ------------------------------------------------------------------ #

    @staticmethod
    def extract_emojis(text: str) -> list:
        """
        Extract all emojis from a text string.

        :param text: Message string
        :return: List of emoji characters
        """
        return [char for char in text if char in emoji.EMOJI_DATA]

    @staticmethod
    def count_emojis(texts: pd.Series) -> Counter:
        """
        Count emoji frequency across a series of messages.

        :param texts: Pandas Series of message strings
        :return: Counter of emoji frequencies
        """
        all_emojis = []
        for text in texts:
            all_emojis.extend(
                [char for char in str(text) if char in emoji.EMOJI_DATA]
            )
        return Counter(all_emojis)

    # ------------------------------------------------------------------ #
    #  Word Utilities                                                      #
    # ------------------------------------------------------------------ #

    @classmethod
    def extract_words(cls, texts: pd.Series, 
                       stopwords_set: set = None) -> list:
        """
        Extract clean words from a series of messages.
        Filters out stopwords, short words and noise.

        :param texts: Pandas Series of message strings
        :param stopwords_set: Optional custom stopwords set
        :return: List of clean words
        """
        if stopwords_set is None:
            stopwords_set = cls.load_stopwords()

        words = []
        for text in texts:
            for word in str(text).lower().split():
                word = re.sub(r'[^\w]', '', word)
                if word and word not in stopwords_set and len(word) > 1:
                    words.append(word)

        return words

    # ------------------------------------------------------------------ #
    #  DataFrame Utilities                                                 #
    # ------------------------------------------------------------------ #

    @staticmethod
    def filter_by_user(df: pd.DataFrame, 
                        selected_user: str) -> pd.DataFrame:
        """
        Filter DataFrame by selected user.
        Returns full DataFrame if 'Overall' is selected.

        :param df: Chat DataFrame
        :param selected_user: Username or 'Overall'
        :return: Filtered DataFrame
        """
        if selected_user != "Overall":
            return df[df["username"] == selected_user].copy()
        return df.copy()

    @staticmethod
    def filter_text_messages(df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter out media messages — keep text only.

        :param df: Chat DataFrame
        :return: DataFrame with only text messages
        """
        return df[df["is_media"] == False].copy()

    @staticmethod
    def validate_dataframe(df: pd.DataFrame) -> bool:
        """
        Validate that the DataFrame has required columns
        and is not empty.

        :param df: Chat DataFrame
        :return: True if valid, False otherwise
        """
        required_columns = [
            "datetime", "username", "message",
            "is_media", "word_count", "has_link"
        ]

        if df is None or df.empty:
            return False

        return all(col in df.columns for col in required_columns)

    # ------------------------------------------------------------------ #
    #  Link Utilities                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def extract_links(text: str) -> list:
        """
        Extract all URLs from a message.

        :param text: Message string
        :return: List of URLs found
        """
        return re.findall(r'http[s]?://\S+', str(text))

    # ------------------------------------------------------------------ #
    #  Formatting Utilities                                                #
    # ------------------------------------------------------------------ #

    @staticmethod
    def format_number(num: int) -> str:
        """
        Format large numbers with commas for display.
        e.g. 38291 → '38,291'

        :param num: Integer number
        :return: Formatted string
        """
        return f"{num:,}"

    @staticmethod
    def format_percentage(value: float) -> str:
        """
        Format float as percentage string.
        e.g. 62.5 → '62.5%'

        :param value: Float value
        :return: Formatted percentage string
        """
        return f"{value:.1f}%"