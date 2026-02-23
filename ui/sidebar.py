# =============================================================================
# sidebar.py — Sidebar UI Component
# Handles API key input, file upload, user selection and feature navigation
# =============================================================================

import streamlit as st
from config.settings import AppConfig


class Sidebar:
    """
    Manages the entire sidebar UI.
    Responsible for API key input, file upload,
    user selector and feature navigation.
    """

    def __init__(self):
        """Initialize sidebar state variables."""
        self._init_session_state()

    def _init_session_state(self):
        """Initialize all required session state variables."""
        defaults = {
            AppConfig.SESSION_API_KEY:        None,
            AppConfig.SESSION_SELECTED_MODEL: None,
            AppConfig.SESSION_MODEL_INFO:     None,
            AppConfig.SESSION_RPM_USED:       0,
            AppConfig.SESSION_RPD_USED:       0,
            AppConfig.SESSION_ANALYTICS_VIEWED: False,
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def render(self) -> dict:
        """
        Main render method — builds the complete sidebar.
        Returns dict of all user selections.

        :return: Dictionary of sidebar selections
        """
        self._render_logo()
        self._render_divider()
        self._render_api_section()
        self._render_divider()
        uploaded_file = self._render_upload_section()
        selected_user = None
        analyze_clicked = False

        if uploaded_file is not None:
            self._render_divider()
            selected_user, analyze_clicked = self._render_user_section()

        self._render_divider()
        feature = self._render_feature_selector()
        self._render_divider()
        self._render_footer()

        return {
            "uploaded_file":   uploaded_file,
            "selected_user":   selected_user,
            "analyze_clicked": analyze_clicked,
            "selected_feature": feature,
        }

    # ------------------------------------------------------------------ #
    #  Logo                                                                #
    # ------------------------------------------------------------------ #

    def _render_logo(self):
        """Render sidebar logo and app name."""
        st.sidebar.markdown(f"""
            <div style="text-align:center; padding:10px 0 10px 0;">
                <h2 style="color:{AppConfig.PRIMARY_COLOR};
                           font-size:1.4rem; font-weight:800;">
                    💬 WhatsApp Analyzer
                </h2>
                <p style="color:{AppConfig.TEXT_SECONDARY};
                          font-size:0.75rem; margin:0;">
                    Turn chats into insights
                </p>
            </div>
        """, unsafe_allow_html=True)

    # ------------------------------------------------------------------ #
    #  API Key Section                                                     #
    # ------------------------------------------------------------------ #

    def _render_api_section(self):
        """
        Render Gemini API key input and model selector.
        Fetches available models dynamically using the key.
        """
        self._render_section_label("🔑 Gemini API Key")

        api_key = st.sidebar.text_input(
            label="Enter your Gemini API key",
            type="password",
            placeholder="AIza...",
            help="Get your free key at aistudio.google.com",
            label_visibility="collapsed"
        )

        if api_key:
            # Save key to session state
            st.session_state[AppConfig.SESSION_API_KEY] = api_key

            # Fetch models if not already fetched
            # or if key changed
            if st.session_state[AppConfig.SESSION_MODEL_INFO] is None:
                with st.sidebar.spinner("Fetching models..."):
                    models = self._fetch_models(api_key)
                    st.session_state[AppConfig.SESSION_MODEL_INFO] = models

            models = st.session_state[AppConfig.SESSION_MODEL_INFO]

            if models:
                self._render_section_label("🤖 Select Model")

                model_displays = [m["display"] for m in models]
                selected_display = st.sidebar.selectbox(
                    label="Select Gemini model",
                    options=model_displays,
                    label_visibility="collapsed",
                    help="Higher RPM = more messages per minute allowed"
                )

                # Save selected model to session state
                selected_model = next(
                    m for m in models
                    if m["display"] == selected_display
                )
                st.session_state[AppConfig.SESSION_SELECTED_MODEL] = (
                    selected_model
                )

                # Show rate limits for selected model
                rpm = selected_model.get("rpm", "?")
                rpd = selected_model.get("rpd", "?")

                st.sidebar.markdown(f"""
                    <div style="background:{AppConfig.CARD_BACKGROUND};
                                border:1px solid {AppConfig.BORDER_COLOR};
                                border-radius:8px; padding:10px 12px;
                                margin-top:8px; font-size:0.78rem;">
                        <span style="color:{AppConfig.TEXT_SECONDARY};">
                            Limits:
                        </span>
                        <span style="color:{AppConfig.PRIMARY_COLOR};
                                     font-weight:700;">
                            {rpm} RPM
                        </span>
                        <span style="color:{AppConfig.TEXT_SECONDARY};">
                            &nbsp;|&nbsp;
                        </span>
                        <span style="color:{AppConfig.PRIMARY_COLOR};
                                     font-weight:700;">
                            {rpd} RPD
                        </span>
                    </div>
                """, unsafe_allow_html=True)

            else:
                st.sidebar.error("❌ Invalid API key or no models found")
                st.session_state[AppConfig.SESSION_API_KEY]    = None
                st.session_state[AppConfig.SESSION_MODEL_INFO] = None
        else:
            st.session_state[AppConfig.SESSION_API_KEY]    = None
            st.session_state[AppConfig.SESSION_MODEL_INFO] = None
            st.sidebar.caption(
                "🔒 Required for AI Agent feature only"
            )

    def _fetch_models(self, api_key: str) -> list:
        """
        Fetch available Gemini models using the Agent class.

        :param api_key: Gemini API key
        :return: List of model info dicts
        """
        try:
            from core.agent import Agent
            import pandas as pd

            # Create minimal dummy df just to init Agent
            dummy_df = pd.DataFrame([{
                "datetime":  pd.Timestamp.now(),
                "date":      pd.Timestamp.now().date(),
                "year":      2025,
                "month":     "January",
                "month_num": 1,
                "day":       "Monday",
                "day_num":   0,
                "hour":      12,
                "minute":    0,
                "username":  "User",
                "message":   "Hello",
                "is_media":  False,
                "word_count": 1,
                "has_link":  False,
            }])

            agent  = Agent(api_key=api_key, df=dummy_df)
            models = agent.get_available_models()
            return models

        except Exception:
            return []

    # ------------------------------------------------------------------ #
    #  Upload Section                                                      #
    # ------------------------------------------------------------------ #

    def _render_upload_section(self):
        """
        Render file upload widget.

        :return: Uploaded file object or None
        """
        self._render_section_label("📂 Upload Chat")

        uploaded_file = st.sidebar.file_uploader(
            label="Export your WhatsApp chat (.txt)",
            type=["txt"],
            help="WhatsApp → Chat → Export Chat → Without Media",
            label_visibility="collapsed"
        )

        return uploaded_file

    # ------------------------------------------------------------------ #
    #  User Section                                                        #
    # ------------------------------------------------------------------ #

    def _render_user_section(self) -> tuple:
        """
        Render user selector and analyze button.
        Only shown after file is uploaded.

        :return: Tuple of (selected_user, analyze_clicked)
        """
        self._render_section_label("👤 Select User")

        # Get users from session state if available
        users = ["Overall"]
        preprocessor = st.session_state.get(AppConfig.SESSION_PREPROCESSOR)
        if preprocessor is not None:
            try:
                users = preprocessor.get_users()
            except Exception:
                users = ["Overall"]

        selected_user = st.sidebar.selectbox(
            label="Analyze chat for",
            options=users,
            help="Select a specific user or Overall",
            label_visibility="collapsed"
        )

        st.sidebar.markdown("<br>", unsafe_allow_html=True)

        analyze_clicked = st.sidebar.button(
        "🔍 Analyze Chat",
        use_container_width=True,
        type="primary"
    )

        return selected_user, analyze_clicked

    # ------------------------------------------------------------------ #
    #  Feature Selector                                                    #
    # ------------------------------------------------------------------ #

    def _render_feature_selector(self):
        """
        Render feature navigation radio buttons.
        Agent is locked until analytics is viewed.

        :return: Selected feature string
        """
        self._render_section_label("🧭 Navigate")

        analytics_viewed = st.session_state.get(
            AppConfig.SESSION_ANALYTICS_VIEWED, False
        )

        # Lock agent if analytics not viewed yet
        options = [
            AppConfig.FEATURE_ANALYTICS,
            AppConfig.FEATURE_SENTIMENT,
            AppConfig.FEATURE_AGENT if analytics_viewed
            else "🔒 AI Chat Agent (View Analytics First)"
        ]

        feature = st.sidebar.radio(
            label="Navigate to",
            options=options,
            index=0,
            label_visibility="collapsed"
        )

        return feature

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _render_section_label(self, label: str):
        """
        Render a styled section label in the sidebar.

        :param label: Label text
        """
        st.sidebar.markdown(
            f"<p style='color:{AppConfig.PRIMARY_COLOR}; "
            f"font-weight:600; font-size:0.82rem; "
            f"text-transform:uppercase; letter-spacing:1px; "
            f"margin:10px 0 6px 0;'>{label}</p>",
            unsafe_allow_html=True
        )

    def _render_divider(self):
        """Render a styled divider line."""
        st.sidebar.markdown(
            f"<hr style='border:1px solid {AppConfig.BORDER_COLOR};"
            f"margin:12px 0;'>",
            unsafe_allow_html=True
        )

    def _render_footer(self):
        """Render sidebar footer."""
        st.sidebar.markdown(f"""
            <div style="text-align:center;
                        color:{AppConfig.TEXT_SECONDARY};
                        font-size:0.72rem; padding-bottom:10px;">
                Built with ❤️ using Streamlit<br>
                <span style="color:{AppConfig.PRIMARY_COLOR};">
                    v{AppConfig.APP_VERSION}
                </span>
            </div>
        """, unsafe_allow_html=True)