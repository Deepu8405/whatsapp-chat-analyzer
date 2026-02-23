# =============================================================================
# sentiment.py — Sentiment Analysis Class
# Inherits from Base — computes all sentiment related analytics
# =============================================================================

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from core.base import Base


class Sentiment(Base):
    """
    Handles all sentiment analysis computations.
    Inherits shared utilities from Base superclass.

    Covers:
    - Per message sentiment scoring
    - Overall sentiment summary
    - Sentiment timeline
    - Per user sentiment comparison
    - Toxic message detection
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize Sentiment with processed chat DataFrame.
        Automatically runs sentiment scoring on initialization.

        :param df: Clean chat DataFrame from Preprocessor
        """
        if not self.validate_dataframe(df):
            raise ValueError("Invalid or empty DataFrame provided.")

        self.analyzer = SentimentIntensityAnalyzer()
        self.df       = self._score_messages(df)

    # ------------------------------------------------------------------ #
    #  Scoring                                                             #
    # ------------------------------------------------------------------ #

    def _score_messages(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add sentiment scores to every message in the DataFrame.
        Called automatically on initialization.

        :param df: Clean chat DataFrame
        :return: DataFrame with sentiment columns added
        """
        df = df.copy()

        # Score each message
        scores = df["message"].apply(
            lambda msg: self.analyzer.polarity_scores(str(msg))
        )

        # Extract individual score components
        df["sentiment_positive"] = scores.apply(lambda x: x["pos"])
        df["sentiment_negative"] = scores.apply(lambda x: x["neg"])
        df["sentiment_neutral"]  = scores.apply(lambda x: x["neu"])
        df["sentiment_compound"] = scores.apply(lambda x: x["compound"])

        # Classify each message as Positive, Negative or Neutral
        df["sentiment_label"] = df["sentiment_compound"].apply(
            self._classify
        )

        return df

    @staticmethod
    def _classify(compound: float) -> str:
        """
        Classify sentiment compound score into a label.

        :param compound: VADER compound score (-1 to +1)
        :return: 'Positive', 'Negative' or 'Neutral'
        """
        if compound >= 0.05:
            return "Positive"
        elif compound <= -0.05:
            return "Negative"
        else:
            return "Neutral"

    # ------------------------------------------------------------------ #
    #  Overall Sentiment                                                   #
    # ------------------------------------------------------------------ #

    def get_overall_sentiment(self, selected_user: str) -> dict:
        """
        Get overall sentiment summary for selected user.

        :param selected_user: Username or 'Overall'
        :return: Dictionary with sentiment percentages and mood score
        """
        df     = self.filter_by_user(self.df, selected_user)
        total  = len(df)
        counts = df["sentiment_label"].value_counts()

        positive = counts.get("Positive", 0)
        negative = counts.get("Negative", 0)
        neutral  = counts.get("Neutral",  0)

        # Scale compound score from -1/+1 range to 0-10 mood score
        avg_compound = df["sentiment_compound"].mean()
        mood_score   = round((avg_compound + 1) * 5, 2)

        return {
            "positive_pct":   round(positive / total * 100, 2),
            "negative_pct":   round(negative / total * 100, 2),
            "neutral_pct":    round(neutral  / total * 100, 2),
            "mood_score":     mood_score,
            "total_messages": total,
        }

    # ------------------------------------------------------------------ #
    #  Sentiment Timeline                                                  #
    # ------------------------------------------------------------------ #

    def sentiment_timeline(self, selected_user: str) -> pd.DataFrame:
        """
        Get average sentiment compound score per month.

        :param selected_user: Username or 'Overall'
        :return: DataFrame with time and avg sentiment columns
        """
        df = self.filter_by_user(self.df, selected_user)

        timeline = df.groupby(
            ["year", "month_num", "month"]
        )["sentiment_compound"].mean().reset_index()

        timeline = timeline.sort_values(["year", "month_num"])
        timeline["time"] = (
            timeline["month"] + " " + timeline["year"].astype(str)
        )
        timeline["sentiment_compound"] = timeline[
            "sentiment_compound"
        ].round(3)

        return timeline[["time", "sentiment_compound"]]

    # ------------------------------------------------------------------ #
    #  Sentiment Heatmap                                                   #
    # ------------------------------------------------------------------ #

    def sentiment_heatmap(self, selected_user: str) -> pd.DataFrame:
        """
        Build pivot table of avg sentiment by day vs hour.

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
            values="sentiment_compound",
            aggfunc="mean"
        ).reindex(day_order).fillna(0).round(3)

        return pivot

    # ------------------------------------------------------------------ #
    #  Per User Sentiment                                                  #
    # ------------------------------------------------------------------ #

    def per_user_sentiment(self) -> pd.DataFrame:
        """
        Get sentiment breakdown for each user.

        :return: DataFrame with per user sentiment stats
        """
        results = []

        for user in self.df["username"].unique():
            user_df = self.df[self.df["username"] == user]
            counts  = user_df["sentiment_label"].value_counts()
            total   = len(user_df)

            avg_compound = user_df["sentiment_compound"].mean()

            results.append({
                "username":     user,
                "positive_pct": round(
                    counts.get("Positive", 0) / total * 100, 2
                ),
                "neutral_pct":  round(
                    counts.get("Neutral",  0) / total * 100, 2
                ),
                "negative_pct": round(
                    counts.get("Negative", 0) / total * 100, 2
                ),
                "mood_score":   round((avg_compound + 1) * 5, 2)
            })

        return pd.DataFrame(results)

    # ------------------------------------------------------------------ #
    #  Toxic Message Detection                                             #
    # ------------------------------------------------------------------ #

    def detect_toxic_messages(self, selected_user: str,
                               threshold: float = -0.5) -> pd.DataFrame:
        """
        Flag messages with high negativity as potentially toxic.

        :param selected_user: Username or 'Overall'
        :param threshold: Compound score below which msg is flagged
        :return: DataFrame of flagged messages
        """
        df    = self.filter_by_user(self.df, selected_user)
        toxic = df[df["sentiment_compound"] <= threshold].copy()
        toxic = toxic.sort_values("sentiment_compound", ascending=True)

        return toxic[[
            "username", "message",
            "sentiment_compound", "date"
        ]].reset_index(drop=True)

    def get_scored_df(self) -> pd.DataFrame:
        """
        Return the full sentiment scored DataFrame.
        Used by Agent class to build personality profile.

        :return: DataFrame with all sentiment columns
        """
        return self.df.copy()