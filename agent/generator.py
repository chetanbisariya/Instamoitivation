import datetime
import hashlib
import json
import random
import requests
from agent.config import Config

# Multi-Category Database
CATEGORY_SCRIPTS = {
    "MOTIVATION": [
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
            "topic": "DAILY DISCIPLINE",
            "author": "The Iron Law",
            "hook": "Motivation is an emotion. Discipline is a decision.",
            "body": "Motivation shows up on sunny days. Discipline shows up in the freezing rain, when you are exhausted, broke, and doubt whispers in your ear. Do the work anyway.",
            "script": "Motivation is an emotion. Discipline is a decision. Motivation shows up on sunny days. Discipline shows up in the freezing rain, when you are exhausted, broke, and doubt whispers in your ear. Do the work anyway.",
            "reflection": "When your feelings say no, let your commitment say yes."
        },
        {
            "topic": "STAND FIRM",
            "author": "Marcus Aurelius",
            "hook": "Be like the cliff against which the waves continually break.",
            "body": "It stands firm, and about it the boiling waters subside into rest. Let the chaos rage around you. You remain steady, grounded, and unyielding.",
            "script": "Be like the cliff against which the waves continually break. It stands firm, and about it the boiling waters subside into rest. Let the chaos rage around you. You remain steady, grounded, and unyielding.",
            "reflection": "Calm in the storm is the greatest superpower."
        }
    ],

    "ADVENTURE": [
        {
            "topic": "INTO THE UNKNOWN",
            "author": "The Explorer's Chronicle",
            "hook": "The map ends where your courage begins.",
            "body": "We crossed the ridge just as the storm broke over the ancient valley. For centuries, they warned that no one returns from the northern peaks. But the greatest danger in life is never taking the leap.",
            "script": "The map ends where your courage begins. We crossed the ridge just as the storm broke over the ancient valley. For centuries, they warned that no one returns from the northern peaks. But the greatest danger in life is never taking the leap.",
            "reflection": "Adventure isn't outside you. It's the fire within that refuses to sit still."
        },
        {
            "topic": "THE WHISPERING CANYON",
            "author": "Wilderness Lore",
            "hook": "Deep in the canyon, the compass started spinning wildly.",
            "body": "Three days with nothing but a leather notebook and cold mountain air. You don't conquer nature. You learn to listen to its rhythm until you forget who you were in the crowded city.",
            "script": "Deep in the canyon, the compass started spinning wildly. Three days with nothing but a leather notebook and cold mountain air. You don't conquer nature. You learn to listen to its rhythm until you forget who you were in the crowded city.",
            "reflection": "Not all who wander are lost. Some are finding where they belong."
        },
        {
            "topic": "SUMMIT OF THE GODS",
            "author": "Highland Tales",
            "hook": "At nineteen thousand feet, every breath is a negotiation with destiny.",
            "body": "Your legs burn, the snow blinds your vision, and every instinct screams to turn around. Then you reach the summit. And you see the sunrise lighting up half the world.",
            "script": "At nineteen thousand feet, every breath is a negotiation with destiny. Your legs burn, the snow blinds your vision, and every instinct screams to turn around. Then you reach the summit. And you see the sunrise lighting up half the world.",
            "reflection": "The mountain does not yield. You just grow taller."
        }
    ],

    "ROMANTIC": [
        {
            "topic": "MIDNIGHT CONFESSIONS",
            "author": "Letters to the Stars",
            "hook": "I used to think soulmates were a myth made up by poets.",
            "body": "Until the moment you laughed in the quiet rain, and the entire universe suddenly made sense. Some people are not just strangers you meet. They are memories your heart was waiting to recall.",
            "script": "I used to think soulmates were a myth made up by poets. Until the moment you laughed in the quiet rain, and the entire universe suddenly made sense. Some people are not just strangers you meet. They are memories your heart was waiting to recall.",
            "reflection": "You are my favorite thought before I fall asleep."
        },
        {
            "topic": "THE UNSPOKEN TRUTH",
            "author": "Twilight Prose",
            "hook": "If love was simple, poets would have nothing left to write.",
            "body": "It is in the way you look away when you are caught staring. In the silence between our words where everything that matters is said without a single sound. Stay with me a little longer.",
            "script": "If love was simple, poets would have nothing left to write. It is in the way you look away when you are caught staring. In the silence between our words where everything that matters is said without a single sound. Stay with me a little longer.",
            "reflection": "In all the crowded rooms in the world, my eyes will always look for you."
        },
        {
            "topic": "TIMELESS CONNECTION",
            "author": "A Million Lifetimes",
            "hook": "We loved with a love that was more than love.",
            "body": "Through crowded train stations and quiet rainy mornings, you were the calm in all my storms. If I had to live a thousand lives, I would search the world to find you in every single one.",
            "script": "We loved with a love that was more than love. Through crowded train stations and quiet rainy mornings, you were the calm in all my storms. If I had to live a thousand lives, I would search the world to find you in every single one.",
            "reflection": "You will always be my once-in-a-lifetime."
        }
    ],

    "THRILLER": [
        {
            "topic": "THE 3 AM KNOCK",
            "author": "Dark Frequency",
            "hook": "The message on my phone said: Look behind you. But I live alone.",
            "body": "The front door was bolted from the inside. Then I heard the floorboards in the hallway creak. Once. Twice. And then the doorknob slowly started to turn.",
            "script": "The message on my phone said: Look behind you. But I live alone. The front door was bolted from the inside. Then I heard the floorboards in the hallway creak. Once. Twice. And then the doorknob slowly started to turn.",
            "reflection": "Some secrets don't stay buried in the dark."
        },
        {
            "topic": "THE FORBIDDEN TAPE",
            "author": "Midnight Files",
            "hook": "They told us the lighthouse had been abandoned for thirty years.",
            "body": "So why was the beacon rotating at midnight? When we stepped into the keeper's cabin, the tea on the table was still steaming. And the guestbook had tonight's date written in fresh red ink.",
            "script": "They told us the lighthouse had been abandoned for thirty years. So why was the beacon rotating at midnight? When we stepped into the keeper's cabin, the tea on the table was still steaming. And the guestbook had tonight's date written in fresh red ink.",
            "reflection": "Never look into windows when you walk through empty corridors."
        },
        {
            "topic": "VANISHED AT DAWN",
            "author": "Cold Case Mystery",
            "hook": "The security camera captured her entering the elevator. It never opened again.",
            "body": "The elevator shaft was empty. The cables were cut twenty minutes before she stepped inside. So who was holding her hand as the doors slipped shut?",
            "script": "The security camera captured her entering the elevator. It never opened again. The elevator shaft was empty. The cables were cut twenty minutes before she stepped inside. So who was holding her hand as the doors slipped shut?",
            "reflection": "Sometimes the shadows have eyes."
        }
    ],

    "WISDOM": [
        {
            "topic": "THE ART OF LETTING GO",
            "author": "Eastern Wisdom",
            "hook": "You cannot calm the ocean with your bare hands.",
            "body": "Stop fighting the waves. Drop your shoulders, breathe in the stillness, and realize that peace was never about having control. It is about letting go of what you cannot change.",
            "script": "You cannot calm the ocean with your bare hands. Stop fighting the waves. Drop your shoulders, breathe in the stillness, and realize that peace was never about having control. It is about letting go of what you cannot change.",
            "reflection": "He who masters peace inside cannot be defeated outside."
        },
        {
            "topic": "THE RIPPLE EFFECT",
            "author": "Ancient Parable",
            "hook": "A single word spoken in anger can destroy years of trust.",
            "body": "Watch your thoughts, for they become words. Watch your words, for they become actions. A peaceful mind creates an unshakeable fortress around your life.",
            "script": "A single word spoken in anger can destroy years of trust. Watch your thoughts, for they become words. Watch your words, for they become actions. A peaceful mind creates an unshakeable fortress around your life.",
            "reflection": "Kindness is the highest form of intelligence."
        }
    ]
}

