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
    
    # Instagram & Branding
    INSTAGRAM_HANDLE = os.getenv("INSTAGRAM_HANDLE", "@stoic.discipline.daily")
    DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "MOTIVATION")
    DEFAULT_TOPIC = os.getenv("DEFAULT_TOPIC", "DAILY DISCIPLINE")
    
    # ElevenLabs TTS Settings
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")
    ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
    
    # Default Fallback Voice (Free Neural Voice)
    DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "en-US-ChristopherNeural")
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
    SCHEDULE_CATEGORY_ROTATION = os.getenv("SCHEDULE_CATEGORY_ROTATION", "true").lower() == "true"
    DEFAULT_AVATAR = os.getenv("DEFAULT_AVATAR", "female_innocent")
    SHOW_AVATAR = os.getenv("SHOW_AVATAR", "true").lower() == "true"

    # Supported Neural Voices (Female & Male)
    VOICES = {
        # Female Voices
        "ava_female": {
            "name": "Ava (Gentle & Innocent)",
            "gender": "Female",
            "edge_id": "en-US-AvaNeural",
            "eleven_id": "21m00Tcm4TlvDq8ikWAM", # Rachel
            "description": "Warm, innocent, sweet, conversational female tone"
        },
        "emma_female": {
            "name": "Emma (Expressive & Warm)",
            "gender": "Female",
            "edge_id": "en-US-EmmaNeural",
            "eleven_id": "EXAVITQu4vr4xnSDxMaL", # Bella
            "description": "Heartfelt, emotive, poetic female narrator"
        },
        "jenny_female": {
            "name": "Jenny (Crisp & Cheerful)",
            "gender": "Female",
            "edge_id": "en-US-JennyNeural",
            "eleven_id": "AZnzlk1XvdvUeBnXmlld", # Domi
            "description": "Energetic, clear, storytelling female voice"
        },
        "sonia_female": {
            "name": "Sonia (British Elegance)",
            "gender": "Female",
            "edge_id": "en-GB-SoniaNeural",
            "eleven_id": "ThT5KcBeYPX3keUQqHPh", # Dorothy
            "description": "Sophisticated, serene British female storyteller"
        },
        # Male Voices
        "brian_male": {
            "name": "Brian (Kind & Innocent)",
            "gender": "Male",
            "edge_id": "en-US-BrianNeural",
            "eleven_id": "ErXwobaYiN019PkySvjV", # Antoni
            "description": "Kind, sincere, gentle, approachable male voice"
        },
        "andrew_male": {
            "name": "Andrew (Youthful & Adventurous)",
            "gender": "Male",
            "edge_id": "en-US-AndrewNeural",
            "eleven_id": "TxGEqnHWrfWFTfGW9XjX", # Josh
            "description": "Youthful, dynamic, confident explorer"
        },
        "christopher_male": {
            "name": "Christopher (Deep & Cinematic)",
            "gender": "Male",
            "edge_id": "en-US-ChristopherNeural",
            "eleven_id": "pNInz6obpgDQGcFmaJgB", # Adam
            "description": "Authoritative, deep, grounding cinematic voice"
        },
        "ryan_male": {
            "name": "Ryan (British Storyteller)",
            "gender": "Male",
            "edge_id": "en-GB-RyanNeural",
            "eleven_id": "VR6AewLTigWG4xSOukaG", # Arnold
            "description": "Thoughtful, atmospheric British narrator"
        }
    }

    # Supported Avatars
    AVATARS = {
        "female_innocent": {
            "name": "Ava (Innocent & Kind)",
            "gender": "Female",
            "file": "female_innocent.jpg",
            "description": "Warm, natural young woman with kind smile"
        },
        "male_innocent": {
            "name": "Lucas (Innocent & Sincere)",
            "gender": "Male",
            "file": "male_innocent.jpg",
            "description": "Thoughtful, kind young man with genuine smile"
        },
        "female_poetic": {
            "name": "Elena (Poetic & Soulful)",
            "gender": "Female",
            "file": "female_poetic.jpg",
            "description": "Gentle storyteller with warm twilight glow"
        },
        "male_adventurer": {
            "name": "Leo (Adventurer & Explorer)",
            "gender": "Male",
            "file": "male_adventurer.jpg",
            "description": "Charismatic mountain explorer with warm gaze"
        }
    }

    # Categories with styling, music, and voice pairings
    CATEGORIES = {
        "MOTIVATION": {
            "label": "Daily Discipline & Stoicism",
            "tagline": "MENTAL TOUGHNESS",
            "accent_hex": "#F59E0B", # Radiant Amber Gold
            "accent_rgb": (245, 158, 11),
            "music_file": "cinematic_ambient_drone.wav",
            "default_voice": "christopher_male",
            "default_avatar": "male_innocent"
        },
        "ADVENTURE": {
            "label": "Storytelling & Adventure",
            "tagline": "UNEXPLORED REALMS",
            "accent_hex": "#10B981", # Emerald Forest
            "accent_rgb": (16, 185, 129),
            "music_file": "adventure_epic_drone.wav",
            "default_voice": "andrew_male",
            "default_avatar": "male_adventurer"
        },
        "ROMANTIC": {
            "label": "Romantic & Poetic",
            "tagline": "HEART & SOUL",
            "accent_hex": "#F43F5E", # Sunset Rose
            "accent_rgb": (244, 63, 94),
            "music_file": "romantic_warm_pad.wav",
            "default_voice": "ava_female",
            "default_avatar": "female_poetic"
        },
        "THRILLER": {
            "label": "Thriller & Suspense",
            "tagline": "THE UNSEEN TRUTH",
            "accent_hex": "#06B6D4", # Electric Cyan / Noir
            "accent_rgb": (6, 182, 212),
            "music_file": "thriller_suspense_drone.wav",
            "default_voice": "christopher_male",
            "default_avatar": "female_innocent"
        },
        "WISDOM": {
            "label": "Life Wisdom & Parables",
            "tagline": "TIMELESS TRUTHS",
            "accent_hex": "#A855F7", # Royal Violet
            "accent_rgb": (168, 85, 247),
            "music_file": "cinematic_ambient_drone.wav",
            "default_voice": "brian_male",
            "default_avatar": "male_innocent"
        }
    }

    @classmethod
    def ensure_dirs(cls):
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.FONTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.MUSIC_DIR.mkdir(parents=True, exist_ok=True)
        cls.AVATARS_DIR.mkdir(parents=True, exist_ok=True)

Config.ensure_dirs()
