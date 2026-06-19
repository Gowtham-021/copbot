TN Police Cop Bot

Small Flask app that provides FIR, bail, crime type info and integrates with a local Ollama LLM.

Quick start

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Install and run Ollama (if using LLM features) and install a model via the Ollama app or CLI.

4. Set environment variables and run the app:

```powershell
$env:MODEL_BACKEND = 'ollama'
$env:MODEL_PATH = 'mistral'  # replace with your Ollama model name
python .\app.py
```

5. Open http://127.0.0.1:5001 in your browser.

Pushing to GitHub

- Create a remote repository on GitHub and then run:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <git@github.com:USERNAME/REPO.git> OR https://github.com/USERNAME/REPO.git
git push -u origin main
```

Or using GitHub CLI:

```powershell
gh repo create USERNAME/REPO --public --source=. --remote=origin --push
```

Files to review before pushing

- `venv/` is included in `.gitignore` (do not commit).
- Remove any large model files (GGUF) before pushing.
