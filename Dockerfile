FROM ollama/ollama:latest

# Set model name as build argument
ARG MODEL_NAME=qwen3:4b

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y \
        python3.11 \
        python3.11-distutils \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Make Python 3.11 the default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

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
# Wait for Ollama to start\n\
sleep 5 && \n\
\n\
# Pull specified model\n\
ollama run ${MODEL_NAME} &\n\
\n\
sleep 5 && \n\
# Start FastAPI server\n\
exec uvicorn api:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh

RUN chmod +x /app/start.sh

# Only expose FastAPI port since Ollama will be internal
EXPOSE 8000

ENTRYPOINT ["/bin/bash"]
CMD ["/app/start.sh"]