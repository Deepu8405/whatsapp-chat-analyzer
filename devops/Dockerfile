# =============================================================================
# Dockerfile — WhatsApp Analyzer Pro
# Multi-stage build for optimized production image
# Python 3.14.2 base
# =============================================================================

# ---- Base Image ----
FROM python:3.14.2-slim

# ---- Maintainer ----
LABEL maintainer="Deepu Kumar Rajak"
LABEL description="WhatsApp Analyzer Pro — Data Analytics & AI App"
LABEL version="1.0.0"

# ---- Environment Variables ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---- Working Directory ----
WORKDIR /app

# ---- System Dependencies ----
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy Requirements First (for layer caching) ----
COPY requirements.txt .

# ---- Install Python Dependencies ----
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ---- Copy Project Files ----
COPY . .

# ---- Expose Streamlit Port ----
EXPOSE 8501

# ---- Health Check ----
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ---- Run Application ----
ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.headless=true", \
            "--browser.gatherUsageStats=false"]