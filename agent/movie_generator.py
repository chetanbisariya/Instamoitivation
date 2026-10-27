import datetime
import hashlib
import json
import random
import re
import requests
from agent.config import Config

MOVIE_TEMPLATES = {
    "THRILLER": [
        {
            "title": "THE SILENT PROTOCOL",
            "logline": "A transmission received in the dead of night leads to an impossible discovery.",
            "scene1": "The rain beat against the cold glass as the {k1} appeared on the screen. It was not supposed to exist.",
            "scene2": "Deep inside the underground facility, every step echoed against the metal walls. In the center of the vault lay the {k2}, humming with a strange, forbidden pulse.",
            "scene3": "My fingers brushed the surface. A voice whispered through the radio: 'You should not have touched the {k3}.' And then the lights went black.",
            "scene_titles": ["ACT I: THE ANOMALY", "ACT II: THE VAULT", "ACT III: THE BLACKOUT"]
        },
        {
            "title": "THE WATCHER'S KEY",
            "logline": "Some doors are meant to remain closed forever.",
            "scene1": "At three in the morning, the old grandfather clock stopped. On the table lay an ancient {k1}.",
            "scene2": "Footsteps crept across the attic floorboards. The shadows stretched toward the {k2}, shifting as if they were alive.",
            "scene3": "I turned around slowly. Holding the {k3} was not a burglar. It was someone wearing my face.",
            "scene_titles": ["ACT I: THE RENDEZVOUS", "ACT II: THE ATTIC", "ACT III: THE REFLECTION"]
        },
        {
            "title": "CIPHER IN THE DARK",
            "logline": "In the city of echoes, every secret demands a price.",
            "scene1": "The static on channel four cleared for three seconds, revealing a lone {k1} abandoned on the bridge.",
            "scene2": "I sprinted through the pouring rain until I reached the safehouse, clutching the {k2} tight against my chest.",
            "scene3": "The door clicked shut behind me. A red laser dotted my chest, and the voice murmured: 'Hand over the {k3}.'",
            "scene_titles": ["ACT I: THE SIGNAL", "ACT II: THE PURSUIT", "ACT III: THE AMBUSH"]
        }
    ],
    "SCI-FI": [
        {
            "title": "ORBIT ZERO",
            "logline": "At the edge of explored space, an ancient beacon awakens.",
            "scene1": "Three million light years from Earth, the ship's sensors detected the {k1} floating in the silence of deep space.",
            "scene2": "Commander Reynolds deployed the drone. As the telemetry synchronized, the alien {k2} suddenly powered on, projecting coordinates that matched Earth.",
            "scene3": "The ship's AI began counting down: 'The {k3} is returning home.' We were never the explorers. We were the bait.",
            "scene_titles": ["ACT I: DEEP SPACE", "ACT II: THE AWAKENING", "ACT III: THE INVASION"]
        },
        {
            "title": "CHRONO DRIFT",
            "logline": "Time is not a straight line; it is a maze of shattered fragments.",
            "scene1": "The quantum drive ruptured during the jump, trapping our pod beside a giant crystalline {k1}.",
            "scene2": "My past self appeared on the exterior hull, desperately signaling with an emergency {k2}.",
            "scene3": "I pressed the override switch, only to realize the paradox: the person who triggered the {k3} was me.",
            "scene_titles": ["ACT I: THE FRACTURE", "ACT II: THE ECHO", "ACT III: THE PARADOX"]
        }
    ],
    "ADVENTURE": [
        {
            "title": "THE FORGOTTEN EXPEDITION",
            "logline": "Across frozen summits and lost canyons, truth awaits those who dare.",
            "scene1": "The map had only one marking: a faded sketch of the {k1} carved into the cliffside above the clouds.",
            "scene2": "We fought through the blizzard for fourteen days until we reached the hidden chasm. Resting on the stone altar was the {k2}.",
            "scene3": "When I raised it toward the northern star, the mountain opened. And there, frozen in ice, stood the legendary {k3}.",
            "scene_titles": ["ACT I: THE TRAIL", "ACT II: THE CHASM", "ACT III: THE SANCTUARY"]
        },
        {
            "title": "ISLAND OF ASHES",
            "logline": "Beyond the charted storms lies an island forgotten by time.",
            "scene1": "The shipwreck washed us ashore at sunrise, our only salvaged possession a gold-inlaid {k1}.",
            "scene2": "Vines parted in the jungle canopy to reveal ancient stone ruins guarded by a carved {k2}.",
            "scene3": "As the volcanic tremor shook the valley, the temple doors parted, revealing the glowing {k3}.",
            "scene_titles": ["ACT I: SHIPWRECK", "ACT II: THE RUINS", "ACT III: THE TEMPLE"]
        }
    ],
    "ROMANTIC": [
        {
            "title": "A MEMORY IN THE RAIN",
            "logline": "Some encounters are written in the stars long before we meet.",
            "scene1": "The autumn rain washed over the cobblestones. You were standing by the corner, holding that worn {k1}.",
            "scene2": "For hours, we walked through the empty city, talking about dreams, regrets, and the {k2} we thought we had lost forever.",
            "scene3": "Before the last train pulled away, you slipped the {k3} into my hand and whispered: 'Find me where the story began.'",
            "scene_titles": ["ACT I: THE CROSSING", "ACT II: THE RAINY STREETS", "ACT III: THE FAREWELL"]
        },
        {
            "title": "MIDNIGHT LETTERS",
            "logline": "Between two distant cities, two souls whispered across the silence.",
            "scene1": "In the dusty cafe in Vienna, I found a vintage postcard tucked inside an old {k1}.",
            "scene2": "Every night at twelve, another message arrived, each describing the scent of lavender and a mysterious {k2}.",
            "scene3": "When I finally turned the corner into the moonlit square, you were there, holding the promised {k3}.",
            "scene_titles": ["ACT I: THE LETTER", "ACT II: THE VOW", "ACT III: THE REUNION"]
        }
    ],
    "NOIR": [
        {
            "title": "MIDNIGHT CIPHER",
            "logline": "In the city of smoke and shadows, everyone has a price.",
            "scene1": "The smoke curled toward the ceiling fan as the dame walked into my office, dropping a bloody {k1} on the desk.",
            "scene2": "Down at the docks, the fog was thick enough to choke on. The warehouse was guarded by men armed with the {k2}.",
            "scene3": "I drew my snub-nose. 'Tell your boss,' I said, cocking the hammer, 'that the {k3} belongs to the city now.'",
            "scene_titles": ["ACT I: THE OFFICE", "ACT II: THE HARBOR", "ACT III: THE SHOOTOUT"]
        },
        {
            "title": "NEON RAIN",
            "logline": "Trust is a luxury this city traded away decades ago.",
            "scene1": "The neon sign buzzed in the alleyway outside the diner where I first intercepted the {k1}.",
            "scene2": "The detective leaned against the lamppost, tossing me a matchbox marked with the insignia of the {k2}.",
            "scene3": "'Don't look back,' she whispered. But as the sirens howled, I knew the {k3} had already sealed our fate.",
            "scene_titles": ["ACT I: THE ALLEY", "ACT II: THE INFORMANT", "ACT III: THE SIRENS"]
        }
    ]
}

