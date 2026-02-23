# =============================================================================
# app.py — Main Streamlit Entry Point
# Orchestrates all UI components and manages session state
# No business logic here — only coordination
# =============================================================================

import streamlit as st
from config.settings import AppConfig
from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.sentiment_ui import SentimentUI
from ui.agent_ui import AgentUI
import streamlit.components.v1 as components

# ------------------------------------------------------------------ #
#  App Initialization                                                  #
# ------------------------------------------------------------------ #

def initialize_app():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title=AppConfig.APP_TITLE,
        page_icon=AppConfig.APP_ICON,
        layout=AppConfig.APP_LAYOUT,
        initial_sidebar_state=AppConfig.APP_INITIAL_SIDEBAR
    )


def load_css():
    """Load custom CSS from assets folder."""
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# ------------------------------------------------------------------ #
#  Session State                                                       #
# ------------------------------------------------------------------ #

def init_session_state():
    """Initialize all app level session state variables."""
    defaults = {
        AppConfig.SESSION_DF:               None,
        AppConfig.SESSION_PREPROCESSOR:     None,
        AppConfig.SESSION_ANALYZER:         None,
        AppConfig.SESSION_SENTIMENT:        None,
        AppConfig.SESSION_AGENT:            None,
        AppConfig.SESSION_ANALYTICS_VIEWED: False,
        AppConfig.SESSION_CHAT_HISTORY:     [],
        AppConfig.SESSION_AGENT_ROLE:       None,
        AppConfig.SESSION_RPM_USED:         0,
        AppConfig.SESSION_RPD_USED:         0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ------------------------------------------------------------------ #
#  Data Processing                                                     #
# ------------------------------------------------------------------ #

def process_uploaded_file(uploaded_file):
    """
    Process uploaded WhatsApp chat file through
    Preprocessor, Analyzer and Sentiment classes.
    Results stored in session state.

    :param uploaded_file: Streamlit uploaded file object
    """
    from core.preprocessor import Preprocessor
    from core.analyzer import Analyzer
    from core.sentiment import Sentiment

    with st.spinner("⏳ Processing chat file..."):
        try:
            # Step 1: Read raw text
            raw_text = uploaded_file.getvalue().decode("utf-8")

            # Step 2: Preprocess
            preprocessor = Preprocessor()
            df = preprocessor.load(raw_text).process()

            # Step 3: Analyze
            analyzer = Analyzer(df)

            # Step 4: Sentiment
            sentiment = Sentiment(df)

            # Step 5: Get sentiment scored df
            scored_df = sentiment.get_scored_df()

            # Step 6: Store everything in session state
            st.session_state[AppConfig.SESSION_DF]           = scored_df
            st.session_state[AppConfig.SESSION_PREPROCESSOR] = preprocessor
            st.session_state[AppConfig.SESSION_ANALYZER]     = analyzer
            st.session_state[AppConfig.SESSION_SENTIMENT]    = sentiment

            # Reset agent when new file uploaded
            st.session_state[AppConfig.SESSION_AGENT]            = None
            st.session_state[AppConfig.SESSION_ANALYTICS_VIEWED] = False
            st.session_state[AppConfig.SESSION_CHAT_HISTORY]     = []

            st.success("✅ Chat analyzed successfully!")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")


def initialize_agent():
    """
    Initialize the AI Agent with API key and scored DataFrame.
    Only called when user navigates to Agent section.
    """
    from core.agent import Agent

    api_key = st.session_state.get(AppConfig.SESSION_API_KEY)
    df      = st.session_state.get(AppConfig.SESSION_DF)

    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar.")
        return False

    if df is None:
        st.warning("⚠️ Please upload and analyze a chat file first.")
        return False

    if st.session_state[AppConfig.SESSION_AGENT] is None:
        with st.spinner("🤖 Initializing AI Agent..."):
            try:
                agent = Agent(api_key=api_key, df=df)
                st.session_state[AppConfig.SESSION_AGENT] = agent
            except Exception as e:
                st.error(f"❌ Agent initialization failed: {str(e)}")
                return False

    return True


# ------------------------------------------------------------------ #
#  Floating Top Bar                                                    #
# ------------------------------------------------------------------ #

def render_floating_bar():
    """
    Render fixed floating bar at top of page showing
    selected model, RPM and RPD usage counters.
    Uses st.markdown with unsafe_allow_html only.
    """
    model_name = "No model selected"
    rpm_limit  = 0
    rpd_limit  = 0
    rpm_used   = st.session_state.get(AppConfig.SESSION_RPM_USED, 0)
    rpd_used   = st.session_state.get(AppConfig.SESSION_RPD_USED, 0)

    selected_model = st.session_state.get(AppConfig.SESSION_SELECTED_MODEL)
    if selected_model:
        model_name = selected_model.get("name", "Unknown")
        rpm_limit  = selected_model.get("rpm", 0)
        rpd_limit  = selected_model.get("rpd", 0)

    # Calculate usage percentages
    rpm_pct = (rpm_used / rpm_limit * 100) if rpm_limit > 0 else 0
    rpd_pct = (rpd_used / rpd_limit * 100) if rpd_limit > 0 else 0

    def get_color(pct):
        if pct >= AppConfig.CRITICAL_THRESHOLD * 100:
            return AppConfig.NEGATIVE_COLOR
        elif pct >= AppConfig.WARN_THRESHOLD * 100:
            return AppConfig.NEUTRAL_COLOR
        return AppConfig.PRIMARY_COLOR

    rpm_color = get_color(rpm_pct)
    rpd_color = get_color(rpd_pct)

    warning = ""
    if rpd_pct >= AppConfig.CRITICAL_THRESHOLD * 100:
        warning = "🔴 Daily limit almost reached!"
    elif rpd_pct >= AppConfig.WARN_THRESHOLD * 100:
        warning = "🟡 80% of daily limit used"

    st.markdown(
        f"""
        <div id="floating-bar">
            <span class="bar-item">
                🤖 Model: <b style="color:{AppConfig.PRIMARY_COLOR}">{model_name}</b>
            </span>
            <span class="bar-item">
                ⚡ RPM: <b style="color:{rpm_color}">{rpm_used}/{rpm_limit}</b>
            </span>
            <span class="bar-item">
                📅 RPD: <b style="color:{rpd_color}">{rpd_used}/{rpd_limit}</b>
            </span>
            {"<span style='color:" + get_color(rpd_pct) + ";font-weight:700;'>" + warning + "</span>" if warning else ""}
        </div>
        <div style="height:40px;"></div>
        """,
        unsafe_allow_html=True
    )
# ------------------------------------------------------------------ #
#  Empty State                                                         #
# ------------------------------------------------------------------ #

def render_home():
    """Render hero landing page before file is uploaded."""
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">💬 WhatsApp Analyzer Pro</h1>
            <p style="font-size:1.1rem; color:#8B949E; max-width:600px;
                      margin:0 auto 40px auto; line-height:1.7;
                      text-align:center; display:block;">
                Upload your WhatsApp chat export to unlock deep insights,
                sentiment analysis, and an AI agent that chats like
                your contacts.
            </p>
            <div class="feature-grid">
                <div class="feature-card">
                    📊 <b>Deep Analytics</b><br>
                    Messages, timelines, activity maps
                </div>
                <div class="feature-card">
                    🧠 <b>Sentiment Analysis</b><br>
                    Mood tracking per user over time
                </div>
                <div class="feature-card">
                    🤖 <b>AI Chat Agent</b><br>
                    LLM that mimics your contact's style
                </div>
                <div class="feature-card">
                    😂 <b>Emoji & Word Stats</b><br>
                    Most used words, emojis & more
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_empty_state(message: str, icon: str = "📭"):
    """
    Render a clean empty state card with message.

    :param message: Message to display
    :param icon: Emoji icon to show
    """
    st.markdown(f"""
        <div style="
            background:{AppConfig.CARD_BACKGROUND};
            border:1px solid {AppConfig.BORDER_COLOR};
            border-radius:12px;
            padding:60px 20px;
            text-align:center;
            margin-top:40px;
        ">
            <div style="font-size:3rem;">{icon}</div>
            <div style="color:{AppConfig.PRIMARY_COLOR};
                        font-size:1.1rem; font-weight:700;
                        margin:16px 0 8px 0;">
                {AppConfig.EMPTY_STATE_TITLE}
            </div>
            <div style="color:{AppConfig.TEXT_SECONDARY};
                        font-size:0.9rem;">
                {message}
            </div>
        </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  Main                                                                #
# ------------------------------------------------------------------ #

def main():
    """
    Main app entry point.
    Orchestrates all components and manages app flow.
    """
    # Step 1: Initialize
    initialize_app()
    init_session_state()
    load_css()
    # Step 2: Load custom CSS
    load_css()

    # Step 3: Render top navigation
    render_top_nav()

    # Step 4: Render floating top bar
    render_floating_bar()

    # Step 5: Render sidebar
    sidebar    = Sidebar()
    selections = sidebar.render()

    uploaded_file   = selections["uploaded_file"]
    selected_user   = selections["selected_user"]
    analyze_clicked = selections["analyze_clicked"]
    feature         = selections["selected_feature"]

    # Step 6: Process file when analyze clicked
    if analyze_clicked and uploaded_file is not None:
        process_uploaded_file(uploaded_file)

    # Step 7: Render main content
    df = st.session_state.get(AppConfig.SESSION_DF)

    # No file uploaded yet — show home
    if uploaded_file is None:
        render_home()
        return

    # File uploaded but not analyzed yet
    if df is None:
        render_empty_state(
            AppConfig.EMPTY_STATE_ANALYZE,
            "🔍"
        )
        return

    # Step 8: Route to correct feature
    analyzer  = st.session_state.get(AppConfig.SESSION_ANALYZER)
    sentiment = st.session_state.get(AppConfig.SESSION_SENTIMENT)

    with st.spinner("Loading..."):

        if AppConfig.FEATURE_ANALYTICS in feature:
            # Mark analytics as viewed to unlock agent
            st.session_state[AppConfig.SESSION_ANALYTICS_VIEWED] = True
            dashboard = Dashboard(
                selected_user=selected_user,
                analyzer=analyzer
            )
            dashboard.render()

        elif AppConfig.FEATURE_SENTIMENT in feature:
            sentiment_ui = SentimentUI(
                selected_user=selected_user,
                sentiment=sentiment
            )
            sentiment_ui.render()

        elif "Agent" in feature:
            # Check if analytics viewed
            if not st.session_state.get(
                AppConfig.SESSION_ANALYTICS_VIEWED, False
            ):
                render_empty_state(
                    AppConfig.EMPTY_STATE_AGENT, "🔒"
                )
                return

            # Initialize agent if needed
            if not initialize_agent():
                return

            agent_ui = AgentUI(
                selected_user=selected_user,
                agent=st.session_state[AppConfig.SESSION_AGENT]
            )
            agent_ui.render()

def render_top_nav():
    """Render top navigation bar using Streamlit native components."""
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown(
            "<h3 style='color:#25D366; margin:0; padding:4px 0;'>"
            "💬 WhatsApp Analyzer Pro</h3>",
            unsafe_allow_html=True
        )

    with col2:
        st.link_button("📖 How To Use", "/How_To_Use", use_container_width=True)

    with col3:
        st.link_button(
            "🌐 Contact Me",
            "https://whimsical-conkies-ad5d60.netlify.app/",
            use_container_width=True
        )

    st.markdown(
        "<hr style='border:1px solid #21262D; margin:4px 0 16px 0;'>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()