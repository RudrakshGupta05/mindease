# 🌿 MindEase AI — Autonomous Mental Health & Wellness Companion

MindEase is an AI-powered emotional wellness companion designed to provide a calm, judgment-free space to reflect, decompress, and practice grounding mindfulness. Built with a warm skeuomorphic interface, interactive 3D robotic companion, proactive crisis intervention safeguards, and persistent conversational memory.

---

## ✨ Features

- **Warm Skeuomorphic Design:** Tactile cards, parchment texture (`#FFEAD3`), soft mint assistant bubbles (`#BFE7EA`), embossed terracotta buttons (`#D46743`), sage green accents (`#B7D894`), and warm amber tones (`#E89B5B`).
- **Flowing Ambient Header:** Smooth, continuous fluid ambient gradient animation that gently illuminates the top bar.
- **Interactive 3D Robot Companion:** Three.js companion head that reacts and tracks your interactions with thoughtful expressions.
- **Clerk Authentication & Privacy:** Secure sign-in to safeguard conversations; guest access to chat is strictly protected.
- **Multi-Turn Persistent Chat:** Full conversation history per user with cross-session retrieval and Chrome/Safari-compatible conversation management.
- **Crisis Detection Safeguards:** Built-in proactive crisis keyword analysis with immediate 24/7 helpline routing (988 / Vandrevala Foundation).
- **Deployment-Ready:** Containerized with Docker, health checks, environment templates, and multi-cloud readiness (Render, Railway, Fly.io, Cloud Run).

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python 3.11, Uvicorn, Pydantic, Groq API (Llama 3.3 70B / 120B Versatile)
- **Frontend:** Vanilla HTML5, Vanilla CSS3 (Custom Skeuomorphic Design System), Modern JavaScript
- **3D Graphics:** Three.js
- **Auth:** Clerk SDK
- **Data Persistence:** JSON-based stateful conversation store with normalized ID matching

---

## 🚀 Quickstart (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/RudrakshGupta05/mindease.git
cd mindease
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```
Fill in your credentials:
```ini
GROQ_API_KEY=gsk_your_groq_api_key_here
CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_publishable_key_here
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_clerk_publishable_key_here
PORT=8000
```

### 5. Start the development server
```bash
uvicorn main:app --reload --port 8000
```
Open your browser and navigate to:
```
http://localhost:8000/app/
```

---

## 🐳 Docker Deployment

You can build and run MindEase with Docker:

```bash
# Build the Docker image
docker build -t mindease .

# Run the container
docker run -p 8000:8000 --env-file .env mindease
```

Check application health:
```bash
curl http://localhost:8000/health
```

---

## ☁️ Cloud Deployment

### Deploying to Render
1. Create a new **Web Service** on [Render](https://render.com).
2. Connect your GitHub repository `RudrakshGupta05/mindease`.
3. Choose **Docker** or **Python 3** environment.
   - If Python:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. In **Environment Variables**, add:
   - `GROQ_API_KEY`
   - `CLERK_PUBLISHABLE_KEY`

### Deploying to Railway
1. Click **New Project** -> **Deploy from GitHub repo**.
2. Select `mindease`.
3. Railway automatically detects the `Dockerfile` or `Procfile`.
4. Add your environment variables in the Railway dashboard.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to `/app/` |
| `GET` | `/app/` | Serves the companion web application |
| `GET` | `/health` | Container & service health check (`{"status": "ok"}`) |
| `GET` | `/config` | Returns public Clerk configuration |
| `GET` | `/conversations?user_id=...` | List conversations for authenticated user |
| `POST` | `/conversations` | Create a new conversation thread |
| `GET` | `/conversations/{id}?user_id=...` | Retrieve message history for a conversation |
| `DELETE` | `/conversations/{id}?user_id=...` | Delete a conversation |
| `POST` | `/chat` | Send a message to the AI Companion |

---

## 📄 License

MIT License. Designed with care for mental wellness support.
