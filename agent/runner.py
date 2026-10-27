import argparse
import datetime
import os
import sys
import time
from pathlib import Path
import schedule

from agent.config import Config
from agent.generator import get_daily_script
from agent.voice import VoiceSynthesizer
from agent.video_engine import VideoEngine
from agent.movie_engine import MovieEngine
from agent.movie_generator import generate_short_movie_script
from agent.publisher import SocialPublisher

class DailyReelAgent:
    def __init__(self):
        Config.ensure_dirs()
        self.video_engine = VideoEngine(
            width=Config.VIDEO_WIDTH,
            height=Config.VIDEO_HEIGHT,
            fps=Config.VIDEO_FPS
        )
        self.movie_engine = MovieEngine(
            width=Config.VIDEO_WIDTH,
            height=Config.VIDEO_HEIGHT,
            fps=Config.VIDEO_FPS
        )

    def run_pipeline(
        self,
        category: str = "",
        voice_key: str = "",
        avatar_key: str = "",
        topic: str = "",
        custom_prompt: str = "",
        date_str: str = None,
        language: str = "en"
    ) -> dict:
        """
        Executes complete multi-genre video reel pipeline:
        1. Script & Caption generation for the selected category & language
        2. Neural Voiceover synthesis (Girl / Male options, native language)
        3. 1080x1920 Reel rendering with Audio-Reactive Avatar Aura & Waveform
        4. Social Dispatch / Queueing
        """
        if not date_str:
            date_str = datetime.date.today().isoformat()

        cat = (category or Config.DEFAULT_CATEGORY).upper()
        if cat not in Config.CATEGORIES:
            cat = "MOTIVATION"
            
        cat_info = Config.CATEGORIES[cat]
        selected_voice = voice_key or cat_info.get("default_voice", "christopher_male")
        selected_avatar = avatar_key or cat_info.get("default_avatar", "female_innocent")
        if selected_avatar.lower() == "none":
            selected_avatar = ""

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] --- Starting Story Reel Pipeline ---")
        print(f"  Category: {cat} ({cat_info['label']}) | Language: {language}")
        print(f"  Voice: {selected_voice}")
        print(f"  Avatar: {selected_avatar or 'Hidden'}")

        # 1. Script Generation
        print(f"[1/4] Generating story script and caption ({language.upper()})...")
        script_data = get_daily_script(category=cat, date_str=date_str, topic=topic, custom_prompt=custom_prompt, language=language)
        print(f"      Topic: {script_data.get('topic')}")
        print(f"      Author: {script_data.get('author')}")
        print(f"      Hook: \"{script_data.get('hook')}\"")

        # 2. Voiceover Synthesis
        print("[2/4] Synthesizing voiceover narration...")
        voice_filename = f"voice_{cat.lower()}_{timestamp_str}.mp3"
        voice_path = str(Config.OUTPUT_DIR / voice_filename)
        voice_data = VoiceSynthesizer.generate_voiceover(script_data["script"], voice_path, voice_key=selected_voice)
        print(f"      Voice: {voice_data['voice_name']} ({voice_data['provider']})")
        print(f"      Duration: {voice_data['duration']:.2f} seconds ({voice_data['word_count']} words)")

        # 3. Video Rendering
        print(f"[3/4] Rendering 9:16 Reel with Avatar Aura & Audio Spectrum...")
        video_filename = f"reel_{cat.lower()}_{timestamp_str}.mp4"
        video_path = str(Config.OUTPUT_DIR / video_filename)
        self.video_engine.render_video(
            script_data=script_data,
            voice_data=voice_data,
            output_mp4=video_path,
            category=cat,
            avatar_key=selected_avatar
        )

        # 4. Social Dispatch / Queueing
        print("[4/4] Queueing to social channels...")
        publish_result = SocialPublisher.queue_post(video_path, script_data, voice_data)
        print(f"      Publish Status: {publish_result['status']}")

        result = {
            "success": True,
            "timestamp": timestamp_str,
            "video_path": video_path,
            "video_filename": video_filename,
            "category": cat,
            "language": language,
            "voice_data": voice_data,
            "avatar_key": selected_avatar,
            "script_data": script_data,
            "publish_result": publish_result
        }
        print(f"--- Pipeline Completed Successfully! ---")
        print(f"Output file: {video_path}\n")
        return result

    def create_short_movie(
        self,
        keyword1: str,
        keyword2: str,
        keyword3: str,
        genre: str = "THRILLER",
        voice_key: str = "",
        avatar_key: str = "",
        language: str = "en"
    ) -> dict:
        """
        Generates a 3-act cinematic short movie from 3 user keywords:
        - Act I: Inciting Incident (Keyword 1)
        - Act II: Rising Conflict (Keyword 2)
        - Act III: Climax / Twist (Keyword 3)
        Renders with 2.39:1 widescreen aesthetic, active keyword glow tracking, and cinema soundtrack.
        """
        k1 = keyword1.strip() or "Midnight"
        k2 = keyword2.strip() or "Lighthouse"
        k3 = keyword3.strip() or "Key"
        g = genre.upper() if genre.upper() in ["THRILLER", "SCI-FI", "ADVENTURE", "ROMANTIC", "NOIR"] else "THRILLER"
        selected_voice = voice_key or Config.DEFAULT_VOICE or "ava_female"
        selected_avatar = avatar_key or Config.DEFAULT_AVATAR or "female_innocent"
        if selected_avatar.lower() == "none":
            selected_avatar = ""

        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] --- Starting 3-Keyword Short Movie Pipeline ---")
        print(f"  Keywords: [{k1}, {k2}, {k3}] | Language: {language}")
        print(f"  Genre: {g}")
        print(f"  Voice: {selected_voice} | Avatar: {selected_avatar or 'Hidden'}")

        # 1. Generate 3-Act Script
        print(f"[1/4] Generating 3-act cinematic script and act breakdown ({language.upper()})...")
        movie_data = generate_short_movie_script(keyword1=k1, keyword2=k2, keyword3=k3, genre=g, language=language)
        print(f"      Film Title: \"{movie_data.get('title')}\"")
        print(f"      Logline: {movie_data.get('logline')}")
        print(f"      Act Breakdown: {movie_data.get('scene_titles')}")

        # 2. Voiceover Synthesis
        print("[2/4] Synthesizing cinematic voice narration...")
        voice_filename = f"movie_voice_{g.lower()}_{timestamp_str}.mp3"
        voice_path = str(Config.OUTPUT_DIR / voice_filename)
        voice_data = VoiceSynthesizer.generate_voiceover(movie_data["full_script"], voice_path, voice_key=selected_voice)
        print(f"      Voice: {voice_data['voice_name']} | Duration: {voice_data['duration']:.2f}s")

        # 3. Cinema Video Rendering
        print("[3/4] Rendering 3-Act Cinematic Short Film with Keyword Tracking...")
        video_filename = f"movie_{g.lower()}_{timestamp_str}.mp4"
        video_path = str(Config.OUTPUT_DIR / video_filename)
        self.movie_engine.render_movie(
            movie_data=movie_data,
            voice_data=voice_data,
            output_mp4=video_path,
            avatar_key=selected_avatar,
            genre=g
        )

        # 4. Social Dispatch / Queueing
        print("[4/4] Queueing short movie premiere...")
        movie_meta = {
            "category": f"MOVIE_{g}",
            "topic": f"SHORT FILM: {movie_data.get('title')}",
            "author": "AI Cinema Studio",
            "script": movie_data["full_script"],
            "caption": movie_data["caption"]
        }
        publish_result = SocialPublisher.queue_post(video_path, movie_meta, voice_data)

        result = {
            "success": True,
            "timestamp": timestamp_str,
            "video_path": video_path,
            "video_filename": video_filename,
            "genre": g,
            "keywords": [k1, k2, k3],
            "movie_data": movie_data,
            "voice_data": voice_data,
            "avatar_key": selected_avatar,
            "publish_result": publish_result
        }
        print(f"--- 3-Keyword Short Movie Complete! ---")
        print(f"Movie File: {video_path}\n")
        return result

    def start_scheduler(self, run_time: str = None, category: str = None):
        """Runs the agent as a persistent daily scheduler with automatic category rotation."""
        target_time = run_time or Config.SCHEDULE_TIME or "09:00"
        cat_list = list(Config.CATEGORIES.keys())
        
        print(f"==================================================")
        print(f"  Instagram Daily Multi-Category Reel Agent Active")
        print(f"  Target Run Time: {target_time} daily")
        print(f"  Category Mode: {'Automatic Rotation' if not category else category}")
        print(f"  Instagram Handle: {Config.INSTAGRAM_HANDLE}")
        print(f"==================================================")

        def job():
            try:
                # Deterministic day-of-week category rotation if not forced
                if not category:
                    day_idx = datetime.datetime.now().weekday()
                    rot_cat = cat_list[day_idx % len(cat_list)]
                else:
                    rot_cat = category

                print(f"[Daily Job] Triggering automatic reel for category: {rot_cat}")
                self.run_pipeline(category=rot_cat)
            except Exception as e:
                print(f"[Scheduler Error] Pipeline failed: {e}", file=sys.stderr)

        schedule.every().day.at(target_time).do(job)
        next_run = schedule.next_run()
        print(f"Next scheduled run: {next_run}")

        try:
            while True:
                schedule.run_pending()
                time.sleep(30)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user.")

