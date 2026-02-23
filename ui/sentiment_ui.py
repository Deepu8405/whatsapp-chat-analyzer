# =============================================================================
# sentiment_ui.py — Sentiment Analysis UI Component
# Renders all sentiment sections with real data from Sentiment class
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
from config.settings import AppConfig
from core.sentiment import Sentiment


class SentimentUI:
    """
    Manages the entire Sentiment Analysis UI.
    Receives real data from Sentiment class.
    Each section is a separate method for clean separation.
    """

    def __init__(self, selected_user: str, sentiment: Sentiment):
        """
        Initialize SentimentUI with selected user and Sentiment instance.

        :param selected_user: User selected from sidebar
        :param sentiment: Sentiment instance with scored chat data
        """
        self.selected_user = selected_user
        self.sentiment     = sentiment

    def render(self):
        """Main render method — builds complete sentiment UI."""
        self._render_header()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_overall_sentiment()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_sentiment_timeline()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_per_user_sentiment()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_toxic_messages()

    # ------------------------------------------------------------------ #
    #  Header                                                              #
    # ------------------------------------------------------------------ #

    def _render_header(self):
        """Render sentiment page header and user badge."""
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"<h2 style='color:{AppConfig.PRIMARY_COLOR};"
                f"margin-bottom:0;'>🧠 Sentiment Analysis</h2>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='color:{AppConfig.TEXT_SECONDARY};"
                f"font-size:0.88rem;'>"
                f"Understand the emotional tone and mood patterns "
                f"in your chat.</p>",
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"<div style='background:{AppConfig.CARD_BACKGROUND};"
                f"border:1px solid {AppConfig.PRIMARY_COLOR};"
                f"border-radius:20px; padding:6px 16px;"
                f"text-align:center; color:{AppConfig.PRIMARY_COLOR};"
                f"font-size:0.85rem; margin-top:10px;'>"
                f"👤 {self.selected_user}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            f"<hr style='border:1px solid {AppConfig.BORDER_COLOR};"
            f"margin:10px 0 24px 0;'>",
            unsafe_allow_html=True
        )

    # ------------------------------------------------------------------ #
    #  Overall Sentiment                                                   #
    # ------------------------------------------------------------------ #

    def _render_overall_sentiment(self):
        """Render overall sentiment score cards with real data."""
        self._render_section_label("🎯 Overall Sentiment Score")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Overall sentiment gives you an instant <b style="color:#25D366;">emotional fingerprint</b> of the entire chat.<br>
            • <b style="color:#25D366;">Positive %</b> — Percentage of messages with happy, excited or agreeable tone.
            e.g. 62% positive means the group has a generally upbeat and friendly atmosphere.<br>
            • <b style="color:#25D366;">Neutral %</b> — Factual or informational messages with no strong emotion.
            High neutral % is common in planning or task-oriented groups.<br>
            • <b style="color:#25D366;">Negative %</b> — Messages with frustration, disagreement or sad tone.
            A small negative % is healthy and normal. Anything above 20% may indicate frequent conflicts.<br>
            • <b style="color:#25D366;">Mood Score</b> — Composite score out of 10 representing the overall emotional health of the chat.
            e.g. 7.2/10 = positive and emotionally healthy group dynamic.
        """)

        scores = self.sentiment.get_overall_sentiment(self.selected_user)

        col1, col2, col3, col4 = st.columns(4)

        cards = [
            ("😊", "Positive",   f"{scores['positive_pct']}%",  AppConfig.POSITIVE_COLOR),
            ("😐", "Neutral",    f"{scores['neutral_pct']}%",   AppConfig.NEUTRAL_COLOR),
            ("😠", "Negative",   f"{scores['negative_pct']}%",  AppConfig.NEGATIVE_COLOR),
            ("🎭", "Mood Score", f"{scores['mood_score']}/10",  AppConfig.PURPLE_COLOR),
        ]

        for col, (icon, label, value, color) in zip(
            [col1, col2, col3, col4], cards
        ):
            with col:
                st.markdown(f"""
                    <div style="
                        background:{AppConfig.CARD_BACKGROUND};
                        border:1px solid {color};
                        border-radius:12px;
                        padding:20px 16px;
                        text-align:center;
                    ">
                        <div style="font-size:1.8rem;">{icon}</div>
                        <div style="color:{AppConfig.TEXT_SECONDARY};
                             font-size:0.78rem; text-transform:uppercase;
                             letter-spacing:1px;
                             margin:6px 0 4px 0;">{label}</div>
                        <div style="color:{color}; font-size:1.8rem;
                             font-weight:800;">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ------------------------------------------------------------------ #
    #  Sentiment Timeline                                                  #
    # ------------------------------------------------------------------ #

    def _render_sentiment_timeline(self):
        """Render sentiment timeline and heatmap with real data."""
        self._render_section_label("📅 Sentiment Over Time")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Sentiment timeline tracks how the <b style="color:#25D366;">emotional tone evolved</b> over months.<br>
            • <b style="color:#25D366;">Monthly Mood Timeline</b> — Green bars = net positive months, Red bars = net negative months.
            e.g. A dip in November followed by recovery in December could indicate a conflict that got resolved over time.<br>
            • <b style="color:#25D366;">Sentiment Heatmap</b> — Reveals which day and hour combinations have the most positive or negative conversations.
            e.g. Late night conversations on weekends tend to be more emotional and expressive compared to daytime chats.
        """)

        col1, col2 = st.columns(2)

        with col1:
            timeline = self.sentiment.sentiment_timeline(
                self.selected_user
            )

            # Color bars green/red based on positive/negative
            colors = [
                AppConfig.POSITIVE_COLOR
                if v >= 0 else AppConfig.NEGATIVE_COLOR
                for v in timeline["sentiment_compound"]
            ]

            fig = go.Figure(go.Bar(
                x=timeline["time"],
                y=timeline["sentiment_compound"],
                marker_color=colors,
                opacity=0.85,
            ))
            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color=AppConfig.TEXT_SECONDARY,
                line_width=1
            )
            fig = self._apply_chart_style(
                fig, "📈 Monthly Mood Timeline"
            )
            st.plotly_chart(fig, width='stretch')

        with col2:
            heatmap_data = self.sentiment.sentiment_heatmap(
                self.selected_user
            )

            fig = go.Figure(go.Heatmap(
                z=heatmap_data.values,
                x=heatmap_data.columns.astype(str),
                y=heatmap_data.index,
                colorscale=[
                    [0.0, AppConfig.NEGATIVE_COLOR],
                    [0.5, AppConfig.CARD_BACKGROUND],
                    [1.0, AppConfig.POSITIVE_COLOR],
                ],
                showscale=True,
                colorbar=dict(
                    tickfont=dict(color="#FFFFFF"),
                ),
            ))
            fig.update_layout(
                title=dict(
                    text="🌡️ Sentiment Heatmap",
                    font=dict(
                        color=AppConfig.PRIMARY_COLOR, size=14
                    )
                ),
                paper_bgcolor=AppConfig.PLOT_BG,
                plot_bgcolor=AppConfig.CHART_BG,
                font=dict(color=AppConfig.TEXT_PRIMARY),
                margin=dict(l=20, r=20, t=40, b=20),
                height=AppConfig.CHART_HEIGHT,
                xaxis=dict(
                    title="Hour of Day",
                    tickfont=dict(color="#FFFFFF"),
                    gridcolor=AppConfig.GRIDLINE_COLOR,
                ),
                yaxis=dict(
                    tickfont=dict(color="#FFFFFF"),
                    gridcolor=AppConfig.GRIDLINE_COLOR,
                ),
            )
            st.plotly_chart(fig, width='stretch')

    # ------------------------------------------------------------------ #
    #  Per User Sentiment                                                  #
    # ------------------------------------------------------------------ #

    def _render_per_user_sentiment(self):
        """Render per user sentiment comparison with real data."""
        self._render_section_label("👥 Per User Sentiment")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Per user sentiment breaks down the <b style="color:#25D366;">emotional contribution of each person</b> in the chat.<br>
            • <b style="color:#25D366;">User Sentiment Comparison</b> — Side by side comparison of positivity, neutrality and negativity per person.
            e.g. If one person has 40% negative messages they may be the source of tension or simply very expressive with frustration.<br>
            • <b style="color:#25D366;">Mood Score Distribution</b> — Who brings the most positive energy to the group?
            The person with the highest mood score is the group's <b style="color:#25D366;">emotional anchor</b> — 
            they consistently uplift the conversation.<br>
            • <b style="color:#25D366;">Individual Score Cards</b> — Quick reference for each person's emotional profile.
            Useful for understanding interpersonal dynamics and who drives positivity vs negativity.
        """)

        user_sentiment = self.sentiment.per_user_sentiment()

        col1, col2 = st.columns(2)

        with col1:
            x      = list(range(len(user_sentiment)))
            width  = 0.25

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Positive",
                x=user_sentiment["username"],
                y=user_sentiment["positive_pct"],
                marker_color=AppConfig.POSITIVE_COLOR,
            ))
            fig.add_trace(go.Bar(
                name="Neutral",
                x=user_sentiment["username"],
                y=user_sentiment["neutral_pct"],
                marker_color=AppConfig.NEUTRAL_COLOR,
            ))
            fig.add_trace(go.Bar(
                name="Negative",
                x=user_sentiment["username"],
                y=user_sentiment["negative_pct"],
                marker_color=AppConfig.NEGATIVE_COLOR,
            ))
            fig.update_layout(barmode="group")
            fig = self._apply_chart_style(
                fig, "📊 User Sentiment Comparison"
            )
            st.plotly_chart(fig, width='stretch')

        with col2:
            fig = go.Figure(go.Pie(
                labels=user_sentiment["username"],
                values=user_sentiment["mood_score"],
                hole=0.4,
                marker=dict(colors=[
                    AppConfig.POSITIVE_COLOR,
                    AppConfig.SECONDARY_COLOR,
                    AppConfig.PURPLE_COLOR,
                    AppConfig.NEUTRAL_COLOR,
                ][:len(user_sentiment)])
            ))
            fig = self._apply_chart_style(
                fig, "🥧 Mood Score Distribution"
            )
            st.plotly_chart(fig, width='stretch')

        # Mood score cards per user
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(len(user_sentiment))

        for col, (_, row) in zip(cols, user_sentiment.iterrows()):
            with col:
                mood   = row["mood_score"]
                color  = (
                    AppConfig.POSITIVE_COLOR if mood >= 6
                    else AppConfig.NEUTRAL_COLOR if mood >= 4
                    else AppConfig.NEGATIVE_COLOR
                )
                st.markdown(f"""
                    <div style="
                        background:{AppConfig.CARD_BACKGROUND};
                        border:1px solid {color};
                        border-radius:12px;
                        padding:16px 12px;
                        text-align:center;
                    ">
                        <div style="color:{AppConfig.TEXT_SECONDARY};
                             font-size:0.75rem; text-transform:uppercase;
                             letter-spacing:1px;">
                             {row['username']}</div>
                        <div style="color:{color}; font-size:1.5rem;
                             font-weight:800; margin-top:6px;">
                             {mood}/10</div>
                        <div style="color:{AppConfig.TEXT_SECONDARY};
                             font-size:0.72rem; margin-top:4px;">
                             😊 {row['positive_pct']}% &nbsp;
                             😠 {row['negative_pct']}%</div>
                    </div>
                """, unsafe_allow_html=True)

    # ------------------------------------------------------------------ #
    #  Toxic Messages                                                      #
    # ------------------------------------------------------------------ #

    def _render_toxic_messages(self):
        """Render toxic message detection with real data."""
        self._render_section_label("⚠️ Toxic Message Detection")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Toxic message detection flags <b style="color:#25D366;">highly negative or aggressive messages</b> that may indicate conflict.<br>
            • <b style="color:#25D366;">Flagged Messages</b> — Messages with a compound sentiment score below -0.5 are flagged.
            These are messages with strong negative language, frustration or potential conflict triggers.
            e.g. An argument about plans or responsibilities often shows up here.<br>
            • <b style="color:#25D366;">Toxicity Per User</b> — Which person sends the most flagged messages?
            Important note: A high count does not always mean a toxic person — 
            it could simply mean they are more <b style="color:#25D366;">emotionally expressive</b> in their communication style.
        """)

        toxic_df = self.sentiment.detect_toxic_messages(
            self.selected_user, threshold=-0.5
        )

        col1, col2 = st.columns(2)

        with col1:
            if toxic_df.empty:
                self._render_empty_state(
                    "🎉 No toxic messages detected!"
                )
            else:
                st.markdown(
                    f"<p style='color:{AppConfig.NEGATIVE_COLOR};"
                    f"font-size:0.88rem;'>"
                    f"🚨 {len(toxic_df)} flagged messages found</p>",
                    unsafe_allow_html=True
                )
                # Show flagged messages table
                st.dataframe(
                    toxic_df[["username", "message",
                               "sentiment_compound", "date"]],
                    use_container_width=True,
                    hide_index=True,
                )

        with col2:
            if not toxic_df.empty:
                toxic_counts = toxic_df["username"].value_counts()
                fig = go.Figure(go.Bar(
                    x=toxic_counts.index,
                    y=toxic_counts.values,
                    marker_color=AppConfig.NEGATIVE_COLOR,
                ))
                fig = self._apply_chart_style(
                    fig, "📊 Toxic Messages Per User"
                )
                st.plotly_chart(fig, width='stretch')
            else:
                self._render_empty_state(
                    "No data to display"
                )

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _apply_chart_style(
        self, fig: go.Figure, title: str
    ) -> go.Figure:
        """
        Apply consistent dark theme to all charts.

        :param fig: Plotly figure
        :param title: Chart title
        :return: Styled figure
        """
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(color=AppConfig.PRIMARY_COLOR, size=14)
            ),
            paper_bgcolor=AppConfig.PLOT_BG,
            plot_bgcolor=AppConfig.CHART_BG,
            font=dict(color=AppConfig.TEXT_PRIMARY),
            margin=dict(l=20, r=20, t=40, b=20),
            height=AppConfig.CHART_HEIGHT,
            xaxis=dict(gridcolor=AppConfig.GRIDLINE_COLOR),
            yaxis=dict(gridcolor=AppConfig.GRIDLINE_COLOR),
        )
        return fig

    def _render_section_label(self, label: str):
        """Render styled section label."""
        st.markdown(
            f"<p style='color:{AppConfig.TEXT_SECONDARY};"
            f"font-size:0.85rem; text-transform:uppercase;"
            f"letter-spacing:1px;'>{label}</p>",
            unsafe_allow_html=True
        )
    def _render_section_description(self, description: str):
        """
        Render a static description card below section label.

        :param description: HTML formatted description string
        """
        st.markdown(f"""
            <div style="
                background:{AppConfig.CARD_BACKGROUND};
                border-left:3px solid {AppConfig.PRIMARY_COLOR};
                border-radius:0 8px 8px 0;
                padding:12px 16px;
                margin-bottom:16px;
                font-size:0.83rem;
                color:{AppConfig.TEXT_SECONDARY};
                line-height:1.7;
            ">{description}</div>
        """, unsafe_allow_html=True)

    def _render_empty_state(self, message: str):
        """Render empty state card."""
        st.markdown(f"""
            <div style="
                background:{AppConfig.CARD_BACKGROUND};
                border:1px solid {AppConfig.BORDER_COLOR};
                border-radius:12px; padding:40px;
                text-align:center;
            ">
                <div style="color:{AppConfig.TEXT_SECONDARY};
                            font-size:0.9rem;">{message}</div>
            </div>
        """, unsafe_allow_html=True)