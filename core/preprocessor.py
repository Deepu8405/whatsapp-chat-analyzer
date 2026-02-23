# =============================================================================
# preprocessor.py — WhatsApp Chat Parser Class
# Inherits from Base — parses raw .txt export into clean DataFrame
# =============================================================================

import re
import pandas as pd
from datetime import datetime
from core.base import Base


class Preprocessor(Base):
    """
    Handles parsing of raw WhatsApp chat export .txt files.
    Inherits shared utilities from Base superclass.

    Supports:
    - DD/MM/YY and DD/MM/YYYY date formats
    - 12hr am/pm time format
    - Group and individual chats
    - Media omitted messages
    - Multi line messages
    - System message filtering
    """

    # Regex pattern matching: 03/11/25, 10:15 pm -
    MESSAGE_PATTERN = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[aApP][mM]\s-\s'

    def __init__(self):
        """Initialize Preprocessor with empty state."""
        self.raw_data = None
        self.df       = None

    def load(self, raw_text: str) -> "Preprocessor":
        """
        Load raw chat text into the preprocessor.

        :param raw_text: Raw string content of WhatsApp .txt export
        :return: self for method chaining
        """
        self.raw_data = raw_text
        return self

    def process(self) -> pd.DataFrame:
        """
        Main method — parse raw chat text into clean DataFrame.
        Calls all private parsing steps in sequence.

        :return: Clean pandas DataFrame
        """
        if not self.raw_data:
            raise ValueError("No data loaded. Call load() first.")

        # Step 1: Split into messages and timestamps
        messages, timestamps = self._split_messages()

        # Step 2: Build records list
        records = self._build_records(messages, timestamps)

        # Step 3: Create DataFrame
        self.df = self._create_dataframe(records)

        return self.df

    def get_users(self) -> list:
        """
        Get sorted list of unique users with 'Overall' prepended.

        :return: List of usernames
        """
        if self.df is None:
            raise ValueError("No data processed. Call process() first.")

        users = sorted(self.df["username"].unique().tolist())
        users.insert(0, "Overall")
        return users

    # ------------------------------------------------------------------ #
    #  Private Methods                                                     #
    # ------------------------------------------------------------------ #

    def _split_messages(self) -> tuple:
        """
        Split raw chat text into individual messages and timestamps.

        :return: Tuple of (messages list, timestamps list)
        """
        messages   = re.split(self.MESSAGE_PATTERN, self.raw_data)[1:]
        timestamps = re.findall(self.MESSAGE_PATTERN, self.raw_data)
        return messages, timestamps

    def _parse_timestamp(self, timestamp: str) -> datetime | None:
        """
        Parse timestamp string into datetime object.
        Tries both 2 digit and 4 digit year formats.

        :param timestamp: Raw timestamp string
        :return: datetime object or None if parsing fails
        """
        timestamp = timestamp.strip().rstrip('-').strip()

        for fmt in ["%d/%m/%y, %I:%M %p", "%d/%m/%Y, %I:%M %p"]:
            try:
                return datetime.strptime(timestamp, fmt)
            except ValueError:
                continue
        return None

    def _build_records(self, messages: list,
                        timestamps: list) -> list:
        """
        Build list of record dicts from messages and timestamps.
        Filters out system messages and empty messages.

        :param messages: List of raw message strings
        :param timestamps: List of raw timestamp strings
        :return: List of record dictionaries
        """
        records = []

        for timestamp, message in zip(timestamps, messages):

            # Parse datetime
            dt = self._parse_timestamp(timestamp)
            if dt is None:
                continue

            # Clean message
            message = message.strip()

            # Separate username from message text
            if ': ' in message:
                username, msg_text = message.split(': ', 1)
            else:
                # System message — skip
                continue

            # Skip empty messages
            if not msg_text.strip():
                continue

            is_media = msg_text.strip() == "<Media omitted>"

            records.append({
                "datetime":  dt,
                "date":      dt.date(),
                "year":      dt.year,
                "month":     dt.strftime("%B"),
                "month_num": dt.month,
                "day":       dt.strftime("%A"),
                "day_num":   dt.weekday(),
                "hour":      dt.hour,
                "minute":    dt.minute,
                "username":  username.strip(),
                "message":   msg_text.strip(),
                "is_media":  is_media,
                "word_count": 0 if is_media else len(msg_text.strip().split()),
            })

        return records

    def _create_dataframe(self, records: list) -> pd.DataFrame:
        """
        Convert records list into a clean pandas DataFrame.
        Adds derived columns for links and emoji detection.

        :param records: List of record dictionaries
        :return: Clean pandas DataFrame
        """
        df = pd.DataFrame(records)

        # Add has_link column
        df["has_link"] = df["message"].apply(
            lambda x: bool(re.search(r'http[s]?://\S+', str(x)))
        )

        return df