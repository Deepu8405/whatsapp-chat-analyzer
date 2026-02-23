# =============================================================================
# dashboard.py — Main Dashboard Layout
# Renders all analytics sections with real data from Analyzer class
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from config.settings import AppConfig
from core.analyzer import Analyzer


class Dashboard:
    """
    Manages the main analytics dashboard layout.
    Receives real data from Analyzer class.
    Each section is a separate method for clean separation.
    """

    def __init__(self, selected_user: str, analyzer: Analyzer):
        """
        Initialize Dashboard with selected user and Analyzer instance.

        :param selected_user: User selected from sidebar
        :param analyzer: Analyzer instance with processed chat data
        """
        self.selected_user = selected_user
        self.analyzer      = analyzer

    def render(self):
        """Main render method — builds complete dashboard."""
        self._render_header()
        self._render_stats_cards()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_timeline_section()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_activity_section()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_busy_users_section()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_wordcloud_section()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_emoji_section()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_response_time_section()

    # ------------------------------------------------------------------ #
    #  Header                                                              #
    # ------------------------------------------------------------------ #

    def _render_header(self):
        """Render dashboard title and selected user badge."""
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"<h2 style='color:{AppConfig.PRIMARY_COLOR};"
                f"margin-bottom:0;'>📊 Analytics Dashboard</h2>",
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
    #  Stats Cards                                                         #
    # ------------------------------------------------------------------ #

    def _render_stats_cards(self):
        """Render the 4 top level metric stat cards with real data."""
        self._render_section_label("📈 Overview")

        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            These 4 KPIs give you an instant snapshot of the chat's overall activity.<br>
            • <b style="color:#25D366;">Total Messages</b> — Measures overall engagement level.
            A high count means an active group. e.g. 2,847 messages over 3 months = ~31 msgs/day showing consistent engagement.<br>
            • <b style="color:#25D366;">Total Words</b> — Reflects depth of conversation.
            High word count vs message count = people write long thoughtful replies.<br>
            • <b style="color:#25D366;">Media Shared</b> — Shows how visual the chat is.
            Groups with high media count tend to be more social/fun oriented.<br>
            • <b style="color:#25D366;">Links Shared</b> — Indicates information sharing behavior.
            High link count = knowledge sharing or news discussion group.
        """)

        stats = self.analyzer.fetch_basic_stats(self.selected_user)

        col1, col2, col3, col4 = st.columns(4)

        cards = [
            ("💬", "Total Messages", stats["total_messages"], ""),
            ("📝", "Total Words",    stats["total_words"],    ""),
            ("🖼️", "Media Shared",   stats["total_media"],    ""),
            ("🔗", "Links Shared",   stats["total_links"],    ""),
        ]

        for col, (icon, label, value, sub) in zip(
            [col1, col2, col3, col4], cards
        ):
            with col:
                st.markdown(f"""
                    <div style="
                        background:{AppConfig.CARD_BACKGROUND};
                        border:1px solid {AppConfig.BORDER_COLOR};
                        border-radius:12px;
                        padding:20px 16px;
                        text-align:center;
                    ">
                        <div style="font-size:1.8rem;">{icon}</div>
                        <div style="color:{AppConfig.TEXT_SECONDARY};
                             font-size:0.78rem; text-transform:uppercase;
                             letter-spacing:1px;
                             margin:6px 0 4px 0;">{label}</div>
                        <div style="color:{AppConfig.PRIMARY_COLOR};
                             font-size:1.8rem;
                             font-weight:800;">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

    # ------------------------------------------------------------------ #
    #  Timelines                                                           #
    # ------------------------------------------------------------------ #

    def _render_timeline_section(self):
        """Render monthly and daily timeline charts with real data."""
        self._render_section_label("📅 Timelines")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Timelines reveal the <b style="color:#25D366;">growth and activity patterns</b> of your chat over time.<br>
            • <b style="color:#25D366;">Monthly Timeline</b> — Identifies peak months of activity.
            e.g. A spike in December could mean holiday planning or celebrations happening in the group.<br>
            • <b style="color:#25D366;">Daily Timeline</b> — Shows consistency of chat activity.
            Flat lines = steady engagement. Sharp spikes = specific events or incidents triggered heavy discussion.
        """)
        col1, col2 = st.columns(2)

        with col1:
            monthly = self.analyzer.monthly_timeline(self.selected_user)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=monthly["time"],
                y=monthly["messages"],
                mode="lines+markers",
                line=dict(color=AppConfig.PRIMARY_COLOR, width=2),
                marker=dict(size=6),
                fill="tozeroy",
                fillcolor="rgba(37,211,102,0.1)"
            ))
            fig = self._apply_chart_style(fig, "📆 Monthly Timeline")
            st.plotly_chart(fig, width='stretch')

        with col2:
            daily = self.analyzer.daily_timeline(self.selected_user)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily["date"],
                y=daily["messages"],
                mode="lines",
                line=dict(color=AppConfig.SECONDARY_COLOR, width=1.5),
                fill="tozeroy",
                fillcolor="rgba(18,140,126,0.1)"
            ))
            fig = self._apply_chart_style(fig, "📅 Daily Timeline")
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------ #
    #  Activity Map                                                        #
    # ------------------------------------------------------------------ #

    def _render_activity_section(self):
        """Render activity map charts with real data."""
        self._render_section_label("🗺️ Activity Map")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Activity maps reveal <b style="color:#25D366;">when</b> people are most active — helping you understand behavior patterns.<br>
            • <b style="color:#25D366;">Busiest Day</b> — Tells you which day of the week drives the most conversation.
            e.g. If Sunday is busiest it means the group is more active on weekends — social in nature.<br>
            • <b style="color:#25D366;">Busiest Month</b> — Seasonal trends in the chat.
            e.g. Low activity in exam months, high in vacation months.<br>
            • <b style="color:#25D366;">Activity Heatmap</b> — The most powerful view. Shows exact hour + day combinations of peak activity.
            e.g. High intensity at 10PM on weekdays = night owl group that chats after work/college.
        """)
        col1, col2 = st.columns(2)

        with col1:
            day_counts = self.analyzer.busiest_day(self.selected_user)
            fig = go.Figure(go.Bar(
                x=day_counts.index,
                y=day_counts.values,
                marker_color=AppConfig.PRIMARY_COLOR
            ))
            fig = self._apply_chart_style(fig, "📊 Busiest Day")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            month_counts = self.analyzer.busiest_month(self.selected_user)
            fig = go.Figure(go.Bar(
                x=month_counts.index,
                y=month_counts.values,
                marker_color=AppConfig.SECONDARY_COLOR
            ))
            fig = self._apply_chart_style(fig, "📊 Busiest Month")
            st.plotly_chart(fig, use_container_width=True)

        # Heatmap full width
        heatmap_data = self.analyzer.activity_heatmap(self.selected_user)
        fig = go.Figure(go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns.astype(str),
            y=heatmap_data.index,
            colorscale=AppConfig.HEATMAP_COLORSCALE,
        ))
        fig = self._apply_chart_style(
            fig, "🔥 Activity Heatmap — Hour vs Day"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------ #
    #  Busy Users                                                          #
    # ------------------------------------------------------------------ #

    def _render_busy_users_section(self):
        """Render most busy users section."""
        self._render_section_label("👥 Most Active Users")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Identifies the <b style="color:#25D366;">dominant voices</b> in the conversation and contribution balance.<br>
            • <b style="color:#25D366;">Message Count</b> — Who drives the most conversation?
            e.g. If one person sends 60% of messages they are the group's primary initiator and conversation driver.<br>
            • <b style="color:#25D366;">Contribution %</b> — Is the chat balanced or one-sided?
            A healthy group chat has relatively balanced contributions. Heavy imbalance may indicate passive members.
        """)

        counts, percent_df = self.analyzer.most_busy_users()

        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure(go.Bar(
                x=counts.index,
                y=counts.values,
                marker_color=[
                    AppConfig.PRIMARY_COLOR,
                    AppConfig.SECONDARY_COLOR,
                    AppConfig.PURPLE_COLOR,
                    AppConfig.NEUTRAL_COLOR,
                ][:len(counts)]
            ))
            fig = self._apply_chart_style(fig, "💬 Message Count")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = go.Figure(go.Pie(
                labels=percent_df["username"],
                values=percent_df["messages"],
                hole=0.4,
                marker=dict(colors=[
                    AppConfig.PRIMARY_COLOR,
                    AppConfig.SECONDARY_COLOR,
                    AppConfig.PURPLE_COLOR,
                    AppConfig.NEUTRAL_COLOR,
                ][:len(percent_df)])
            ))
            fig = self._apply_chart_style(
                fig, "🥧 Contribution %"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------ #
    #  Word Analysis                                                       #
    # ------------------------------------------------------------------ #

    def _render_wordcloud_section(self):
        """Render WordCloud and most common words with real data."""
        self._render_section_label("💬 Word Analysis")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Word analysis uncovers the <b style="color:#25D366;">topics, themes and vocabulary</b> that define this chat.<br>
            • <b style="color:#25D366;">Word Cloud</b> — Bigger the word = more frequently used.
            Instantly reveals the dominant topics and recurring themes in the conversation without reading every message.<br>
            • <b style="color:#25D366;">Top 20 Words</b> — Precise frequency count of the most used vocabulary.
            e.g. If "plan", "kab", "kaha" dominate = group is mostly used for planning meetups and outings.
        """)
        col1, col2 = st.columns(2)

        with col1:
            import matplotlib.pyplot as plt
            wc = self.analyzer.generate_wordcloud(self.selected_user)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            fig.patch.set_facecolor(AppConfig.PLOT_BG)
            ax.set_facecolor(AppConfig.PLOT_BG)
            st.markdown(
                f"<p style='color:{AppConfig.TEXT_SECONDARY};"
                f"font-size:0.85rem; text-align:center;'>"
                f"☁️ Word Cloud</p>",
                unsafe_allow_html=True
            )
            st.pyplot(fig)
            plt.close()

        with col2:
            common = self.analyzer.most_common_words(
                self.selected_user, top_n=20
            )
            fig = go.Figure(go.Bar(
                x=common["count"],
                y=common["word"],
                orientation="h",
                marker_color=AppConfig.PRIMARY_COLOR
            ))
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig = self._apply_chart_style(
                fig, "📊 Top 20 Most Common Words"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------ #
    #  Emoji Analysis                                                      #
    # ------------------------------------------------------------------ #

    def _render_emoji_section(self):
        """Render emoji analysis with real data."""
        self._render_section_label("😂 Emoji Analysis")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Emojis are the <b style="color:#25D366;">emotional language</b> of WhatsApp — they reveal tone and group culture.<br>
            • <b style="color:#25D366;">Emoji Frequency</b> — Which emojis dominate the chat?
            e.g. Heavy 😂 usage = fun and humorous group. Heavy ❤️ usage = emotionally close and supportive group.<br>
            • <b style="color:#25D366;">Emoji Distribution</b> — Are a few emojis dominant or is usage diverse?
            A diverse emoji palette indicates expressive communicators while a narrow palette suggests habitual usage.
        """)

        emoji_df = self.analyzer.emoji_analysis(self.selected_user)

        if emoji_df.empty:
            self._render_empty_state("No emojis found in this chat")
            return

        col1, col2 = st.columns(2)

        with col1:
            top_10 = emoji_df.head(10)
            fig = go.Figure(go.Bar(
                x=top_10["frequency"],
                y=top_10["emoji"],
                orientation="h",
                marker_color=AppConfig.PRIMARY_COLOR
            ))
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig = self._apply_chart_style(
                fig, "😂 Top 10 Emoji Frequency"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_5 = emoji_df.head(5)
            fig = go.Figure(go.Pie(
                labels=top_5["emoji"],
                values=top_5["frequency"],
                hole=0.4,
                marker=dict(colors=[
                    AppConfig.PRIMARY_COLOR,
                    AppConfig.SECONDARY_COLOR,
                    AppConfig.NEUTRAL_COLOR,
                    AppConfig.PURPLE_COLOR,
                    AppConfig.NEGATIVE_COLOR,
                ])
            ))
            fig = self._apply_chart_style(
                fig, "🥧 Top 5 Emoji Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------ #
    #  Response Time                                                       #
    # ------------------------------------------------------------------ #

    def _render_response_time_section(self):
        """Render response time and conversation starter analysis."""
        self._render_section_label("⚡ Response Analysis")
        self._render_section_description("""
            <b style="color:#FFFFFF;">What this tells you:</b>
            Response patterns reveal <b style="color:#25D366;">engagement quality and communication dynamics</b> between members.<br>
            • <b style="color:#25D366;">Avg Response Time</b> — How quickly does each person reply?
            e.g. A person with 2 min avg response time is highly engaged. 60+ min avg suggests they check the chat occasionally.<br>
            • <b style="color:#25D366;">Conversation Starters</b> — Who initiates discussions most often?
            The person who starts conversations most is the group's <b style="color:#25D366;">social anchor</b> — 
            they keep the group alive and drive engagement.
        """)

        col1, col2 = st.columns(2)

        with col1:
            response_df = self.analyzer.response_time_analysis()
            fig = go.Figure(go.Bar(
                x=response_df["username"],
                y=response_df["avg_response_minutes"],
                marker_color=AppConfig.SECONDARY_COLOR
            ))
            fig = self._apply_chart_style(
                fig, "⚡ Avg Response Time (minutes)"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            starters_df = self.analyzer.conversation_starters()
            fig = go.Figure(go.Bar(
                x=starters_df["username"],
                y=starters_df["conversations_started"],
                marker_color=AppConfig.PURPLE_COLOR
            ))
            fig = self._apply_chart_style(
                fig, "🗣️ Conversation Starters"
            )
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _apply_chart_style(
        self, fig: go.Figure, title: str
    ) -> go.Figure:
        """
        Apply consistent dark theme styling to all charts.

        :param fig: Plotly figure object
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
            xaxis=dict(
                gridcolor=AppConfig.GRIDLINE_COLOR,
                showgrid=True
            ),
            yaxis=dict(
                gridcolor=AppConfig.GRIDLINE_COLOR,
                showgrid=True
            ),
        )
        return fig

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


    def _render_section_label(self, label: str):
        """
        Render a styled section label.

        :param label: Label text
        """
        st.markdown(
            f"<p style='color:{AppConfig.TEXT_SECONDARY};"
            f"font-size:0.85rem; text-transform:uppercase;"
            f"letter-spacing:1px;'>{label}</p>",
            unsafe_allow_html=True
        )

    def _render_empty_state(self, message: str):
        """
        Render empty state card.

        :param message: Message to display
        """
        st.markdown(f"""
            <div style="
                background:{AppConfig.CARD_BACKGROUND};
                border:1px solid {AppConfig.BORDER_COLOR};
                border-radius:12px; padding:30px;
                text-align:center;
            ">
                <div style="color:{AppConfig.TEXT_SECONDARY};
                            font-size:0.9rem;">{message}</div>
            </div>
        """, unsafe_allow_html=True)