CATEGORY_HASHTAGS = {
    "MOTIVATION": ["#discipline", "#stoicism", "#mindset", "#motivation", "#dailystoic", "#focus", "#selfmastery", "#grind", "#resilience", "#reels", "#fyp"],
    "ADVENTURE": ["#adventure", "#wanderlust", "#travelstory", "#wilderness", "#explorer", "#mountains", "#naturevibes", "#survival", "#expedition", "#reels", "#fyp"],
    "ROMANTIC": ["#lovequotes", "#romantic", "#soulmate", "#poetic", "#heartfelt", "#relationshipgoals", "#loveletters", "#feelings", "#deepquotes", "#reels", "#fyp"],
    "THRILLER": ["#thriller", "#mystery", "#creepy", "#suspense", "#darkstories", "#spooky", "#plotwist", "#horrorstories", "#scaryreels", "#reels", "#fyp"],
    "WISDOM": ["#wisdom", "#innerpeace", "#mindfulness", "#lifelessons", "#philosophical", "#mentalclarity", "#zen", "#calm", "#quotesdaily", "#reels", "#fyp"]
}

def generate_with_gemini(category: str = "MOTIVATION", prompt_override: str = "") -> dict | None:
    api_key = Config.GEMINI_API_KEY
    if not api_key:
        return None

    cat = category.upper() if category.upper() in Config.CATEGORIES else "MOTIVATION"
    genre_guidelines = {
        "MOTIVATION": "Focus on discipline, mental toughness, stoic philosophy, and relentless focus.",
        "ADVENTURE": "Focus on an intense, cinematic adventure story or expedition into uncharted wilderness with high stakes and rich sensory details.",
        "ROMANTIC": "Focus on deeply emotional, tender, poetic romantic prose, soul connections, and heartfelt love.",
        "THRILLER": "Focus on a gripping, atmospheric psychological thriller or mystery micro-story with an unforgettable hook and a chilling cliffhanger.",
        "WISDOM": "Focus on timeless life perspective, inner peace, and letting go of worry."
    }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    system_instruction = (
        f"You are a master storyteller for viral Instagram Reels in the {cat} genre. {genre_guidelines.get(cat, '')} "
        "Output ONLY a raw JSON object with keys: "
        "'topic' (2-3 words uppercase), 'author' (character or creator attribution), "
        "'hook' (first sentence, highly captivating hook under 12 words), "
        "'body' (2-3 sentences delivering the core story/insight, under 45 words), "
        "'script' (combined hook + body, 35-55 words total, written to be spoken naturally), "
        "'caption' (engaging Instagram caption with a question), "
        "'hashtags' (array of 12 viral hashtags)."
    )

