FROM python:3.9-slim

WORKDIR /app

# Copy badproxy settings, which help if a transparent proxy is causing issues
# (Optional but often fixes “Hash Sum mismatch” on some networks.)
COPY badproxy /etc/apt/apt.conf.d/99fixbadproxy

# Example "badproxy" file contents:
#   Acquire::http::Pipeline-Depth "0";
#   Acquire::http::No-Cache "true";
#   Acquire::BrokenProxy "true";

RUN echo 'Acquire::http::Pipeline-Depth 0;\nAcquire::http::No-Cache true;\nAcquire::BrokenProxy true;\n' > /etc/apt/apt.conf.d/99fixbadproxy

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
    git g++ curl gnupg ca-certificates chromium && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get -y --no-install-recommends install nodejs && \
    apt-get -y --no-install-recommends install \
    libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 \
    libcairo2 libgtk-3-0 libgbm1 libxcomposite1 libxdamage1 libxfixes3 \
    libxrandr2 libxext6 libxi6 libxcursor1 libglib2.0-0 libdrm2 \
    libxinerama1 libpango1.0-0 libgdk-pixbuf2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt puppeteer-config.json ./
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install -g @mermaid-js/mermaid-cli
RUN pip install pylint==3.2.2 mypy==1.10.0 pandas-stubs==1.2.0.57

EXPOSE 8510

# Don't copy the code, it will be mounted as a volume