def generate_short_movie_script(
    keyword1: str,
    keyword2: str,
    keyword3: str,
    genre: str = "THRILLER"
) -> dict:
    """
    Generates a 3-act short movie script based on 3 user-provided keywords.
    Uses Google Gemini API if configured, or the cinematic procedural masterclass engine.
    """
    k1 = keyword1.strip() or "Midnight"
    k2 = keyword2.strip() or "Lighthouse"
    k3 = keyword3.strip() or "Key"
    g = genre.upper() if genre.upper() in MOVIE_TEMPLATES else "THRILLER"

    # Try Gemini API if key exists
    api_key = Config.GEMINI_API_KEY
    if api_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = (
            f"You are an acclaimed Hollywood cinematic micro-movie writer. "
            f"Write a riveting 3-act short movie based around these 3 keywords:\n"
            f"Keyword 1 (Inciting Incident): '{k1}'\n"
            f"Keyword 2 (Rising Action/Tension): '{k2}'\n"
            f"Keyword 3 (Climax/Twist): '{k3}'\n"
            f"Genre: {g}\n\n"
            f"Return ONLY a JSON object with keys:\n"
            f"- 'title': 2-4 words film title\n"
            f"- 'logline': one sentence cinematic premise\n"
            f"- 'scene1': 1-2 punchy sentences introducing {k1}\n"
            f"- 'scene2': 2 sentences building suspense/conflict introducing {k2}\n"
            f"- 'scene3': 2 sentences delivering climax/twist introducing {k3}\n"
            f"- 'scene_titles': array of 3 act titles (e.g. ['ACT I: ...', 'ACT II: ...', 'ACT III: ...'])\n"
            f"- 'full_script': combined scene1 + scene2 + scene3 (under 65 words total, written for intense spoken narration)\n"
            f"- 'caption': Instagram movie premiere caption with a question and 12 hashtags."
        )
        try:
            res = requests.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseMimeType": "application/json"}},
                timeout=20
            )
            if res.status_code == 200:
                raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                movie_data = json.loads(raw_text)
                movie_data["keywords"] = [k1, k2, k3]
                movie_data["genre"] = g
                return movie_data
        except Exception as e:
            print(f"[MovieGenerator] Gemini fallback: {e}")

    # Procedural Cinema Script Engine
    templates = MOVIE_TEMPLATES.get(g, MOVIE_TEMPLATES["THRILLER"])
    seed = int(hashlib.md5(f"{k1}_{k2}_{k3}_{g}".encode()).hexdigest(), 16)
    tmpl = templates[seed % len(templates)]

    scene1 = tmpl["scene1"].replace("{k1}", k1.lower()).replace("{k2}", k2.lower()).replace("{k3}", k3.lower())
    scene2 = tmpl["scene2"].replace("{k1}", k1.lower()).replace("{k2}", k2.lower()).replace("{k3}", k3.lower())
    scene3 = tmpl["scene3"].replace("{k1}", k1.lower()).replace("{k2}", k2.lower()).replace("{k3}", k3.lower())

    full_script = f"{scene1} {scene2} {scene3}"
    hashtags = [f"#{g.lower()}", "#shortfilm", "#cinema", "#movietrailer", "#3keywords", "#storytelling", "#reels", "#fyp", "#filmmaking"]

    caption = (
        f"🎬 PREMIERE: \"{tmpl['title']}\"\n"
        f"Genre: {g} | Generated from 3 Keywords: [{k1.upper()}, {k2.upper()}, {k3.upper()}]\n\n"
        f"\"{tmpl['logline']}\"\n\n"
        f"Scene 1: {scene1}\n\n"
        f"Scene 2: {scene2}\n\n"
        f"Scene 3: {scene3}\n\n"
        f"💬 How would you survive this twist? Drop your theory in the comments!\n"
        f"🔖 Save this short movie and share it with someone who loves {g.lower()} stories.\n\n"
        f"{' '.join(hashtags)}"
    )

    return {
        "title": tmpl["title"],
        "logline": tmpl["logline"],
        "genre": g,
        "keywords": [k1, k2, k3],
        "scene1": scene1,
        "scene2": scene2,
        "scene3": scene3,
        "scene_titles": tmpl["scene_titles"],
        "full_script": full_script,
        "caption": caption,
        "hashtags": hashtags
    }

if __name__ == "__main__":
    movie = generate_short_movie_script("Midnight", "Lighthouse", "Key", "THRILLER")
    print(f"Movie Title: {movie['title']}")
    print(f"Logline: {movie['logline']}")
    print(f"Script:\n{movie['full_script']}")