MULTILINGUAL_SCRIPTS = {
    "hi": {
        "MOTIVATION": [
            {
                "topic": "अटूट संकल्प",
                "author": "स्वामी विवेकानंद",
                "hook": "उठो, जागो और तब तक मत रुको जब तक लक्ष्य प्राप्त न हो जाए।",
                "body": "मंज़िल उन्हीं को मिलती है जिनके सपनों में जान होती है। पंखों से कुछ नहीं होता, हौसलों से उड़ान होती है। अपने मन को वश में करो, दुनिया तुम्हारे कदमों में होगी।",
                "script": "उठो, जागो और तब तक मत रुको जब तक लक्ष्य प्राप्त न हो जाए। मंज़िल उन्हीं को मिलती है जिनके सपनों में जान होती है। पंखों से कुछ नहीं होता, हौसलों से उड़ान होती है। अपने मन को वश में करो, दुनिया तुम्हारे कदमों में होगी।",
                "reflection": "सफलता केवल उनके लिए है जो कभी हार नहीं मानते।"
            }
        ],
        "ROMANTIC": [
            {
                "topic": "खामोश मोहब्बत",
                "author": "गुलज़ार की यादें",
                "hook": "कुछ मुलाकातें लफ़्ज़ों की मोहताज नहीं होतीं।",
                "body": "जब आँखें मिलती हैं, तो खामोशी भी दास्तान बन जाती है। बारिश की बूँदों में तुम्हारी वो पुरानी मुस्कान आज भी ताज़ा है।",
                "script": "कुछ मुलाकातें लफ़्ज़ों की मोहताज नहीं होतीं। जब आँखें मिलती हैं, तो खामोशी भी दास्तान बन जाती है। बारिश की बूँदों में तुम्हारी वो पुरानी मुस्कान आज भी ताज़ा है।",
                "reflection": "सच्चा प्यार समय और दूरी से परे होता है।"
            }
        ],
        "THRILLER": [
            {
                "topic": "आधी रात का राज़",
                "author": "अनाम कथाकार",
                "hook": "रात के तीन बजे जब दरवाज़ा खटखटाया गया...",
                "body": "बाहर कोई नहीं था, सिर्फ ज़मीन पर एक पुरानी खून से सनी चाबी पड़ी थी। और फिर सीढ़ियों से किसी के कदमों की आवाज़ आने लगी।",
                "script": "रात के तीन बजे जब दरवाज़ा खटखटाया गया, बाहर कोई नहीं था, सिर्फ ज़मीन पर एक पुरानी चाबी पड़ी थी। और फिर सीढ़ियों से किसी के कदमों की आवाज़ आने लगी।",
                "reflection": "कुछ दरवाज़े कभी नहीं खोलने चाहिए।"
            }
        ],
        "ADVENTURE": [
            {
                "topic": "हिमालय का रहस्य",
                "author": "पर्वत यात्री",
                "hook": "नक्शा जहाँ खत्म होता है, असली सफ़र वहीं से शुरू होता है।",
                "body": "बर्फानी तूफ़ान के बीच हमें वो प्राचीन गुफा दिखाई दी। उस गुफा के अंदर सदियों से खोया हुआ एक सुनहरा मंदिर चमक रहा था।",
                "script": "नक्शा जहाँ खत्म होता है, असली सफ़र वहीं से शुरू होता है। बर्फानी तूफ़ान के बीच हमें वो प्राचीन गुफा दिखाई दी। उस गुफा के अंदर सदियों से खोया हुआ मंदिर चमक रहा था।",
                "reflection": "साहस ही सबसे बड़ा मार्गदर्शक है।"
            }
        ],
        "WISDOM": [
            {
                "topic": "मौन की शक्ति",
                "author": "प्राचीन उपदेश",
                "hook": "क्रोध में बोला गया एक शब्द वर्षों का विश्वास तोड़ सकता है।",
                "body": "शांत जल में ही आकाश का असली प्रतिबिंब दिखाई देता है। अपने मन को शांत रखो, हर उलझन का हल स्वयं मिल जाएगा।",
                "script": "क्रोध में बोला गया एक शब्द वर्षों का विश्वास तोड़ सकता है। शांत जल में ही आकाश का असली प्रतिबिंब दिखाई देता है। अपने मन को शांत रखो, हर उलझन का हल स्वयं मिल जाएगा।",
                "reflection": "मौन ही सबसे बड़ा उत्तर है।"
            }
        ]
    },
    "es": {
        "MOTIVATION": [
            {
                "topic": "ENFOQUE IMPARABLE",
                "author": "Marco Aurelio",
                "hook": "Tienes poder sobre tu mente, no sobre los eventos externos.",
                "body": "Reconoce esto y encontrarás una fuerza inquebrantable. La disciplina vence al talento cuando el talento no se disciplina.",
                "script": "Tienes poder sobre tu mente, no sobre los eventos externos. Reconoce esto y encontrarás una fuerza inquebrantable. La disciplina vence al talento cuando el talento no se disciplina.",
                "reflection": "El autodominio es la mayor de las victorias."
            }
        ],
        "ROMANTIC": [
            {
                "topic": "MEMORIAS BAJO LA LLUVIA",
                "author": "Prosa Nocturna",
                "hook": "Hay miradas que guardan secretos que las palabras jamás podrán explicar.",
                "body": "Caminamos por la ciudad vacía mientras la lluvia borraba nuestras dudas. Antes de partir, dejaste tu promesa en mi corazón.",
                "script": "Hay miradas que guardan secretos que las palabras jamás podrán explicar. Caminamos por la ciudad vacía mientras la lluvia borraba nuestras dudas. Antes de partir, dejaste tu promesa en mi corazón.",
                "reflection": "El amor verdadero no se olvida."
            }
        ]
    }
}

