# =============================================================================
# agent_ui.py — AI Chat Agent UI Component
# Renders chat agent interface with real Gemini LLM responses
# =============================================================================

import streamlit as st
from config.settings import AppConfig
from core.agent import Agent


class AgentUI:
    """
    Manages the entire AI Chat Agent UI.
    Receives real Agent instance for LLM responses.
    """

    def __init__(self, selected_user: str, agent: Agent):
        """
        Initialize AgentUI with selected user and Agent instance.

        :param selected_user: User selected from sidebar
        :param agent: Agent instance with extracted patterns
        """
        self.selected_user = selected_user
        self.agent         = agent
        self._init_session_state()

    def _init_session_state(self):
        """Initialize agent related session state variables."""
        if AppConfig.SESSION_CHAT_HISTORY not in st.session_state:
            st.session_state[AppConfig.SESSION_CHAT_HISTORY] = []
        if AppConfig.SESSION_AGENT_ROLE not in st.session_state:
            st.session_state[AppConfig.SESSION_AGENT_ROLE] = None
        if "agent_session_active" not in st.session_state:
            st.session_state["agent_session_active"] = False
        if "agent_rpm_this_minute" not in st.session_state:
            st.session_state["agent_rpm_this_minute"] = 0
        if "input_key" not in st.session_state:
            st.session_state["input_key"] = 0

    def render(self):
        """Main render method — builds complete agent UI."""
        self._render_header()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_personality_cards()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_role_selector()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_chat_window()

    # ------------------------------------------------------------------ #
    #  Header                                                              #
    # ------------------------------------------------------------------ #

    def _render_header(self):
        """Render agent page header."""
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(
                f"<h2 style='color:{AppConfig.PRIMARY_COLOR};"
                f"margin-bottom:0;'>🤖 AI Chat Agent</h2>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='color:{AppConfig.TEXT_SECONDARY};"
                f"font-size:0.88rem;'>"
                f"An AI that learns from the chat and replies "
                f"just like your contact.</p>",
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
    #  Personality Cards                                                   #
    # ------------------------------------------------------------------ #

    def _render_personality_cards(self):
        """
        Render personality trait cards for selected role user.
        Shows real extracted patterns from Agent class.
        """
        self._render_section_label("🎭 Agent Personality Card")

        role = st.session_state.get(AppConfig.SESSION_AGENT_ROLE)

        if not role or role == "Select a person...":
            self._render_empty_state(
                "Select a person below to see their personality profile"
            )
            return

        try:
            pattern = self.agent.get_pattern(role)
        except Exception:
            self._render_empty_state("Pattern not found for this user")
            return

        col1, col2, col3, col4, col5 = st.columns(5)

        top_emoji = pattern["top_emojis"][0] if pattern["top_emojis"] else "😊"
        top_word  = pattern["top_words"][0]  if pattern["top_words"]  else "—"

        traits = [
            ("💬", "Avg Words/Msg", str(pattern["avg_words_per_msg"])),
            ("😂", "Top Emoji",     top_emoji),
            ("🎭", "Tone",          pattern["tone"].split("/")[0]),
            ("⏰", "Active Hour",   f"{pattern['most_active_hour']}:00"),
            ("🧠", "Mood Score",    f"{pattern['mood_score']}/10"),
        ]

        for col, (icon, label, value) in zip(
            [col1, col2, col3, col4, col5], traits
        ):
            with col:
                st.markdown(f"""
                    <div style="
                        background:{AppConfig.CARD_BACKGROUND};
                        border:1px solid {AppConfig.BORDER_COLOR};
                        border-radius:12px;
                        padding:16px 12px;
                        text-align:center;
                    ">
                        <div style="font-size:1.5rem;">{icon}</div>
                        <div style="color:{AppConfig.TEXT_SECONDARY};
                             font-size:0.72rem; text-transform:uppercase;
                             letter-spacing:1px;
                             margin:6px 0 4px 0;">{label}</div>
                        <div style="color:{AppConfig.PRIMARY_COLOR};
                             font-size:1.1rem;
                             font-weight:700;">{value}</div>
                    </div>
                """, unsafe_allow_html=True)

        # Top words and phrases
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            top_words = ", ".join(pattern["top_words"][:8])
            st.markdown(f"""
                <div style="background:{AppConfig.CARD_BACKGROUND};
                            border:1px solid {AppConfig.BORDER_COLOR};
                            border-radius:10px; padding:14px 16px;">
                    <div style="color:{AppConfig.PRIMARY_COLOR};
                                font-size:0.8rem; font-weight:700;
                                margin-bottom:8px;">
                                🔤 Top Words</div>
                    <div style="color:{AppConfig.TEXT_SECONDARY};
                                font-size:0.82rem; line-height:1.8;">
                                {top_words}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            top_phrases = " &nbsp;•&nbsp; ".join(
                pattern["top_phrases"][:4]
            )
            st.markdown(f"""
                <div style="background:{AppConfig.CARD_BACKGROUND};
                            border:1px solid {AppConfig.BORDER_COLOR};
                            border-radius:10px; padding:14px 16px;">
                    <div style="color:{AppConfig.PRIMARY_COLOR};
                                font-size:0.8rem; font-weight:700;
                                margin-bottom:8px;">
                                💬 Common Phrases</div>
                    <div style="color:{AppConfig.TEXT_SECONDARY};
                                font-size:0.82rem; line-height:1.8;">
                                {top_phrases}</div>
                </div>
            """, unsafe_allow_html=True)

    # ------------------------------------------------------------------ #
    #  Role Selector                                                       #
    # ------------------------------------------------------------------ #

    def _render_role_selector(self):
        """
        Render two side by side role selectors.
        Left: User's own role | Right: AI's role
        Starts agent session when both roles are selected.
        """
        self._render_section_label("🎯 Assign Roles")

        users = self.agent.get_users()

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.markdown(
                f"<p style='color:{AppConfig.PRIMARY_COLOR};"
                f"font-size:0.8rem; font-weight:600;"
                f"margin-bottom:4px;'>👤 You are</p>",
                unsafe_allow_html=True
            )
            your_role = st.selectbox(
                label="You are",
                options=["Select your role..."] + users,
                label_visibility="collapsed",
                key="your_role_selector",
                help="Select which person you are in this conversation"
            )

        with col2:
            st.markdown(
                f"<p style='color:{AppConfig.PRIMARY_COLOR};"
                f"font-size:0.8rem; font-weight:600;"
                f"margin-bottom:4px;'>🤖 AI is</p>",
                unsafe_allow_html=True
            )

            # Filter out the user's own role from AI options
            ai_options = [
                u for u in users
                if u != your_role
            ] if your_role != "Select your role..." else users

            ai_role = st.selectbox(
                label="AI is",
                options=["Select AI role..."] + ai_options,
                label_visibility="collapsed",
                key="ai_role_selector",
                help="AI will respond as this person"
            )

        with col3:
            st.markdown(
                "<p style='margin-bottom:4px; font-size:0.8rem;"
                "color:transparent;'>.</p>",
                unsafe_allow_html=True
            )
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state[AppConfig.SESSION_CHAT_HISTORY] = []
                st.session_state["agent_session_active"]          = False
                st.rerun()

        # Status message
        both_selected = (
            your_role != "Select your role..."
            and ai_role != "Select AI role..."
        )

        if both_selected:
            st.success(
                f"✅ You are **{your_role}** "
                f"| AI is responding as **{ai_role}**"
            )
        elif your_role != "Select your role...":
            st.warning("⚠️ Now select who the AI should respond as")
        else:
            st.warning("⚠️ Select your role and AI role to start chatting")

        # Detect role changes and restart session
        prev_your_role = st.session_state.get("your_role")
        prev_ai_role   = st.session_state.get(AppConfig.SESSION_AGENT_ROLE)

        roles_changed = (
            your_role != prev_your_role
            or ai_role != prev_ai_role
        )

        if both_selected and roles_changed:
            # Save roles to session state
            st.session_state["your_role"]                    = your_role
            st.session_state[AppConfig.SESSION_AGENT_ROLE]  = ai_role
            st.session_state[AppConfig.SESSION_CHAT_HISTORY] = []
            st.session_state["agent_session_active"]          = False

        elif not both_selected:
            st.session_state[AppConfig.SESSION_AGENT_ROLE] = None

        # Start agent session if both roles selected and not active
        if both_selected and not st.session_state["agent_session_active"]:
            selected_model = st.session_state.get(
                AppConfig.SESSION_SELECTED_MODEL
            )
            model_name = (
                selected_model.get("name", AppConfig.DEFAULT_MODEL)
                if selected_model else AppConfig.DEFAULT_MODEL
            )

            try:
                self.agent.start_session(
                    ai_username=ai_role,
                    user_username=your_role,
                    model_name=model_name
                )
                self.agent.active_user_role = your_role
                st.session_state["agent_session_active"] = True
            except Exception as e:
                st.error(f"❌ Failed to start agent: {str(e)}")

    # ------------------------------------------------------------------ #
    #  Chat Window                                                         #
    # ------------------------------------------------------------------ #

    def _render_chat_window(self):
        """Render chat window with message history and input."""
        self._render_section_label("💬 Chat Window")

        role = st.session_state.get(AppConfig.SESSION_AGENT_ROLE)

        # Show empty state if no role selected
        if not role:
            st.markdown(f"""
                <div style="
                    background:{AppConfig.CARD_BACKGROUND};
                    border:1px solid {AppConfig.BORDER_COLOR};
                    border-radius:12px; padding:60px 20px;
                    text-align:center; min-height:300px;
                ">
                    <div style="font-size:2.5rem;">🤖</div>
                    <div style="color:{AppConfig.PRIMARY_COLOR};
                         font-size:1rem; font-weight:700;
                         margin:12px 0 6px 0;">Agent Ready</div>
                    <div style="color:{AppConfig.TEXT_SECONDARY};
                         font-size:0.85rem;">
                         Select a person above and start chatting.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            return

        # Render chat history
        chat_history = st.session_state.get(
            AppConfig.SESSION_CHAT_HISTORY, []
        )

        chat_container = st.container()
        with chat_container:
            if chat_history:
                for message in chat_history:
                    self._render_chat_bubble(
                        message["role"],
                        message["content"]
                    )
            else:
                st.markdown(
                    f"<p style='color:{AppConfig.TEXT_SECONDARY};"
                    f"font-size:0.85rem; text-align:center;"
                    f"padding:20px;'>"
                    f"Start chatting — AI is responding as {role}</p>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Message input
        col1, col2 = st.columns([5, 1])

        with col1:
            user_input = st.text_input(
                label="Type your message",
                placeholder=f"Message {role}...",
                label_visibility="collapsed",
                key=f"chat_input_{st.session_state['input_key']}"
            )

        with col2:
            send = st.button(
                "📨 Send",
                use_container_width=True,
                type="primary"
            )

        # Handle send — increment key to reset input field
        if send and user_input.strip():
            st.session_state["input_key"] += 1
            self._handle_send(user_input.strip(), role)

    def _handle_send(self, user_input: str, role: str):
        """
        Handle sending a message to the agent.
        Updates RPM/RPD counters in session state.

        :param user_input: User message text
        :param role: Active agent role
        """
        # Check if agent session is active
        if not st.session_state.get("agent_session_active"):
            st.error("⚠️ Agent session not active. Please reselect role.")
            return

        # Check RPD limit
        selected_model = st.session_state.get(
            AppConfig.SESSION_SELECTED_MODEL
        )
        rpd_limit = selected_model.get("rpd", 20) if selected_model else 20
        rpd_used  = st.session_state.get(AppConfig.SESSION_RPD_USED, 0)

        if rpd_used >= rpd_limit:
            st.error(
                "🔴 Daily message limit reached. "
                "Please try again tomorrow."
            )
            return

        with st.spinner(f"{role} is typing..."):
            try:
                # Get response from agent
                reply = self.agent.chat(user_input)

                # Update chat history
                history = st.session_state.get(
                    AppConfig.SESSION_CHAT_HISTORY, []
                )
                history.append({
                    "role":    "user",
                    "content": user_input
                })
                history.append({
                    "role":    "agent",
                    "content": reply
                })
                st.session_state[AppConfig.SESSION_CHAT_HISTORY] = history

                # Update usage counters
                st.session_state[AppConfig.SESSION_RPD_USED] = (
                    rpd_used + 1
                )
                st.session_state[AppConfig.SESSION_RPM_USED] = (
                    st.session_state.get(AppConfig.SESSION_RPM_USED, 0) + 1
                )

                st.rerun()

            except Exception as e:
                st.error(f"❌ Agent error: {str(e)}")

    # ------------------------------------------------------------------ #
    #  Chat Bubble                                                         #
    # ------------------------------------------------------------------ #

    def _render_chat_bubble(self, role: str, content: str):
        """
        Render a single chat bubble with real names.
        User name on right, AI person name on left.

        :param role: 'user' or 'agent'
        :param content: Message text
        """
        your_name  = st.session_state.get("your_role", "You")
        agent_name = st.session_state.get(
            AppConfig.SESSION_AGENT_ROLE, "AI"
        )

        if role == "user":
            st.markdown(f"""
                <div style="display:flex; justify-content:flex-end;
                            margin-bottom:12px;">
                    <div style="text-align:right;">
                        <div style="color:{AppConfig.PRIMARY_COLOR};
                             font-size:0.72rem; font-weight:700;
                             margin-bottom:3px;">{your_name}</div>
                       <div style="
                            background:{AppConfig.CHAT_USER_BG};
                            color:#FFFFFF;
                            border-radius:16px 16px 4px 16px;
                            padding:10px 16px;
                            min-width:80px;
                            max-width:420px;
                            width:fit-content;
                            font-size:0.9rem; line-height:1.5;
                            display:inline-block;
                            word-wrap:break-word;
                        ">{content}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="display:flex; justify-content:flex-start;
                            margin-bottom:12px;">
                    <div style="text-align:left;">
                        <div style="color:{AppConfig.SECONDARY_COLOR};
                             font-size:0.72rem; font-weight:700;
                             margin-bottom:3px;">{agent_name}</div>
                        <div style="
                            background:{AppConfig.CHAT_AGENT_BG};
                            border:1px solid {AppConfig.BORDER_COLOR};
                            color:#FFFFFF;
                            border-radius:16px 16px 16px 4px;
                            padding:10px 16px;
                            min-width:80px;
                            max-width:420px;
                            width:fit-content;
                            font-size:0.9rem; line-height:1.5;
                            display:inline-block;
                            word-wrap:break-word;
                        ">{content}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _render_section_label(self, label: str):
        """Render styled section label."""
        st.markdown(
            f"<p style='color:{AppConfig.TEXT_SECONDARY};"
            f"font-size:0.85rem; text-transform:uppercase;"
            f"letter-spacing:1px;'>{label}</p>",
            unsafe_allow_html=True
        )

    def _render_empty_state(self, message: str):
        """Render empty state card."""
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