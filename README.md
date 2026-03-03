# 🧠 Snap Tutor (Study Analyzer)

**Snap Tutor** is an AI-powered learning assistant designed to help students analyze academic problems instantly. By using a Chrome Extension to capture questions from any website, the system leverages the **GPT-4o-mini** vision model to provide step-by-step diagnostic reports on a web-based dashboard.

---

## ✨ Features

- **Floating Capture Widget**: A seamless Chrome Extension that allows users to screenshot questions or solutions without leaving their current tab.
- **AI-Powered Diagnosis**: Automatically recognizes image content, determines correctness, and categorizes errors into 'careless' mistakes or 'concept' misunderstandings.
- **Interactive Dashboard**: A professional web interface built with Streamlit to display captured images and detailed AI-generated explanations side-by-side.
- **Live Cloud Sync**: Backend hosted on Render ensures that your data is synchronized between the browser extension and the dashboard.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Dashboard UI), JavaScript/CSS (Chrome Extension).
- **Backend**: Flask (Python), Gunicorn.
- **AI Engine**: OpenAI API (GPT-4o-mini).
- **Deployment**: Render (Web Service), GitHub (Version Control).

---

## 🚀 Quick Start

### 1. Backend Deployment
1. Upload the project code to GitHub.
2. Create a new "Web Service" on [Render](https://render.com/).
3. **Environment Variable**: Add your `OPENAI_API_KEY` in the Render dashboard settings.
4. **Start Command**: `gunicorn backend_v2:app`.

### 2. Chrome Extension Installation
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select the `Extension` folder from this project.

### 3. Dashboard Access
Run the Streamlit app locally or deploy it to a cloud platform:
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚙️ Configuration Reminder

Before installing the extension, ensure you have updated the following constants to match your deployment:

### 1. Update Backend URL in Extension
In `Extension/background.js`, locate the API URL and update it to your production link:
```javascript
// Extension/background.js
const EMILY_API_URL = '[https://snap-tutor.onrender.com/diagnose](https://snap-tutor.onrender.com/diagnose)'; // Replace with your Render URL

### 2. Update Backend URL in Extension
-In Extension/manifest.json:
Add your Render domain to host_permissions.

In app.py:
Update RENDER_URL to point to your backend.

---
// Extension/manifest.json
"host_permissions": [
    "[https://snap-tutor.onrender.com/](https://snap-tutor.onrender.com/)*" 
],

# app.py
RENDER_URL = "[https://snap-tutor.onrender.com](https://snap-tutor.onrender.com)" # Your Backend Render URL

## 📸 Workflow

1. **Invoke Extension**: Click the extension icon in your browser toolbar to summon the floating capture widget on any webpage.
2. **Capture**: Click the **"Question"** button. The widget will automatically hide itself, take a high-quality screenshot of the visible tab, and send the data to the Flask backend.
3. **AI Diagnosis**: The backend processes the image using the **GPT-4o-mini** model. It identifies the question, evaluates the student's answer, and generates a detailed explanation in JSON format.
4. **Data Storage**: The system saves the screenshot as a `.png` file and the AI report as a `.json` file within the server's `uploads/` directory.
5. **Review Results**: Refresh your **Snap Tutor** dashboard. The app automatically fetches the latest image and the corresponding AI diagnostic report via the backend API URL.

---

## 📁 Project Structure

```text
.
├── backend_v2.py        # Flask server: Handles image uploads, AI diagnosis, and file serving
├── requirements.txt     # Python dependency list (Flask, OpenAI, Streamlit, etc.)
└── Extension/           # Chrome Extension source files
    ├── app.py               # Streamlit dashboard: The web interface that displays reports via URL
    ├── background.js    # Service worker managing screenshots and backend communication
    ├── content.js       # Content script for the draggable floating UI widget
    └── manifest.json    # Extension metadata and required permissions
```