def generate_with_gemini(category: str = "MOTIVATION", prompt_override: str = "", language: str = "en") -> dict | None:
    api_key = Config.GEMINI_API_KEY
    if not api_key:
        return None

    cat = category.upper()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    lang_instruction = f"IMPORTANT: Write the story, hook, body, script, and caption completely in {language.upper()} language!" if language != "en" else ""
    system_instruction = (
        f"You are an acclaimed viral Instagram storyteller. Write a 9:16 high-retention reel script for category: {cat}.\n"
        f"{lang_instruction}\n"
        f"Return ONLY valid JSON matching this schema:\n"
        f"- 'topic': 2-4 words title in uppercase\n"
        f"- 'author': author or speaker persona\n"
        f"- 'hook': punchy opening line under 12 words\n"
        f"- 'body': 2-3 engaging storytelling sentences\n"
        f"- 'script': hook + body combined (under 50 words total)\n"
        f"- 'caption': complete Instagram caption with question and 10 hashtags\n"
        f"- 'hashtags': array of 8-12 hashtag strings."
    )

    user_prompt = prompt_override if prompt_override else f"Write a captivating {cat} micro-story for Instagram Reels in {language}."
    payload = {
        "contents": [{"parts": [{"text": f"{system_instruction}\n\nUser request: {user_prompt}"}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.85}
    }

    try:
        res = requests.post(url, json=payload, timeout=20)
        if res.status_code == 200:
            raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_text)
    except Exception as e:
        print(f"[Generator] Gemini API error: {e}")
    return None

def get_daily_script(
    category: str = "MOTIVATION",
    date_str: str = None,
    topic: str = "",
    custom_prompt: str = "",
    language: str = "en"
) -> dict:
    cat = category.upper() if category.upper() in CATEGORY_SCRIPTS else "MOTIVATION"
    lang = language.lower() if language else "en"

    if custom_prompt or (Config.GEMINI_API_KEY and random.random() > 0.4):
        ai_res = generate_with_gemini(category=cat, prompt_override=custom_prompt or topic, language=lang)
        if ai_res and "script" in ai_res:
            ai_res["category"] = cat
            if not ai_res.get("hashtags"):
                ai_res["hashtags"] = CATEGORY_HASHTAGS.get(cat, CATEGORY_HASHTAGS["MOTIVATION"])
            return ai_res

    # Check multilingual templates
    if lang in MULTILINGUAL_SCRIPTS and cat in MULTILINGUAL_SCRIPTS[lang]:
        lang_scripts = MULTILINGUAL_SCRIPTS[lang][cat]
        item = lang_scripts[0].copy()
        item["category"] = cat
        if topic: item["topic"] = topic.upper()
        hashtags = CATEGORY_HASHTAGS.get(cat, CATEGORY_HASHTAGS["MOTIVATION"])
        item["caption"] = f"{item['hook']}\n\n{item['body']}\n\n— {item['author']}\n\n{' '.join(hashtags)}"
        item["hashtags"] = hashtags
        return item

    if not date_str:
        date_str = datetime.date.today().isoformat()

    scripts = CATEGORY_SCRIPTS.get(cat, CATEGORY_SCRIPTS["MOTIVATION"])
    seed = int(hashlib.md5(f"{date_str}_{cat}".encode()).hexdigest(), 16)
    idx = seed % len(scripts)
    item = scripts[idx].copy()
    item["category"] = cat

    if topic:
        item["topic"] = topic.upper()

    hashtags = CATEGORY_HASHTAGS.get(cat, CATEGORY_HASHTAGS["MOTIVATION"])
    caption = (
        f"{item['hook']}\n\n"
        f"{item['body']}\n\n"
        f"— {item['author']}\n\n"
        f"💬 What does this bring to mind for you? Drop a comment.\n"
        f"🔖 Save this reel to listen again tonight.\n\n"
        f"Follow {Config.INSTAGRAM_HANDLE} for daily {cat.lower()} stories.\n\n"
        f"{' '.join(hashtags)}"
    )
    item["caption"] = caption
    item["hashtags"] = hashtags
    return item

if __name__ == "__main__":
    for cat in ["ADVENTURE", "ROMANTIC", "THRILLER"]:
        s = get_daily_script(category=cat)
        print(f"\n--- {cat} Sample ---")
        print("Topic:", s["topic"])
        print("Hook:", s["hook"])
        print("Script:", s["script"])
