# Obsidian Lecture Notes (OLN)

AI-powered lecture note generator for Obsidian that transforms lecture materials (PDFs, PPTXs) into structured Obsidian notes using LLMs.

## 🚀 Features
- **Multimodal Extraction**: Supports PDF and PPTX file uploads.
- **Template-Driven Generation**: Uses custom templates from your Obsidian vault to structure the generated notes.
- **Automated Vault Integration**: Writes processed notes directly to a specified Obsidian vault path.
- **Modern Stack**: FastAPI backend for high-performance processing and a Svelte 5 frontend.
- **Containerized Deployment**: Ready-to-go Docker configuration for consistent environments.

## 🛠 Installation

### Backend
1. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your OPENAI_API_KEY and other required settings
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## 💻 Usage
1. **Upload**: Upload your lecture PDF or PPTX via the frontend.
2. **Template Selection**: Choose a template from your `~/Notes/Templates` directory.
3. **Generate**: The system extracts content, applies the template, and writes the resulting `.md` file to your Obsidian vault.

## ⚙️ Configuration
The following environment variables are required in your `.env` file:
- `OPENAI_API_KEY`: Your OpenAI API key for note synthesis.
- `OBSIDIAN_VAULT_PATH`: Absolute path to your Obsidian vault.
- `TEMPLATES_DIR`: Path to your templates folder (defaults to `~/Notes/Templates`).

## 📦 Deployment
Deploy the project locally using the provided shell script:
```bash
./deploy.sh
```
This script handles Docker image builds and container orchestration via `docker-compose.yml`.

---
**Project Tag:** `OLN`
