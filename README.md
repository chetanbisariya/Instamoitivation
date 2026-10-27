# ⚡ Instagram Multi-Story, Motivation & 3-Keyword Cinema Agent

An autonomous AI agent and interactive Web Studio that generates daily high-retention 9:16 vertical reels (1080x1920) across **Multi-Genre Storytelling** (Motivation, Adventure, Romantic, Thriller, Wisdom), **3-Keyword Cinematic Micro-Movies**, **Photorealistic Innocent Narrator Avatars with Audio-Reactive Glow**, **Natural Girl & Male Neural Voices**, and **Custom Character / Voice Cloning Uploads (Creator Lab)**.

---

## 🌟 Key Features

1. **🎬 3-Keyword Cinematic Micro-Studio**:
   - Provide any 3 keywords (e.g. `Midnight`, `Lighthouse`, `Key` or randomized with one click).
   - Automatically scripts a complete **3-act cinematic short film**:
     - **Act I**: Inciting Incident (introduces Keyword 1)
     - **Act II**: Rising Conflict / Suspense (introduces Keyword 2)
     - **Act III**: Climax / Shocking Twist (introduces Keyword 3)
   - Widescreen 2.39:1 anamorphic cinema aesthetic with real-time active keyword glow tracking, act title badges (`ACT I: THE ANOMALY`), and genre-tailored cinematic soundtracks (Thriller, Sci-Fi, Adventure, Romance, Noir).

2. **📖 Multi-Genre Autonomous Storytelling**:
   - **Motivation & Stoic**: Daily discipline, relentless focus, unshakeable resilience.
   - **Adventure & Quest**: Ancient expeditions, hidden chasms, mountain summits.
   - **Romantic & Poetic**: Twilight encounters, unspoken letters, emotional intimacy.
   - **Thriller & Suspense**: The 3 AM anomaly, forbidden vaults, neo-noir mysteries.
   - **Life Wisdom & Parables**: Stillness in chaos, the ripple effect, timeless perspective.

3. **🎭 Innocent Avatars with Audio-Reactive Aura**:
   - Photorealistic innocent avatars: **Ava** (Kind & Innocent Female), **Lucas** (Warm & Sincere Male), **Elena** (Poetic Storyteller), **Leo** (Adventurer).
   - Outer glowing energy ring expands and contracts in real-time according to vocal loudness.
   - 42-band symmetric FFT audio spectrum visualizer dancing to narrator speech.

4. **✨ Creator Lab (Custom Characters & Voice Cloning)**:
   - **Upload Custom Character**: Drag & drop any portrait to register a new narrator.
   - **Voice Cloning / Upload**: Instant ElevenLabs voice cloning or local audio reference.
   - **Direct Spoken Narration**: Upload your own spoken audio recording and render a 1080x1920 reel with synchronized subtitles and waveforms!

5. **🎙️ Natural Girl & Male Neural Voices**:
   - Natural female voices: Ava (Gentle), Emma (Expressive), Jenny (Cheerful), Sonia (British Elegance).
   - Natural male voices: Brian (Kind), Andrew (Youthful Explorer), Christopher (Deep Cinematic), Ryan (British Storyteller).
   - ElevenLabs integration with automatic fallback to high-quality Microsoft Edge Neural TTS.

6. **📱 Interactive Web Studio (`http://localhost:8000`)**:
   - Switch between **Story & Motivation Reel** and **3-Keyword Short Movie** studio modes.
   - Live iPhone 9:16 simulator player with real-time playback.
   - One-click publishing to Instagram via **Buffer API** or **Make.com / Zapier Webhooks**.

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

### 3. Generate a 3-Keyword Short Movie from CLI

Generate an epic 3-act cinematic film from 3 keywords:
```bash
.venv/bin/python -m agent.runner --movie --k1 "Midnight" --k2 "Lighthouse" --k3 "Key" --genre THRILLER
```

Sci-Fi time travel film:
```bash
.venv/bin/python -m agent.runner --movie --k1 "Eclipse" --k2 "Observatory" --k3 "Signal" --genre SCI-FI
```

Adventure or Romantic film:
```bash
.venv/bin/python -m agent.runner --movie --k1 "Shipwreck" --k2 "Jungle" --k3 "Amulet" --genre ADVENTURE --avatar male_adventurer
```

---

### 4. Run the Daily Scheduler Daemon

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
