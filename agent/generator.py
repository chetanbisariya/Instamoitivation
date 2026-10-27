import datetime
import hashlib
import json
import random
import requests
from agent.config import Config

CURATED_SCRIPTS = [
    {
        "topic": "RELENTLESS FOCUS",
        "author": "Marcus Aurelius",
        "hook": "You have power over your mind, not outside events.",
        "body": "Realize this, and you will find unbreakable strength. Stop asking what the world can give you. Demand from yourself what you were born to build.",
        "script": "You have power over your mind, not outside events. Realize this, and you will find unbreakable strength. Stop asking what the world can give you. Demand from yourself what you were born to build.",
        "reflection": "True freedom is being master of your own thoughts."
    },
    {
        "topic": "THE POWER OF SILENCE",
        "author": "Miyamoto Musashi",
        "hook": "Do not speak of what you intend to do.",
        "body": "Do it in silence. Let your discipline be your weapon and let your results make the noise. The warrior never shouts when the sword can strike true.",
        "script": "Do not speak of what you intend to do. Do it in silence. Let your discipline be your weapon and let your results make the noise. The warrior never shouts when the sword can strike true.",
        "reflection": "Move in silence. Only speak when it is time to say checkmate."
    },
    {
        "topic": "EMBRACE THE HARD PATH",
        "author": "Seneca",
        "hook": "Difficulties strengthen the mind, as labor does the body.",
        "body": "The comfortable road leads to weakness and regret. Choose the resistance. Run toward what you fear, for on the other side of struggle lies who you are meant to become.",
        "script": "Difficulties strengthen the mind, as labor does the body. The comfortable road leads to weakness and regret. Choose the resistance. Run toward what you fear, for on the other side of struggle lies who you are meant to become.",
        "reflection": "A gem cannot be polished without friction, nor a man perfected without trials."
    },
    {
        "topic": "DAILY DISCIPLINE",
        "author": "Daily Stoic",
        "hook": "Motivation is an emotion. Discipline is a decision.",
        "body": "Motivation shows up on sunny days. Discipline shows up in the freezing rain, when you are exhausted, broke, and doubt whispers in your ear. Do the work anyway.",
        "script": "Motivation is an emotion. Discipline is a decision. Motivation shows up on sunny days. Discipline shows up in the freezing rain, when you are exhausted, broke, and doubt whispers in your ear. Do the work anyway.",
        "reflection": "When your feelings say no, let your commitment say yes."
    },
    {
        "topic": "UNSHAKABLE MIND",
        "author": "Epictetus",
        "hook": "He is a wise man who does not grieve for things he has not.",
        "body": "Instead, he rejoices for what he has. No man is free who is not master of himself. Control your impulses, quiet your complaints, and take command of your life.",
        "script": "He is a wise man who does not grieve for things he has not. Instead, he rejoices for what he has. No man is free who is not master of himself. Control your impulses, quiet your complaints, and take command of your life.",
        "reflection": "Mastery of self is the only empire worth conquering."
    },
    {
        "topic": "OVERCOMING PROCRASTINATION",
        "author": "The Iron Law",
        "hook": "Tomorrow is the graveyard of great intentions.",
        "body": "Every excuse you make today is a debt your future self has to repay with tears. Kill the doubt. Stop waiting for the perfect moment. Take the first step now.",
        "script": "Tomorrow is the graveyard of great intentions. Every excuse you make today is a debt your future self has to repay with tears. Kill the doubt. Stop waiting for the perfect moment. Take the first step now.",
        "reflection": "One day or Day One. You decide."
    },
    {
        "topic": "RADICAL ACCOUNTABILITY",
        "author": "Stoic Creed",
        "hook": "No one is coming to save you.",
        "body": "Not your friends, not your government, not luck. You hold the pen to your own story. Take absolute ownership of your errors and rise higher tomorrow.",
        "script": "No one is coming to save you. Not your friends, not your government, not luck. You hold the pen to your own story. Take absolute ownership of your errors and rise higher tomorrow.",
        "reflection": "Total responsibility equals total freedom."
    },
    {
        "topic": "STAND FIRM",
        "author": "Marcus Aurelius",
        "hook": "Be like the cliff against which the waves continually break.",
        "body": "It stands firm, and about it the boiling waters subside into rest. Let the chaos rage around you. You remain steady, grounded, and unyielding.",
        "script": "Be like the cliff against which the waves continually break. It stands firm, and about it the boiling waters subside into rest. Let the chaos rage around you. You remain steady, grounded, and unyielding.",
        "reflection": "Calm in the storm is the greatest superpower."
    },
    {
        "topic": "EARLY RISER",
        "author": "The Morning Code",
        "hook": "While the world sleeps, destinies are shaped.",
        "body": "The dawn belongs to the hungry. Win the first hour of your day and you win the battle for your mind. Rise early. Breathe the cold air. Conquer your craft.",
        "script": "While the world sleeps, destinies are shaped. The dawn belongs to the hungry. Win the first hour of your day and you win the battle for your mind. Rise early. Breathe the cold air. Conquer your craft.",
        "reflection": "Victory begins before sunrise."
    },
    {
        "topic": "FORGE YOUR LEGACY",
        "author": "Ancient Wisdom",
        "hook": "We suffer more often in imagination than in reality.",
        "body": "Stop tormenting yourself with what could go wrong. Focus solely on what you can build right now. Courage is not the absence of fear, but the triumph over it.",
        "script": "We suffer more often in imagination than in reality. Stop tormenting yourself with what could go wrong. Focus solely on what you can build right now. Courage is not the absence of fear, but the triumph over it.",
        "reflection": "Fear is temporary. Regret lasts forever."
    }
]

