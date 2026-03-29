FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Configure Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[theme]\nprimaryColor = '#1f77b4'\nbackgroundColor = '#ffffff'\nsecondaryBackgroundColor = '#f0f2f6'\ntextColor = '#262730'\nfont = 'sans serif'\n\n[server]\nheadless = true\nport = 8501\nenableXsrfProtection = true\n\n[client]\nshowErrorDetails = true" > ~/.streamlit/config.toml

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
