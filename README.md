# 💬 WhatsApp Analyzer Pro

> An advanced data analytics and AI application that transforms raw WhatsApp chat exports into deep, meaningful insights — powered by Python, Streamlit, Sentiment Analysis and Google Gemini AI.

![Python](https://img.shields.io/badge/Python-3.14.2-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red?style=flat-square&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-27.4.0-blue?style=flat-square&logo=docker)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-green?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 🎯 Project Objective

WhatsApp Analyzer Pro is a portfolio-grade data science project built to demonstrate advanced analytical and AI skills through real-world WhatsApp chat data.

**Key Goals:**
- Parse and process unstructured WhatsApp text data into structured insights
- Apply NLP techniques for sentiment scoring and mood tracking
- Build an LLM-powered agent that learns from real chat patterns
- Present findings through an interactive, visually appealing dashboard
- Deploy end-to-end using Docker, Kubernetes and Jenkins CI/CD pipeline

---

## ✨ Features

### 📊 Analytics Dashboard
- Total messages, words, media and links overview
- Monthly and daily message timelines
- Activity heatmap (hour vs day of week)
- Most active users with contribution percentages
- Word cloud and top 20 most common words
- Emoji frequency and distribution analysis
- Response time analysis per user
- Conversation starter identification

### 🧠 Sentiment Analysis
- Per-message VADER sentiment scoring
- Overall mood score out of 10
- Monthly sentiment timeline (positive/negative trends)
- Sentiment heatmap by hour and day
- Per-user sentiment comparison
- Toxic and aggressive message detection

### 🤖 AI Chat Agent
- Dynamic personality extraction from real chat data
- Two-role conversation setup (you vs AI clone)
- Hinglish-aware LLM responses via Google Gemini
- Chat memory for multi-turn conversations
- RPM and RPD usage counter with warnings
- Model selector with rate limit display

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit, Custom CSS, Plotly |
| **Backend** | Python 3.14, Pandas, NLTK |
| **NLP** | VADER Sentiment, WordCloud |
| **AI/LLM** | Google Gemini API (google-genai) |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (K8s) |
| **CI/CD** | Jenkins |
| **Registry** | Docker Hub |

---

## 🏗️ Project Architecture

```
whatsapp-analyzer/
│
├── app.py                          # Main Streamlit entry point
│
├── config/
│   └── settings.py                 # App-wide constants & config
│
├── core/                           # OOP Business Logic
│   ├── base.py                     # Master Base/Super class
│   ├── preprocessor.py             # WhatsApp chat parser
│   ├── analyzer.py                 # Analytics computations
│   ├── sentiment.py                # Sentiment analysis
│   └── agent.py                    # AI Chat Agent
│
├── ui/                             # UI Components
│   ├── sidebar.py                  # Sidebar component
│   ├── dashboard.py                # Analytics dashboard
│   ├── sentiment_ui.py             # Sentiment UI
│   └── agent_ui.py                 # Agent chat UI
│
├── pages/                          # Streamlit multipage
│   ├── 1_How_To_Use.py             # How To Use guide
│   └── 2_Contact_Me.py             # Contact/Portfolio page
│
├── assets/
│   └── style.css                   # Custom CSS styling
│
├── data/
│   └── stop_hinglish.txt           # Hinglish stopwords
│
├── tests/                          # Unit tests
│
├── devops/                         # DevOps configuration
│   ├── Dockerfile                  # Docker build file
│   ├── docker-compose.yml          # Local Docker Compose
│   ├── Jenkinsfile                 # CI/CD Pipeline
│   └── k8s/
│       ├── deployment.yaml         # Kubernetes Deployment
│       └── service.yaml            # Kubernetes Service
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.14+
- pip
- Git
- Docker (optional, for containerized deployment)

### Local Development

**1. Clone the repository:**
```bash
git clone https://github.com/deepu84059/whatsapp-analyzer-pro.git
cd whatsapp-analyzer-pro
```

**2. Create and activate virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the app:**
```bash
streamlit run app.py
```

**5. Open in browser:**
```
http://localhost:8501
```

---

## 📱 How To Export WhatsApp Chat

**Android:**
1. Open WhatsApp chat
2. Tap three dots (⋮) → More → Export Chat
3. Select **Without Media**
4. Save the `.txt` file

**iPhone:**
1. Open WhatsApp chat
2. Tap contact/group name → Export Chat
3. Select **Without Media**
4. Save the `.txt` file

---

## 🔑 Gemini API Key Setup

The AI Chat Agent requires a free Google Gemini API key:

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API Key** → **Create API Key**
4. Copy the key and paste it in the app sidebar

**Free tier limits:**
| Model | RPM | RPD |
|---|---|---|
| gemini-2.5-flash-lite | 10 | 250 |
| gemini-2.5-flash | 5 | 20 |

---

## 🐳 Docker Deployment

**Build the image:**
```bash
docker build -f devops/Dockerfile -t whatsapp-analyzer:latest .
```

**Run the container:**
```bash
docker run -p 8501:8501 whatsapp-analyzer:latest
```

**Using Docker Compose:**
```bash
cd devops
docker-compose up
```
---

## 📊 OOP Architecture

The project follows a clean OOP design pattern:

```
Base (core/base.py)
├── Preprocessor    — Parses raw WhatsApp .txt into DataFrame
├── Analyzer        — Computes all analytics from DataFrame
├── Sentiment       — Scores sentiment and detects toxicity
└── Agent           — Extracts patterns and powers LLM chat
```

All shared utility methods (text cleaning, stopwords, emoji extraction, DataFrame filtering) live in the `Base` superclass and are inherited by all core classes.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

---

## 🌐 Live Demo

> Coming soon on Streamlit Cloud

---

## 👨‍💻 Author

**Deepu Kumar Rajak**
Data Scientist & AI Enthusiast · IIT Kharagpur

I'm passionate about leveraging AI to solve real-world problems. My work spans machine learning, deep learning, NLP, and generative AI applications.

🌐 [Portfolio](https://whimsical-conkies-ad5d60.netlify.app/)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io) — for the amazing web framework
- [Google Gemini](https://aistudio.google.com) — for the free LLM API
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) — for sentiment analysis
- [Plotly](https://plotly.com) — for interactive charts
