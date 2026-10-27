import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    BASE_DIR = BASE_DIR
    OUTPUT_DIR = BASE_DIR / "output"
    ASSETS_DIR = BASE_DIR / "assets"
    FONTS_DIR = ASSETS_DIR / "fonts"
    MUSIC_DIR = ASSETS_DIR / "music"
    
    # Instagram & Branding
    INSTAGRAM_HANDLE = os.getenv("INSTAGRAM_HANDLE", "@stoic.discipline.daily")
    DEFAULT_TOPIC = os.getenv("DEFAULT_TOPIC", "DAILY DISCIPLINE")
    
    # ElevenLabs TTS Settings
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    # Default: "Adam" (deep, authoritative motivational voice: pNInz6obpgDQGcFmaJgB)
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
    
    # Fallback Edge-TTS Voice (used if ElevenLabs key is missing or quota exceeded)
    # en-US-ChristopherNeural is a deep, warm, cinematic male voice
    FALLBACK_TTS_VOICE = os.getenv("FALLBACK_TTS_VOICE", "en-US-ChristopherNeural")
    
    # Content Generation
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Social Distribution / Scheduling
    BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN", "")
    BUFFER_PROFILE_ID = os.getenv("BUFFER_PROFILE_ID", "")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    # Video Specifications (Instagram Reels 9:16)
    VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
    VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
    VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
    BACKGROUND_MUSIC_VOLUME = float(os.getenv("BACKGROUND_MUSIC_VOLUME", "0.14"))
    
    # Schedule Configuration
    SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "09:00")
    
    @classmethod
    def ensure_dirs(cls):
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.FONTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.MUSIC_DIR.mkdir(parents=True, exist_ok=True)

Config.ensure_dirs()
