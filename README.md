# ⚡ Instagram Motivation Video Agent

An autonomous AI agent that generates daily high-retention 9:16 vertical motivational reels (1080x1920) with **minimalist kinetic typography**, **real-time audio spectrum visualizers**, **cinematic ambient soundtrack**, and **automated posting/queueing to Instagram** via Buffer & Webhooks.

---

## 🌟 Key Features

1. **Minimalist Kinetic Typography Engine**:
   - High-impact editorial design (1080x1920 9:16 vertical video).
   - Real-time word-by-word active glow highlight (words illuminate in golden amber as they are spoken).
   - Category pill badges, author attribution, and custom brand handle (`@yourhandle`).
   - Sleek bottom progress bar.

2. **Dynamic Audio Waveform Visualizer**:
   - 42-band symmetric audio spectrum analyzer that dances dynamically to the narrator's vocal cadence with smooth attack/decay physics.

3. **Ultra-Realistic Voiceover (ElevenLabs & Edge-TTS Fallback)**:
   - Built-in integration for **ElevenLabs API** (deep, authoritative voices like Adam or Antoni).
   - Zero-dependency fallback to **Microsoft Edge Neural Voice** (`en-US-ChristopherNeural` - 100% free, high quality, no API key needed).

4. **Cinematic Ambient Drone**:
   - Procedurally generated deep cinematic drone and bass pad that sits underneath the narration at -18 dB to build anticipation and focus.

5. **Viral Content & Caption Generator**:
   - Rotates through a curated collection of 50+ masterclass scripts (Stoicism, Relentless Focus, Silence, Habit Discipline, Resilience).
   - Generates complete Instagram captions with call-to-action questions and 15+ trending hashtags.
   - Optional **Google Gemini API** integration for custom AI script creation.

6. **Social Scheduler Integration**:
   - **Buffer API**: Directly schedules posts into your Buffer Instagram queue.
   - **Webhooks**: Dispatches JSON payloads to Make.com, Zapier, or n8n to upload and publish reels to Instagram automatically.

7. **Interactive Web Studio**:
   - Sleek dark-mode Studio dashboard on `http://localhost:8000`.
   - iPhone simulator video player to preview 9:16 reels in real time.
   - One-click reel generation, caption copying, and settings management.

8. **24/7 Cloud Automation via GitHub Actions**:
   - Pre-configured `.github/workflows/daily_reel.yml` to trigger the pipeline every day at 9:00 AM UTC without needing your computer turned on!

---

## 🚀 Quick Start

### 1. Launch the Studio Web UI

```bash
cd /Users/chetanbisariya/.gemini/antigravity-ide/scratch/insta-motivation-agent
.venv/bin/uvicorn studio.app:app --host 127.0.0.1 --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

### 2. Generate a Reel from CLI

Generate today's reel immediately:
```bash
.venv/bin/python -m agent.runner --now
```

Generate with a custom topic:
```bash
.venv/bin/python -m agent.runner --topic "RELENTLESS FOCUS"
```

Generate with a custom quote/prompt:
```bash
.venv/bin/python -m agent.runner --prompt "Miyamoto Musashi on why silence is the ultimate weapon."
```

---

### 3. Run the Daily Scheduler Daemon

Keep the agent running in the background to post automatically every day at 09:00 AM:
```bash
.venv/bin/python -m agent.runner --schedule "09:00"
```

Or run via macOS Cron / Launchd using `run_daily.sh`:
```bash
./run_daily.sh
```

---

## ⚙️ Configuration (`.env`)

Configure your keys in `.env` (or via the Studio UI Settings modal):

```ini
# Brand / Watermark
INSTAGRAM_HANDLE=@stoic.discipline.daily
DEFAULT_TOPIC="DAILY DISCIPLINE"

# ElevenLabs Voice AI (Optional - leave blank for free neural voice)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_VOICE_ID=pNInz6obpgDQGcFmaJgB
ELEVENLABS_MODEL_ID=eleven_multilingual_v2

# Social Scheduler: Buffer Integration
BUFFER_ACCESS_TOKEN=your_buffer_token
BUFFER_PROFILE_ID=your_instagram_channel_id

# Social Scheduler: Webhook (Make.com / Zapier)
WEBHOOK_URL=https://hook.eu1.make.com/your_webhook_id

# Daily Execution Time (24h format)
SCHEDULE_TIME=09:00
```

---

## 📁 Project Architecture

```
insta-motivation-agent/
├── .env.example              # Environment variables template
├── .env                      # Active settings and API keys
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── run_daily.sh              # Cron / Launchd executable script
├── .github/workflows/
│   └── daily_reel.yml        # GitHub Actions 24/7 cloud daily cron
├── assets/
│   ├── fonts/                # Inter & Anton modern bold fonts
│   └── music/                # Ambient cinematic audio tracks
├── agent/
│   ├── config.py             # Global configuration
│   ├── generator.py          # Script & Caption engine
│   ├── voice.py              # ElevenLabs & Edge-TTS synthesizer
│   ├── visualizer.py         # FFT Audio waveform spectrum analyzer
│   ├── video_engine.py       # 1080x1920 Minimalist Reel renderer
│   ├── publisher.py          # Buffer & Webhook dispatcher
│   └── runner.py             # CLI runner & scheduler daemon
├── studio/
│   ├── app.py                # FastAPI backend
│   └── static/               # Dark-mode Studio Web UI
└── output/                   # Rendered MP4 reels and metadata JSON
```

---

## 📱 Publishing to Instagram via Make.com or Buffer

### Option A: Buffer
1. Connect your Instagram Business or Creator account to [Buffer](https://buffer.com).
2. Grab your Access Token and Profile ID from the Buffer developer settings.
3. Paste them into `.env` or the Studio UI Settings modal.
4. Each daily video will be queued directly into Buffer's daily publishing calendar!

### Option B: Make.com / Zapier Webhook
1. Create a free webhook on [Make.com](https://make.com).
2. Add the **Instagram for Business** -> **Create a Reel** module.
3. Paste the Webhook URL into `.env`.
4. The agent dispatches `{ video_path, caption, hashtags, topic }` whenever a new reel is produced.
