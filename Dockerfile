FROM python:3.9-slim

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Expose the port for Streamlit
EXPOSE 8510
EXPOSE 8511
# Install system packages, Node.js, and Chromium dependencies
RUN apt-get update && apt-get install -yqq \
    # Essential tools
    git \
    g++ \
    curl \    
    gnupg \
    ca-certificates \
    # Chromium dependencies
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcairo2 \
    libgtk-3-0 \
    libgbm1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxext6 \
    libxi6 \
    libxcursor1 \
    libglib2.0-0 \
    libdrm2 \
    libxinerama1 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    # Install Node.js 18.x
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    # Install Mermaid CLI globally
    && npm install -g @mermaid-js/mermaid-cli \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Install additional Python tools
RUN pip install pylint==3.2.2 mypy==1.10.0 pandas-stubs==1.2.0.57 jupyter

COPY puppeteer-config.json /app/puppeteer-config.json

# Copy the rest of your application code
COPY . /app

# Run your Streamlit application
CMD ["sh", "-c", "streamlit run show_mermaid.py --server.port 8510 --server.address 0.0.0.0 & jupyter notebook --ip=0.0.0.0 --port=8512 --no-browser --allow-root"]