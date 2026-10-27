import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Config:
    BASE_DIR = BASE_DIR
    OUTPUT_DIR = BASE_DIR / "output"
    ASSETS_DIR = BASE_DIR / "assets"
    FONTS_DIR = ASSETS_DIR / "fonts"
    MUSIC_DIR = ASSETS_DIR / "music"
    AVATARS_DIR = ASSETS_DIR / "avatars"
    UPLOADS_DIR = ASSETS_DIR / "uploads"
    SFX_DIR = ASSETS_DIR / "sfx"
    CUSTOM_AVATARS_FILE = ASSETS_DIR / "custom_characters.json"
    CUSTOM_VOICES_FILE = ASSETS_DIR / "custom_voices.json"
    
    # Instagram & Branding
    INSTAGRAM_HANDLE = os.getenv("INSTAGRAM_HANDLE", "@stoic.discipline.daily")
    DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "ROMANTIC")
    DEFAULT_TOPIC = os.getenv("DEFAULT_TOPIC", "MIDNIGHT CONFESSIONS")
    
    # ElevenLabs TTS Settings
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
    
    # Default Fallback Voice (Free Neural Voice)
    DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "ava_female")
    FALLBACK_TTS_VOICE = os.getenv("FALLBACK_TTS_VOICE", "en-US-AvaNeural")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
    
    # Content Generation
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Social Distribution / Scheduling
    BUFFER_ACCESS_TOKEN = os.getenv("BUFFER_ACCESS_TOKEN", "")
    BUFFER_PROFILE_ID = os.getenv("BUFFER_PROFILE_ID", "")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
    
    # Direct Social Auto-Publishing (Instagram Graph API & YouTube)
    INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
    
    # Video Specifications (Instagram Reels 9:16)
    VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
    VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
    VIDEO_FPS = int(os.getenv("VIDEO_FPS", "30"))
    BACKGROUND_MUSIC_VOLUME = float(os.getenv("BACKGROUND_MUSIC_VOLUME", "0.14"))
    SFX_VOLUME = float(os.getenv("SFX_VOLUME", "0.22"))
    
    # Schedule Configuration
    SCHEDULE_TIME = os.getenv("SCHEDULE_TIME", "09:00")
    SCHEDULE_CATEGORY_ROTATION = os.getenv("SCHEDULE_CATEGORY_ROTATION", "true").lower() == "true"
    DEFAULT_AVATAR = os.getenv("DEFAULT_AVATAR", "female_innocent")
    SHOW_AVATAR = os.getenv("SHOW_AVATAR", "true").lower() == "true"

    # Multi-Language Directory
    SUPPORTED_LANGUAGES = {
        "en": {"code": "en", "name": "English", "native": "English", "flag": "🇺🇸"},
        "hi": {"code": "hi", "name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳"},
        "es": {"code": "es", "name": "Spanish", "native": "Español", "flag": "🇪🇸"},
        "fr": {"code": "fr", "name": "French", "native": "Français", "flag": "🇫🇷"},
        "de": {"code": "de", "name": "German", "native": "Deutsch", "flag": "🇩🇪"},
        "ja": {"code": "ja", "name": "Japanese", "native": "日本語", "flag": "🇯🇵"},
    }

    # Base Supported Neural Voices (Female & Male across languages)
    _BASE_VOICES = {
        "ava_female": {
            "name": "Ava (Gentle & Innocent)",
            "gender": "Female",
            "edge_id": "en-US-AvaNeural",
            "eleven_id": "21m00Tcm4TlvDq8ikWAM",
            "description": "Warm, innocent, sweet, conversational female tone"
        },
        "emma_female": {
            "name": "Emma (Expressive & Warm)",
            "gender": "Female",
            "edge_id": "en-US-EmmaNeural",
            "eleven_id": "EXAVITQu4vr4xnSDxMaL",
            "description": "Heartfelt, emotive, poetic female narrator"
        },
        "jenny_female": {
            "name": "Jenny (Crisp & Cheerful)",
            "gender": "Female",
            "edge_id": "en-US-JennyNeural",
            "eleven_id": "AZnzlk1XvdvUeBnXmlld",
            "description": "Energetic, clear, storytelling female voice"
        },
        "sonia_female": {
            "name": "Sonia (British Elegance)",
            "gender": "Female",
            "edge_id": "en-GB-SoniaNeural",
            "eleven_id": "ThT5KcBeYPX3keUQqHPh",
            "description": "Sophisticated, serene British female storyteller"
        },
        "brian_male": {
            "name": "Brian (Kind & Innocent)",
            "gender": "Male",
            "edge_id": "en-US-BrianNeural",
            "eleven_id": "ErXwobaYiN019PkySvjV",
            "description": "Kind, sincere, gentle, approachable male voice"
        },
        "andrew_male": {
            "name": "Andrew (Youthful & Adventurous)",
            "gender": "Male",
            "edge_id": "en-US-AndrewNeural",
            "eleven_id": "TxGEqnHWrfWFTfGW9XjX",
            "description": "Youthful, dynamic, confident explorer"
        },
        "christopher_male": {
            "name": "Christopher (Deep & Cinematic)",
            "gender": "Male",
            "edge_id": "en-US-ChristopherNeural",
            "eleven_id": "pNInz6obpgDQGcFmaJgB",
            "description": "Authoritative, deep, grounding cinematic voice"
        },
        "ryan_male": {
            "name": "Ryan (British Storyteller)",
            "gender": "Male",
            "edge_id": "en-GB-RyanNeural",
            "eleven_id": "VR6AewLTigWG4xSOukaG",
            "description": "Thoughtful, atmospheric British narrator",
            "lang": "en"
        },
        # Hindi Voices (हिंदी)
        "swara_hindi_female": {
            "name": "Swara (Hindi Storyteller)",
            "gender": "Female",
            "edge_id": "hi-IN-SwaraNeural",
            "eleven_id": "21m00Tcm4TlvDq8ikWAM",
            "description": "Warm, expressive Hindi female storyteller",
            "lang": "hi"
        },
        "madhur_hindi_male": {
            "name": "Madhur (Hindi Narrator)",
            "gender": "Male",
            "edge_id": "hi-IN-MadhurNeural",
            "eleven_id": "pNInz6obpgDQGcFmaJgB",
            "description": "Deep, poetic Hindi male narrator",
            "lang": "hi"
        },
        # Spanish Voices (Español)
        "elvira_spanish_female": {
            "name": "Elvira (Spanish Storyteller)",
            "gender": "Female",
            "edge_id": "es-ES-ElviraNeural",
            "eleven_id": "EXAVITQu4vr4xnSDxMaL",
            "description": "Heartfelt, evocative Spanish female voice",
            "lang": "es"
        },
        "alvaro_spanish_male": {
            "name": "Alvaro (Spanish Cinematic)",
            "gender": "Male",
            "edge_id": "es-ES-AlvaroNeural",
            "eleven_id": "TxGEqnHWrfWFTfGW9XjX",
            "description": "Vibrant, confident Spanish narrator",
            "lang": "es"
        },
        # French Voices (Français)
        "denise_french_female": {
            "name": "Denise (French Poetic)",
            "gender": "Female",
            "edge_id": "fr-FR-DeniseNeural",
            "eleven_id": "ThT5KcBeYPX3keUQqHPh",
            "description": "Soft, elegant French female storyteller",
            "lang": "fr"
        },
        "henri_french_male": {
            "name": "Henri (French Cinematic)",
            "gender": "Male",
            "edge_id": "fr-FR-HenriNeural",
            "eleven_id": "pNInz6obpgDQGcFmaJgB",
            "description": "Authoritative French cinematic narrator",
            "lang": "fr"
        },
        # German Voices (Deutsch)
        "katja_german_female": {
            "name": "Katja (German Clear)",
            "gender": "Female",
            "edge_id": "de-DE-KatjaNeural",
            "eleven_id": "AZnzlk1XvdvUeBnXmlld",
            "description": "Warm, clear German storyteller",
            "lang": "de"
        },
        "conrad_german_male": {
            "name": "Conrad (German Resonant)",
            "gender": "Male",
            "edge_id": "de-DE-ConradNeural",
            "eleven_id": "pNInz6obpgDQGcFmaJgB",
            "description": "Deep, calm German narrator",
            "lang": "de"
        },
        # Japanese Voices (日本語)
        "nanami_japanese_female": {
            "name": "Nanami (Japanese Serene)",
            "gender": "Female",
            "edge_id": "ja-JP-NanamiNeural",
            "eleven_id": "21m00Tcm4TlvDq8ikWAM",
            "description": "Gentle, atmospheric Japanese storyteller",
            "lang": "ja"
        },
        "keita_japanese_male": {
            "name": "Keita (Japanese Dynamic)",
            "gender": "Male",
            "edge_id": "ja-JP-KeitaNeural",
            "eleven_id": "TxGEqnHWrfWFTfGW9XjX",
            "description": "Inspiring, confident Japanese narrator",
            "lang": "ja"
        }
    }

    # Base Supported Avatars
    _BASE_AVATARS = {
        "female_innocent": {
            "name": "Ava",
            "gender": "Female",
            "file": "female_innocent.jpg",
            "description": "Warm, natural young woman with kind smile"
        },
        "male_innocent": {
            "name": "Lucas",
            "gender": "Male",
            "file": "male_innocent.jpg",
            "description": "Thoughtful, kind young man with sincere gaze"
        },
        "female_poetic": {
            "name": "Elena",
            "gender": "Female",
            "file": "female_poetic.jpg",
            "description": "Gentle storyteller with warm twilight glow"
        },
        "male_adventurer": {
            "name": "Leo",
            "gender": "Male",
            "file": "male_adventurer.jpg",
            "description": "Mountain explorer with courageous warm gaze"
        }
    }

    # Categories with styling, music, and voice pairings
    CATEGORIES = {
        "MOTIVATION": {
            "label": "Daily Discipline & Stoicism",
            "tagline": "MENTAL TOUGHNESS",
            "accent_hex": "#F59E0B",
            "accent_rgb": (245, 158, 11),
            "music_file": "cinematic_ambient_drone.wav",
            "default_voice": "christopher_male",
            "default_avatar": "male_innocent"
        },
        "ADVENTURE": {
            "label": "Storytelling & Adventure",
            "tagline": "UNEXPLORED REALMS",
            "accent_hex": "#10B981",
            "accent_rgb": (16, 185, 129),
            "music_file": "adventure_epic_drone.wav",
            "default_voice": "andrew_male",
            "default_avatar": "male_adventurer"
        },
        "ROMANTIC": {
            "label": "Romantic & Poetic",
            "tagline": "HEART & SOUL",
            "accent_hex": "#F43F5E",
            "accent_rgb": (244, 63, 94),
            "music_file": "romantic_warm_pad.wav",
            "default_voice": "ava_female",
            "default_avatar": "female_innocent"
        },
        "THRILLER": {
            "label": "Thriller & Suspense",
            "tagline": "THE UNSEEN TRUTH",
            "accent_hex": "#06B6D4",
            "accent_rgb": (6, 182, 212),
            "music_file": "thriller_suspense_drone.wav",
            "default_voice": "christopher_male",
            "default_avatar": "female_innocent"
        },
        "WISDOM": {
            "label": "Life Wisdom & Parables",
            "tagline": "TIMELESS TRUTHS",
            "accent_hex": "#A855F7",
            "accent_rgb": (168, 85, 247),
            "music_file": "cinematic_ambient_drone.wav",
            "default_voice": "brian_male",
            "default_avatar": "male_innocent"
        }
    }

    @classmethod
    def get_avatars(cls) -> dict:
        """Returns base avatars merged with custom user uploaded characters."""
        avatars = cls._BASE_AVATARS.copy()
        if cls.CUSTOM_AVATARS_FILE.exists():
            try:
                with open(cls.CUSTOM_AVATARS_FILE, "r", encoding="utf-8") as f:
                    custom = json.load(f)
                    avatars.update(custom)
            except Exception:
                pass
        return avatars

    @classmethod
    def save_custom_avatar(cls, avatar_id: str, avatar_data: dict):
        current = {}
        if cls.CUSTOM_AVATARS_FILE.exists():
            try:
                with open(cls.CUSTOM_AVATARS_FILE, "r", encoding="utf-8") as f:
                    current = json.load(f)
            except Exception:
                current = {}
        current[avatar_id] = avatar_data
        with open(cls.CUSTOM_AVATARS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)

    @classmethod
    def get_voices(cls) -> dict:
        """Returns base voices merged with custom user uploaded/cloned voices."""
        voices = cls._BASE_VOICES.copy()
        if cls.CUSTOM_VOICES_FILE.exists():
            try:
                with open(cls.CUSTOM_VOICES_FILE, "r", encoding="utf-8") as f:
                    custom = json.load(f)
                    voices.update(custom)
            except Exception:
                pass
        return voices

    @classmethod
    def save_custom_voice(cls, voice_id: str, voice_data: dict):
        current = {}
        if cls.CUSTOM_VOICES_FILE.exists():
            try:
                with open(cls.CUSTOM_VOICES_FILE, "r", encoding="utf-8") as f:
                    current = json.load(f)
            except Exception:
                current = {}
        current[voice_id] = voice_data
        with open(cls.CUSTOM_VOICES_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)

    @classmethod
    def ensure_dirs(cls):
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.FONTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.MUSIC_DIR.mkdir(parents=True, exist_ok=True)
        cls.AVATARS_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        cls.SFX_DIR.mkdir(parents=True, exist_ok=True)

Config.ensure_dirs()
