# =============================================================================
# analyzer.py — Analytics Class
# Inherits from Base — computes all chat analytics
# =============================================================================

import pandas as pd
from collections import Counter
from wordcloud import WordCloud
from core.base import Base


class Analyzer(Base):
    """
    Handles all chat analytics computations.
    Inherits shared utilities from Base superclass.

    Covers:
    - Basic stats
    - Monthly and daily timelines
    - Activity maps and heatmaps
    - Most busy users
    - WordCloud generation
    - Most common words
    - Emoji analysis
    - Response time analysis
    - Conversation starter analysis
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize Analyzer with processed chat DataFrame.

        :param df: Clean chat DataFrame from Preprocessor
        """
        if not self.validate_dataframe(df):
            raise ValueError("Invalid or empty DataFrame provided.")
        self.df = df

    # ------------------------------------------------------------------ #
    #  Basic Stats                                                         #
    # ------------------------------------------------------------------ #

    def fetch_basic_stats(self, selected_user: str) -> dict:
        """
        Fetch top level statistics for selected user or overall.

        :param selected_user: Username or 'Overall'
        :return: Dictionary of stats
        """
        df = self.filter_by_user(self.df, selected_user)

        return {
            "total_messages": self.format_number(len(df)),
            "total_words":    self.format_number(int(df["word_count"].sum())),
            "total_media":    self.format_number(int(df["is_media"].sum())),
            "total_links":    self.format_number(int(df["has_link"].sum())),
        }

    # ------------------------------------------------------------------ #
    #  Timelines                                                           #
    # ------------------------------------------------------------------ #

    def monthly_timeline(self, selected_user: str) -> pd.DataFrame:
        """
        Get message count grouped by month.

        :param selected_user: Username or 'Overall'
        :return: DataFrame with time and message count columns
        """
        df = self.filter_by_user(self.df, selected_user)

        timeline = df.groupby(
            ["year", "month_num", "month"]
        ).size().reset_index(name="messages")

        timeline = timeline.sort_values(["year", "month_num"])
        timeline["time"] = (
            timeline["month"] + " " + timeline["year"].astype(str)
        )

        return timeline[["time", "messages"]]

    def daily_timeline(self, selected_user: str) -> pd.DataFrame:
        """
        Get message count grouped by date.

        :param selected_user: Username or 'Overall'
        :return: DataFrame with date and message count columns
        """
        df = self.filter_by_user(self.df, selected_user)

        timeline = df.groupby("date").size().reset_index(name="messages")
        timeline = timeline.sort_values("date")
        timeline["date"] = timeline["date"].astype(str)

        return timeline

    # ------------------------------------------------------------------ #
    #  Activity Maps                                                       #
    # ------------------------------------------------------------------ #

    def busiest_day(self, selected_user: str) -> pd.Series:
        """
        Get message count per day of week.

        :param selected_user: Username or 'Overall'
        :return: Series indexed by day name
        """
        df = self.filter_by_user(self.df, selected_user)

        day_order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        return df["day"].value_counts().reindex(day_order, fill_value=0)

    def busiest_month(self, selected_user: str) -> pd.Series:
        """
        Get message count per month.

        :param selected_user: Username or 'Overall'
        :return: Series indexed by month name
        """
        df = self.filter_by_user(self.df, selected_user)

        month_order = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        return df["month"].value_counts().reindex(
            month_order, fill_value=0
        )

    def activity_heatmap(self, selected_user: str) -> pd.DataFrame:
        """
        Build pivot table of message count by day vs hour.

        :param selected_user: Username or 'Overall'
        :return: Pivot DataFrame (day x hour)
        """
        df = self.filter_by_user(self.df, selected_user)

        day_order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        pivot = df.pivot_table(
            index="day",
            columns="hour",
            values="message",
            aggfunc="count"
        ).reindex(day_order).fillna(0)

        return pivot

    # ------------------------------------------------------------------ #
    #  User Analysis                                                       #
    # ------------------------------------------------------------------ #

    def most_busy_users(self) -> tuple:
        """
        Get most active users in the group chat.

        :return: Tuple of (Series of counts, DataFrame with percentage)
        """
        counts = self.df["username"].value_counts()

        percent_df = pd.DataFrame({
            "username":   counts.index,
            "messages":   counts.values,
            "percentage": (
                counts.values / counts.sum() * 100
            ).round(2)
        })

        return counts, percent_df

    # ------------------------------------------------------------------ #
    #  Word Analysis                                                       #
    # ------------------------------------------------------------------ #

    def generate_wordcloud(self, selected_user: str) -> WordCloud:
        """
        Generate a WordCloud from chat messages.

        :param selected_user: Username or 'Overall'
        :return: WordCloud object
        """
        df = self.filter_by_user(self.df, selected_user)
        df = self.filter_text_messages(df)

        stopwords_set = self.load_stopwords()

        text = " ".join(df["message"].tolist())
        text = self.clean_text(text)

        return WordCloud(
            width=800,
            height=400,
            background_color="#0D1117",
            colormap="Greens",
            stopwords=stopwords_set,
            max_words=100,
            min_font_size=10,
        ).generate(text)

    def most_common_words(self, selected_user: str,
                           top_n: int = 20) -> pd.DataFrame:
        """
        Get the most commonly used words.

        :param selected_user: Username or 'Overall'
        :param top_n: Number of top words to return
        :return: DataFrame with word and count columns
        """
        df = self.filter_by_user(self.df, selected_user)
        df = self.filter_text_messages(df)

        stopwords_set = self.load_stopwords()
        words = self.extract_words(df["message"], stopwords_set)

        word_counts = Counter(words).most_common(top_n)

        return pd.DataFrame(word_counts, columns=["word", "count"])

    # ------------------------------------------------------------------ #
    #  Emoji Analysis                                                      #
    # ------------------------------------------------------------------ #

    def emoji_analysis(self, selected_user: str) -> pd.DataFrame:
        """
        Extract and count all emojis used in chat.

        :param selected_user: Username or 'Overall'
        :return: DataFrame with emoji and frequency columns
        """
        df = self.filter_by_user(self.df, selected_user)

        emoji_counter = self.count_emojis(df["message"])

        return pd.DataFrame(
            emoji_counter.most_common(),
            columns=["emoji", "frequency"]
        )

    # ------------------------------------------------------------------ #
    #  Response Time Analysis                                              #
    # ------------------------------------------------------------------ #

    def response_time_analysis(self) -> pd.DataFrame:
        """
        Calculate average response time per user in minutes.

        :return: DataFrame with username and avg_response_minutes
        """
        df = self.df.sort_values("datetime").copy()

        df["prev_datetime"] = df["datetime"].shift(1)
        df["prev_user"]     = df["username"].shift(1)

        # Only count responses to a different user
        responses = df[df["username"] != df["prev_user"]].copy()
        responses["response_minutes"] = (
            responses["datetime"] - responses["prev_datetime"]
        ).dt.total_seconds() / 60

        # Filter out unrealistic response times (over 12 hours)
        responses = responses[responses["response_minutes"] < 720]

        result = responses.groupby("username")[
            "response_minutes"
        ].mean().round(2).reset_index()

        result.columns = ["username", "avg_response_minutes"]
        result = result.sort_values("avg_response_minutes")

        return result

    # ------------------------------------------------------------------ #
    #  Conversation Starter Analysis                                       #
    # ------------------------------------------------------------------ #

    def conversation_starters(self) -> pd.DataFrame:
        """
        Identify who starts conversations most often.
        A conversation starter is a message sent after
        more than 1 hour of silence.

        :return: DataFrame with username and starter count
        """
        df = self.df.sort_values("datetime").copy()

        df["prev_datetime"] = df["datetime"].shift(1)
        df["gap_minutes"]   = (
            df["datetime"] - df["prev_datetime"]
        ).dt.total_seconds() / 60

        # Message after 60+ min gap = conversation starter
        starters = df[df["gap_minutes"] > 60]

        result = starters["username"].value_counts().reset_index()
        result.columns = ["username", "conversations_started"]

        return result