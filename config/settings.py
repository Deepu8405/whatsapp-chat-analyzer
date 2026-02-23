# =============================================================================
# settings.py — App-wide constants and configuration
# All magic numbers, strings, and config values live here
# =============================================================================


class AppConfig:
    """Central configuration class for the entire application."""

    # ------------------------------------------------------------------ #
    #  App Meta                                                            #
    # ------------------------------------------------------------------ #
    APP_TITLE          = "WhatsApp Analyzer Pro"
    APP_ICON           = "💬"
    APP_LAYOUT         = "wide"
    APP_INITIAL_SIDEBAR = "expanded"
    APP_VERSION        = "1.0.0"

    # ------------------------------------------------------------------ #
    #  Theme Colors                                                        #
    # ------------------------------------------------------------------ #
    PRIMARY_COLOR      = "#25D366"   # WhatsApp green
    SECONDARY_COLOR    = "#128C7E"   # WhatsApp dark green
    BACKGROUND_DARK    = "#0D1117"   # Dark background
    CARD_BACKGROUND    = "#161B22"   # Card background
    BORDER_COLOR       = "#21262D"   # Border color
    TEXT_PRIMARY       = "#FFFFFF"   # Primary text
    TEXT_SECONDARY     = "#8B949E"   # Secondary/muted text
    POSITIVE_COLOR     = "#25D366"   # Sentiment positive
    NEGATIVE_COLOR     = "#FF4B4B"   # Sentiment negative
    NEUTRAL_COLOR      = "#FFA500"   # Sentiment neutral
    PURPLE_COLOR       = "#7B68EE"   # Accent purple
    CHAT_USER_BG       = "#005C4B"   # User chat bubble
    CHAT_AGENT_BG      = "#161B22"   # Agent chat bubble

    # ------------------------------------------------------------------ #
    #  Chart Settings                                                      #
    # ------------------------------------------------------------------ #
    CHART_HEIGHT       = 400
    CHART_BG           = "#161B22"
    PLOT_BG            = "#0D1117"
    GRIDLINE_COLOR     = "#21262D"
    HEATMAP_COLORSCALE = [
        [0.0,  "#0D1117"],
        [0.5,  "#128C7E"],
        [1.0,  "#25D366"],
    ]

    # ------------------------------------------------------------------ #
    #  Agent Settings                                                      #
    # ------------------------------------------------------------------ #
    AGENT_MAX_TOKENS   = 150
    AGENT_TEMPERATURE  = 0.85
    DEFAULT_MODEL      = "gemini-2.5-flash-lite"

    # ------------------------------------------------------------------ #
    #  Rate Limit Warning Thresholds                                       #
    # ------------------------------------------------------------------ #
    WARN_THRESHOLD     = 0.80   # Warn at 80% usage
    CRITICAL_THRESHOLD = 0.95   # Critical at 95% usage

    # ------------------------------------------------------------------ #
    #  Session State Keys                                                  #
    # ------------------------------------------------------------------ #
    SESSION_DF              = "df"
    SESSION_PREPROCESSOR    = "preprocessor"
    SESSION_ANALYZER        = "analyzer"
    SESSION_SENTIMENT       = "sentiment"
    SESSION_AGENT           = "agent"
    SESSION_API_KEY         = "api_key"
    SESSION_SELECTED_MODEL  = "selected_model"
    SESSION_MODEL_INFO      = "model_info"
    SESSION_RPM_USED        = "rpm_used"
    SESSION_RPD_USED        = "rpd_used"
    SESSION_ANALYTICS_VIEWED = "analytics_viewed"
    SESSION_CHAT_HISTORY    = "chat_history"
    SESSION_AGENT_ROLE      = "agent_role"

    # ------------------------------------------------------------------ #
    #  Empty State Messages                                                #
    # ------------------------------------------------------------------ #
    EMPTY_STATE_TITLE   = "No Data Yet"
    EMPTY_STATE_UPLOAD  = "Please upload a WhatsApp chat file to see insights"
    EMPTY_STATE_ANALYZE = "Click 'Analyze Chat' in the sidebar to load data"
    EMPTY_STATE_AGENT   = "View Analytics first to unlock the AI Agent"

    # ------------------------------------------------------------------ #
    #  Feature Navigation Labels                                           #
    # ------------------------------------------------------------------ #
    FEATURE_ANALYTICS  = "📊 Analytics Dashboard"
    FEATURE_SENTIMENT  = "🧠 Sentiment Analysis"
    FEATURE_AGENT      = "🤖 AI Chat Agent"