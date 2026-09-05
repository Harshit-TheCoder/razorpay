# Open Source AI Agent Integration

I have successfully added the capability for the Razorpay Agent to use a locally hosted, open-source AI model via Docker (using **Ollama**). This fulfills the request to create a new strategy specifically for Docker-based LLMs.

## What was built

### LLM Provider Strategy Pattern
- **Backend**: Updated `app/agent/graph.py` to support dynamic switching between the default `gemini` LLM provider and the new `ollama` provider.
- **Library Added**: Installed `langchain-ollama` into the Python backend virtual environment.
- **Integration**: `ChatOllama` is now instantiated when `LLM_PROVIDER=ollama` is set in your environment. It connects to the default local Docker endpoint (`http://localhost:11434`) and supports structured JSON outputs to match our required schema!

## How to Run This

Since Docker is not installed in my sandbox environment, you will need to run the following commands on your host machine to download and start the open-source model:

### 1. Start the Ollama Docker Container
Run this in your terminal to start Ollama in the background:
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 2. Pull an Open Source Model
We will pull **Llama 3** (or you can substitute `phi3` or `mistral`):
```bash
docker exec -it ollama ollama run llama3
```
*(Note: Keep this running or detach from it; the first run downloads the model weights)*

### 3. Run the Backend with Ollama
When starting the FastAPI backend, set the environment variables to instruct it to use the new Docker LLM strategy:

```bash
cd backend
source venv/bin/activate
LLM_PROVIDER=ollama OLLAMA_MODEL=llama3 python -m app.main
```

The system's AI agent will now orchestrate case recovery automatically using your local open-source Docker model!
