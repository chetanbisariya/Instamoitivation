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
from agent.publisher import SocialPublisher

class DailyReelAgent:
    def __init__(self):
        Config.ensure_dirs()
        self.video_engine = VideoEngine(
            width=Config.VIDEO_WIDTH,
            height=Config.VIDEO_HEIGHT,
            fps=Config.VIDEO_FPS
        )

    def run_pipeline(self, topic: str = "", custom_prompt: str = "", date_str: str = None) -> dict:
        """
        Executes complete end-to-end flow:
        1. Script & Caption generation
        2. Audio Voiceover synthesis
        3. Video Rendering
        4. Social Publishing / Queueing
        """
        if not date_str:
            date_str = datetime.date.today().isoformat()
            
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] --- Starting Daily Reel Pipeline ---")
        
        # 1. Script Generation
        print("[1/4] Generating motivational script and caption...")
        script_data = get_daily_script(date_str=date_str, topic=topic, custom_prompt=custom_prompt)
        print(f"      Topic: {script_data.get('topic')}")
        print(f"      Author: {script_data.get('author')}")
        print(f"      Hook: \"{script_data.get('hook')}\"")

        # 2. Voiceover Synthesis
        print("[2/4] Synthesizing voiceover narration...")
        voice_filename = f"voice_{timestamp_str}.mp3"
        voice_path = str(Config.OUTPUT_DIR / voice_filename)
        voice_data = VoiceSynthesizer.generate_voiceover(script_data["script"], voice_path)
        print(f"      Voice Provider: {voice_data['provider']}")
        print(f"      Duration: {voice_data['duration']:.2f} seconds ({voice_data['word_count']} words)")

        # 3. Video Rendering
        print("[3/4] Rendering 9:16 Minimalist Typographic Reel with Audio Visualizer...")
        video_filename = f"reel_{timestamp_str}.mp4"
        video_path = str(Config.OUTPUT_DIR / video_filename)
        self.video_engine.render_video(script_data, voice_data, video_path)

        # 4. Social Dispatch / Queueing
        print("[4/4] Queueing to social channels...")
        publish_result = SocialPublisher.queue_post(video_path, script_data, voice_data)
        print(f"      Publish Status: {publish_result['status']}")

        result = {
            "success": True,
            "timestamp": timestamp_str,
            "video_path": video_path,
            "video_filename": video_filename,
            "voice_data": voice_data,
            "script_data": script_data,
            "publish_result": publish_result
        }
        print(f"--- Pipeline Completed Successfully! ---")
        print(f"Output file: {video_path}\n")
        return result

    def start_scheduler(self, run_time: str = None):
        """Runs the agent as a persistent daily scheduler."""
        target_time = run_time or Config.SCHEDULE_TIME or "09:00"
        print(f"==================================================")
        print(f"  Instagram Daily Motivation Agent Active")
        print(f"  Target Run Time: {target_time} daily")
        print(f"  Output Directory: {Config.OUTPUT_DIR}")
        print(f"  Instagram Handle: {Config.INSTAGRAM_HANDLE}")
        print(f"==================================================")

        def job():
            try:
                self.run_pipeline()
            except Exception as e:
                print(f"[Scheduler Error] Pipeline failed: {e}", file=sys.stderr)

        schedule.every().day.at(target_time).do(job)

        # Print next scheduled time
        next_run = schedule.next_run()
        print(f"Next scheduled run: {next_run}")

        try:
            while True:
                schedule.run_pending()
                time.sleep(30)
        except KeyboardInterrupt:
            print("\nScheduler stopped by user.")

def main():
    parser = argparse.ArgumentParser(description="Instagram Daily Motivation Reel Agent")
    parser.add_argument("--now", action="store_true", help="Generate and process today's reel immediately")
    parser.add_argument("--schedule", type=str, nargs="?", const="", help="Run daily scheduler at specified time (default: 09:00 or .env)")
    parser.add_argument("--topic", type=str, default="", help="Custom topic override (e.g. 'FOCUS')")
    parser.add_argument("--prompt", type=str, default="", help="Custom prompt or quote text")
    args = parser.parse_args()

    agent = DailyReelAgent()

    if args.schedule is not None:
        sched_time = args.schedule if args.schedule else Config.SCHEDULE_TIME
        agent.start_scheduler(run_time=sched_time)
    else:
        # Default action: run now
        agent.run_pipeline(topic=args.topic, custom_prompt=args.prompt)

if __name__ == "__main__":
    main()
