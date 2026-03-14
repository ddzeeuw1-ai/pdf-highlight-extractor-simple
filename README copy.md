---
title: PDF Highlight Extractor
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "4.0.0"
app_file: app.py
pinned: false
license: mit
---

# PDF Highlight Extractor (Simple version)

Extract all highlighted text from any PDF. Upload a file, get a clean text,
Markdown, or JSON export. Built for academics and researchers.

This is the simple single-file version of the app. The full version with a
custom React frontend lives in the `../` folder.

---

## Deploy in 3 ways

### Option 1 — Hugging Face Spaces (recommended, free, 5 minutes)

1. Create a free account at huggingface.co
2. Click **New Space** → give it a name → choose **Gradio** as the SDK
3. Clone the Space repo locally:
   ```bash
   git clone https://huggingface.co/spaces/your-username/your-space-name
   ```
4. Copy these four files into it:
   - `app.py`
   - `pdf_extractor.py`
   - `text_cleaner.py`
   - `requirements.txt`
5. Push:
   ```bash
   git add . && git commit -m "Add app" && git push
   ```
6. Hugging Face builds and hosts it automatically.
   Your app is live at `https://huggingface.co/spaces/your-username/your-space-name`

---

### Option 2 — Render (free, slightly more setup)

1. Create a free account at render.com
2. New **Web Service** → connect your GitHub repo
3. Set:
   - **Root Directory:** `simple`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
4. Deploy — Render gives you a public URL automatically.

Note: add `server_name="0.0.0.0"` and `server_port=int(os.environ.get("PORT", 7860))`
to `demo.launch()` so Render can route traffic correctly:
```python
import os
demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
```

---

### Option 3 — PythonAnywhere (simplest for Python beginners)

1. Create a free account at pythonanywhere.com
2. Go to **Files** and upload all four files
3. Open a **Bash console** and run:
   ```bash
   pip install gradio pypdf pdfplumber --user
   python app.py
   ```
4. Go to the **Web** tab → Add a new web app → point it at `app.py`

PythonAnywhere's free tier has some limitations on network access, so
Hugging Face Spaces is generally more reliable for this use case.

---

## Run locally

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:7860
```

---

## Why this version exists

This is the same PDF extraction logic as the full version, but wrapped in
Gradio instead of React + FastAPI. The tradeoff:

| | Simple (this) | Full version |
|---|---|---|
| Lines of code | ~150 | ~1000+ |
| Setup time | 5 minutes | Several hours |
| Customisability | Limited | Full control |
| Deployment | HF Spaces / Render | Vercel + Railway |
| Best for | Getting started, small groups | Production, custom features |