def main():
    parser = argparse.ArgumentParser(description="Instagram Daily Story & Motivation Reel Agent")
    parser.add_argument("--now", action="store_true", help="Generate reel immediately")
    parser.add_argument("--category", type=str, default="", help="Category: MOTIVATION, ADVENTURE, ROMANTIC, THRILLER, WISDOM")
    parser.add_argument("--voice", type=str, default="", help="Voice: ava_female, emma_female, brian_male, andrew_male, christopher_male")
    parser.add_argument("--avatar", type=str, default="", help="Avatar: female_innocent, male_innocent, female_poetic, male_adventurer, none")
    parser.add_argument("--topic", type=str, default="", help="Custom topic override")
    parser.add_argument("--prompt", type=str, default="", help="Custom prompt or story text")
    parser.add_argument("--schedule", type=str, nargs="?", const="", help="Run daily scheduler at specified time (default: 09:00)")
    
    # 3-Keyword Short Movie flags
    parser.add_argument("--movie", action="store_true", help="Generate a 3-keyword cinematic short movie")
    parser.add_argument("--k1", type=str, default="Midnight", help="Keyword 1 (Inciting Incident)")
    parser.add_argument("--k2", type=str, default="Lighthouse", help="Keyword 2 (Rising Conflict)")
    parser.add_argument("--k3", type=str, default="Key", help="Keyword 3 (Climax / Twist)")
    parser.add_argument("--genre", type=str, default="THRILLER", help="Short movie genre: THRILLER, SCI-FI, ADVENTURE, ROMANTIC, NOIR")
    parser.add_argument("--lang", type=str, default="en", help="Language: en, hi, es, fr, de, ja")
    
    args = parser.parse_args()

    agent = DailyReelAgent()

    if args.movie:
        agent.create_short_movie(
            keyword1=args.k1,
            keyword2=args.k2,
            keyword3=args.k3,
            genre=args.genre,
            voice_key=args.voice,
            avatar_key=args.avatar,
            language=args.lang
        )
    elif args.schedule is not None:
        sched_time = args.schedule if args.schedule else Config.SCHEDULE_TIME
        agent.start_scheduler(run_time=sched_time, category=args.category)
    else:
        agent.run_pipeline(
            category=args.category,
            voice_key=args.voice,
            avatar_key=args.avatar,
            topic=args.topic,
            custom_prompt=args.prompt,
            language=args.lang
        )

if __name__ == "__main__":
    main()
