# Obsidian Lecture Notes (OLN)

AI-powered lecture note generator for Obsidian.
- Frontend: Svelte 5
- Backend: Python


## ⚙️ Environment Setup

1. Copy the example environment file:
   `cp .env.example .env`
2. Edit `.env` with your actual API keys and database credentials.
3. The backend reads from `.env` via `python-dotenv`.
4. The frontend reads environment variables via SvelteKit's `$env/dynamic/private` or `$env/static/private`.