DEFAULT_HASHTAGS = [
    "#discipline", "#stoicism", "#mindset", "#motivation", "#dailystoic",
    "#focus", "#selfmastery", "#marcusaurelius", "#resilience", "#grindset",
    "#mentalstrength", "#motivationalquotes", "#successmindset", "#consistency",
    "#innerpeace", "#wisdom", "#quotesdaily", "#reels", "#fyp"
]

def generate_with_gemini(topic: str = "", prompt_override: str = "") -> dict | None:
    """Uses Gemini API to generate an original motivational script and caption."""
    api_key = Config.GEMINI_API_KEY
    if not api_key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    system_instruction = (
        "You are an expert viral content creator for Instagram Reels specializing in stoicism, mental toughness, and daily discipline. "
        "Output ONLY a raw JSON object with keys: 'topic' (2-3 words uppercase), 'author' (historical figure or 'Stoic Wisdom'), "
        "'hook' (punchy opening sentence, 6-10 words), 'body' (2 sentences delivering deep wisdom), "
        "'script' (combined hook + body, 30-50 words total, written for spoken voice), "
        "'caption' (engaging Instagram caption with a reflective question), "
        "'hashtags' (array of 15 relevant hashtags)."
    )
    user_prompt = prompt_override if prompt_override else f"Topic theme: {topic or 'Relentless discipline and mental toughness'}. Make it unforgettable and cinematic."
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_instruction}\n\nTask: {user_prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.8
        }
    }
    
    try:
        res = requests.post(url, json=payload, timeout=20)
        if res.status_code == 200:
            data = res.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text)
            return parsed
    except Exception as e:
        print(f"[Generator] Gemini API error, falling back to curated library: {e}")
    return None

def get_daily_script(date_str: str = None, topic: str = "", custom_prompt: str = "") -> dict:
    """Returns a motivational script either via Gemini AI or curated rotation."""
    # Try Gemini if key is provided or custom prompt requested
    if custom_prompt or (Config.GEMINI_API_KEY and random.random() > 0.3):
        gemini_result = generate_with_gemini(topic=topic, prompt_override=custom_prompt)
        if gemini_result and "script" in gemini_result:
            if "hashtags" not in gemini_result or not gemini_result["hashtags"]:
                gemini_result["hashtags"] = DEFAULT_HASHTAGS
            if "caption" not in gemini_result:
                gemini_result["caption"] = f"{gemini_result['script']}\n\nSave this reel to remind yourself of this truth."
            return gemini_result
            
    # Deterministic daily rotation using hash of date
    if not date_str:
        date_str = datetime.date.today().isoformat()
        
    seed = int(hashlib.md5(date_str.encode()).hexdigest(), 16)
    idx = seed % len(CURATED_SCRIPTS)
    item = CURATED_SCRIPTS[idx].copy()
    
    if topic:
        item["topic"] = topic.upper()
        
    caption = (
        f"{item['hook']}\n\n"
        f"{item['body']}\n\n"
        f"— {item['author']}\n\n"
        f"💬 What area of your life demands this focus today?\n"
        f"🔖 Save this reel and review it whenever weakness whispers in your mind.\n\n"
        f"Follow {Config.INSTAGRAM_HANDLE} for your daily reminder of strength.\n\n"
        f"{' '.join(DEFAULT_HASHTAGS)}"
    )
    item["caption"] = caption
    item["hashtags"] = DEFAULT_HASHTAGS
    return item

if __name__ == "__main__":
    script = get_daily_script()
    print("Generated Script for Today:")
    print(json.dumps(script, indent=2))
