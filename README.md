# Ballet Cardiac Report Generator

Streamlit app to generate echocardiography / ECG / fietstest / Holter / CIED reports.

This repository contains the Streamlit UI entrypoint `app.py` and the `cardiac_report` package.

Requirements
- A Python 3.10+ environment
- `requirements.txt` (already included)

Quick local run

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app locally:

```powershell
streamlit run app.py
```

Prepare and push to GitHub

1. Initialize git (if not already):

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

2a. Create a GitHub repository using the GitHub CLI (recommended):

```bash
gh repo create YOUR_USERNAME/REPO_NAME --public --source=. --remote=origin --push
```

2b. Or create an empty repository on github.com and then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

Deploy to Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click "New app" → choose repository, branch `main` and set the main file to `app.py`.
3. In "Advanced settings" you can set environment variables (for example `BACKEND_URL`) or secrets.

Notes for a robust deploy
- Ensure `requirements.txt` lists all dependencies.
- Add any secret keys or API base URLs via Streamlit Cloud's secrets (do NOT store them in the repo).
- If your app expects a specific entry filename, specify `app.py` when creating the Streamlit app.

Optional: create repository from the command line and push (if you prefer SSH):

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
git push -u origin main
```

Troubleshooting
- If the app errors on Streamlit Cloud, check the app logs on the Streamlit dashboard. Common issues are missing packages (add to `requirements.txt`) or missing secrets (`secrets.toml`)
- Locally, run `streamlit run app.py` and inspect the console output for tracebacks.

Security
- Do not commit `.env` or `secrets.toml`. Use Streamlit Cloud secret manager.

If you want, I can:
- Create a `LICENSE` file and a concise project description in this `README`.
- Add a GitHub Actions workflow for linting/tests.
- Create a minimal `.streamlit/config.toml` to set theme or server options.
# Ballet Cardiac Report Generator

Streamlit app to generate cardiology echo reports.

Files of interest:
- `app.py` — main Streamlit app
- `requirements.txt` — Python dependencies (used by Streamlit Cloud)
- `launcher.py` / `dist/launcher.exe` — local executable (optional)

Quick deployment to Streamlit Cloud
1. Push this repository to GitHub (public or private).
2. On https://share.streamlit.io (Streamlit Cloud) click "New app" → connect your GitHub repo → choose branch and `app.py` as the main file.
3. Streamlit Cloud will install packages from `requirements.txt` and start the app. Open the web link provided.

Notes
- Remove large build artifacts (e.g. `dist/`, `.venv/`) before pushing.
- If you use secrets (API keys etc), set them in the Streamlit Cloud app settings (do NOT commit them).
- If the app uses heavy binary packages or large amounts of data the free Streamlit Cloud plan might be insufficient.
- PDF upload parsing depends on `pdfplumber`. If a PDF contains only images (no selectable text) the app automatically falls back to OCR, which requires a local Tesseract installation (https://github.com/tesseract-ocr/tesseract) plus the `pytesseract` Python package.
- On Windows, install Tesseract (e.g. via the official installer), tick “add to PATH”, then `pip install pytesseract`. On macOS use `brew install tesseract`. After installation restart Streamlit so the new binary is detected.

If you want, I can:
- Create a git commit locally for you (you will need to push to GitHub from your machine), or
- Walk through creating the GitHub repo and linking it to Streamlit Cloud step-by-step.
