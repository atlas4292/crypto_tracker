FROM ubuntu:latest

# Make ARG available as ENV during runtime
ENV MODEL_NAME=qwen3:4b

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
        python3.11 \
        python3.11-distutils \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Make Python 3.11 the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Install Ollama using official install script
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy project files
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Ollama in the background\n\
ollama serve &\n\
\n\
# Wait for Ollama to be ready\n\
until curl -s http://localhost:11434/api/health >/dev/null; do\n\
    echo "Waiting for Ollama to start..."\n\
    sleep 1\n\
done\n\
\n\
# Pull specified model\n\
echo "Pulling model ${MODEL_NAME}..."\n\
ollama pull ${MODEL_NAME}\n\
\n\
# Start FastAPI server\n\
exec uvicorn api:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh

RUN chmod +x /app/start.sh

# Only expose FastAPI port since Ollama will be internal
EXPOSE 8000

ENTRYPOINT ["/bin/bash"]
CMD ["/app/start.sh"]