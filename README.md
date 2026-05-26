# SkillWiz AI Agent

A small AI agent that suggests a student's next learning step based on stored progress.

## Requirements
- Python 3.10+
- Optional: Ollama running locally for free LLM responses

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Copy .env.example to .env and adjust values if needed.

## Run (PowerShell)
$env:PYTHONPATH="src"
python -m skillwiz --user-id user_123 --question "What should I do today?"

If no question is provided, the app will prompt for one.

## Data
The SQLite database is created at data/skillwiz.db on first run and seeded from data/seed.json.

## Notes
- If Ollama is not available, the agent falls back to rule-based responses.
