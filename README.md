# Visa Attorney Agent ⚖️

An autonomous AI agent built with **LangGraph**, **FastAPI**, and **Gemini 3.1 Flash** to provide US immigration information.

## Tech Stack
- **Orchestration:** LangGraph (StateGraph)
- **Model:** Google Gemini 3.1 Flash (Free Tier)
- **Backend:** FastAPI / Uvicorn
- **Frontend:** Tailwind CSS / Vanilla JS
- **Package Manager:** uv

## Setup
1. Clone the repo: `git clone <url>`
2. Install dependencies: `uv sync`
3. Create a `.env` file with `GOOGLE_API_KEY=your_key`
4. Run the backend: `uv run python app.py`
5. Open `index.html` in your browser.