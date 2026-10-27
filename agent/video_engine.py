import math
import os
import subprocess
import time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
from agent.config import Config
from agent.visualizer import AudioSpectrumVisualizer

class VideoEngine:
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.fonts = self._load_fonts()
        self.bg_base = self._create_base_background()

    def _load_fonts(self) -> dict:
        """Loads bundled modern typography with safe fallbacks."""
        anton_path = Config.FONTS_DIR / "Anton-Regular.ttf"
        inter_path = Config.FONTS_DIR / "Inter-Variable.ttf"
        
        fonts = {}
        try:
            fonts["badge"] = ImageFont.truetype(str(inter_path), 28)
            fonts["quote_large"] = ImageFont.truetype(str(anton_path), 66)
            fonts["quote_medium"] = ImageFont.truetype(str(anton_path), 54)
            fonts["author"] = ImageFont.truetype(str(inter_path), 32)
            fonts["handle"] = ImageFont.truetype(str(inter_path), 28)
            fonts["small"] = ImageFont.truetype(str(inter_path), 22)
        except Exception as e:
            print(f"[VideoEngine] Font load error: {e}. Using PIL default.")
            default_font = ImageFont.load_default()
            fonts = {k: default_font for k in ["badge", "quote_large", "quote_medium", "author", "handle", "small"]}
        return fonts

    def _create_base_background(self) -> Image.Image:
        """Creates a sleek, dark-slate background with subtle radial glow and vignette."""
        img = Image.new("RGB", (self.width, self.height), (10, 11, 15))
        draw = ImageDraw.Draw(img)

        # Subtle dark vertical gradient
        for y in range(0, self.height, 4):
            factor = y / self.height
            # Top: (8, 9, 13) -> Bottom: (14, 16, 22)
            r = int(8 + factor * 6)
            g = int(9 + factor * 7)
            b = int(13 + factor * 9)
            draw.rectangle([0, y, self.width, y + 4], fill=(r, g, b))

        # Radial soft ambient glow in the upper-mid area (behind quote)
        glow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        center_x, center_y = self.width // 2, int(self.height * 0.42)
        max_r = 500

        for r in range(max_r, 0, -25):
            alpha = int((1.0 - (r / max_r) ** 1.5) * 28)
            glow_draw.ellipse(
                [center_x - r, center_y - r * 0.8, center_x + r, center_y + r * 0.8],
                fill=(45, 52, 70, alpha)
            )
            
        glow = glow.filter(ImageFilter.GaussianBlur(radius=30))
        img.paste(glow, (0, 0), glow)

        # Subtle aesthetic border accent lines & corner markers
        draw = ImageDraw.Draw(img)
        border_col = (40, 45, 58)
        
        # Subtle crosshairs in 4 corners
        cs = 16
        for (cx, cy) in [(90, 120), (self.width - 90, 120), (90, self.height - 120), (self.width - 90, self.height - 120)]:
            draw.line([(cx - cs, cy), (cx + cs, cy)], fill=border_col, width=2)
            draw.line([(cx, cy - cs), (cx, cy + cs)], fill=border_col, width=2)

        return img

    def _wrap_text_to_lines(self, words: list[str], font: ImageFont.ImageFont, max_width: int) -> list[list[str]]:
        """Splits words into lines that fit within max_width."""
        lines = []
        current_line = []
        dummy_img = Image.new("RGB", (10, 10))
        draw = ImageDraw.Draw(dummy_img)

        for word in words:
            test_line = current_line + [word]
            test_str = " ".join(test_line)
            bbox = draw.textbbox((0, 0), test_str, font=font)
            line_w = bbox[2] - bbox[0]
            if line_w <= max_width or not current_line:
                current_line.append(word)
            else:
                lines.append(current_line)
                current_line = [word]

        if current_line:
            lines.append(current_line)
        return lines

    def render_frame(
        self,
        frame_idx: int,
        total_frames: int,
        current_time: float,
        topic: str,
        author: str,
        word_lines: list[list[str]],
        word_timings_dict: dict,
        visualizer_bars: np.ndarray,
        quote_font: ImageFont.ImageFont,
        line_height: int,
        total_text_height: int
    ) -> Image.Image:
        """Renders an individual 1080x1920 video frame with kinetic typography & waveform."""
        frame = self.bg_base.copy()
        draw = ImageDraw.Draw(frame)

        # 1. Top Topic Badge
        badge_text = f"•  {topic.upper()}  •"
        badge_font = self.fonts["badge"]
        b_box = draw.textbbox((0, 0), badge_text, font=badge_font)
        bw, bh = b_box[2] - b_box[0], b_box[3] - b_box[1]
        badge_cx = self.width // 2
        badge_cy = 230
        pad_x, pad_y = 28, 12
        badge_rect = [badge_cx - bw // 2 - pad_x, badge_cy - pad_y, badge_cx + bw // 2 + pad_x, badge_cy + bh + pad_y]
        
        # Pill background and border
        draw.rounded_rectangle(badge_rect, radius=24, fill=(24, 28, 38), outline=(60, 70, 90), width=2)
        # Gold accent dot inside badge
        draw.text((badge_cx - bw // 2, badge_cy), badge_text, font=badge_font, fill=(215, 222, 235))

        # 2. Hero Kinetic Typography (Word-by-word active glow)
        start_y = 420 + max(0, (550 - total_text_height) // 2)
        y = start_y

        for line_words in word_lines:
            # Measure full line width to center it
            full_line_str = " ".join(line_words)
            l_box = draw.textbbox((0, 0), full_line_str, font=quote_font)
            line_w = l_box[2] - l_box[0]
            x = (self.width - line_w) // 2

            for word in line_words:
                w_box = draw.textbbox((0, 0), word, font=quote_font)
                ww = w_box[2] - w_box[0]

                timing = word_timings_dict.get(word.lower(), None)
                is_active = False
                is_past = False

                if timing:
                    w_start = timing["start"]
                    w_end = timing["end"]
                    if current_time >= w_start and current_time < w_end:
                        is_active = True
                    elif current_time >= w_end:
                        is_past = True
                else:
                    is_past = True

                # Determine color and glow
                if is_active:
                    # Pulsing warm gold highlight (#F59E0B) with soft glow
                    fill_color = (255, 204, 38)
                    # Word glow shadow
                    draw.text((x + 1, y + 1), word, font=quote_font, fill=(180, 100, 10))
                    draw.text((x, y), word, font=quote_font, fill=fill_color)
                elif is_past:
                    # Clean crisp high-contrast white
                    fill_color = (248, 250, 252)
                    draw.text((x, y), word, font=quote_font, fill=fill_color)
                else:
                    # Unspoken upcoming words: sleek muted charcoal
                    fill_color = (78, 88, 106)
                    draw.text((x, y), word, font=quote_font, fill=fill_color)

                space_box = draw.textbbox((0, 0), " ", font=quote_font)
                sw = space_box[2] - space_box[0]
                x += ww + sw

            y += line_height

        # 3. Dynamic Waveform Visualizer
        viz_center_y = 1240
        num_bars = len(visualizer_bars)
        bar_w = 9
        bar_gap = 6
        total_viz_w = num_bars * bar_w + (num_bars - 1) * bar_gap
        viz_start_x = (self.width - total_viz_w) // 2

        # Draw visualizer baseline glow
        for i, val in enumerate(visualizer_bars):
            bx = viz_start_x + i * (bar_w + bar_gap)
            # Minimum idle height: 12px, peak: 140px
            bar_h = int(12 + val * 128)
            by1 = viz_center_y - bar_h // 2
            by2 = viz_center_y + bar_h // 2

            # Color gradient: Center bars are golden (#F59E0B), edge bars are bright white/cyan
            dist_from_center = abs(i - num_bars / 2) / (num_bars / 2)
            # Interpolate (245, 158, 11) to (230, 240, 255)
            r = int(245 * (1 - dist_from_center) + 230 * dist_from_center)
            g = int(158 * (1 - dist_from_center) + 240 * dist_from_center)
            b = int(11 * (1 - dist_from_center) + 255 * dist_from_center)

            draw.rounded_rectangle([bx, by1, bx + bar_w, by2], radius=4, fill=(r, g, b))

        # 4. Author Attribution
        author_text = f"—  {author.upper()}  —"
        author_font = self.fonts["author"]
        a_box = draw.textbbox((0, 0), author_text, font=author_font)
        aw = a_box[2] - a_box[0]
        draw.text(((self.width - aw) // 2, 1400), author_text, font=author_font, fill=(156, 168, 188))

        # 5. Handle Branding & Social Cue
        handle_text = Config.INSTAGRAM_HANDLE
        h_font = self.fonts["handle"]
        h_box = draw.textbbox((0, 0), handle_text, font=h_font)
        hw = h_box[2] - h_box[0]
        draw.text(((self.width - hw) // 2, 1680), handle_text, font=h_font, fill=(100, 116, 139))

        reminder_text = "SAVE THIS REEL • DAILY DISCIPLINE"
        rem_font = self.fonts["small"]
        r_box = draw.textbbox((0, 0), reminder_text, font=rem_font)
        rw = r_box[2] - r_box[0]
        draw.text(((self.width - rw) // 2, 1726), reminder_text, font=rem_font, fill=(71, 85, 105))

        # 6. Sleek Bottom Progress Bar
        progress = frame_idx / max(total_frames - 1, 1)
        bar_len = int(self.width * progress)
        if bar_len > 0:
            draw.rectangle([0, self.height - 8, bar_len, self.height], fill=(245, 158, 11))

        return frame

    def render_video(
        self,
        script_data: dict,
        voice_data: dict,
        output_mp4: str,
        bg_music_path: str = None
    ) -> str:
        """
        Renders complete 1080x1920 MP4 video directly via ffmpeg stdin pipe.
        """
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        audio_file = voice_data["audio_path"]
        duration = voice_data["duration"]
        word_timings = voice_data.get("word_timings", [])
        total_frames = int(duration * self.fps)

        # Map word timing list to dictionary for O(1) lookup
        word_timings_dict = {}
        for wt in word_timings:
            clean_w = wt["word"].lower().strip(".,!?;:\"'")
            word_timings_dict[clean_w] = wt

        # Precompute visualizer bars
        visualizer = AudioSpectrumVisualizer(audio_file, num_bars=42, fps=self.fps)

        # Typography layout
        words = script_data["script"].split()
        quote_font = self.fonts["quote_large"] if len(words) <= 22 else self.fonts["quote_medium"]
        max_text_width = 860
        word_lines = self._wrap_text_to_lines(words, quote_font, max_text_width)
        
        # Calculate line height and total block height
        dummy = Image.new("RGB", (10, 10))
        d_draw = ImageDraw.Draw(dummy)
        sample_box = d_draw.textbbox((0, 0), "Aj", font=quote_font)
        line_height = int((sample_box[3] - sample_box[1]) * 1.35)
        total_text_height = len(word_lines) * line_height

        print(f"[VideoEngine] Rendering {total_frames} frames ({duration:.2f}s) to {output_mp4}...")
        start_t = time.time()

        # Background music setup
        bg_music = bg_music_path or str(Config.MUSIC_DIR / "cinematic_ambient_drone.wav")
        has_bg_music = os.path.exists(bg_music)

        # Build FFmpeg command with complex audio filter to mix voice + background music
        if has_bg_music:
            # Voice (0:a) + Ambient Drone (1:a) mixed with low volume for ambient music
            music_vol = Config.BACKGROUND_MUSIC_VOLUME
            ffmpeg_cmd = [
                ffmpeg_exe, "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{self.width}x{self.height}",
                "-pix_fmt", "rgb24",
                "-r", str(self.fps),
                "-i", "-",  # Video frames from stdin
                "-i", audio_file,  # Voiceover
                "-stream_loop", "-1", "-i", bg_music,  # Looping background music
                "-filter_complex",
                f"[2:a]volume={music_vol}[bg];[1:a][bg]amix=inputs=2:duration=first:dropout_transition=2[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "21",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_mp4
            ]
        else:
            ffmpeg_cmd = [
                ffmpeg_exe, "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{self.width}x{self.height}",
                "-pix_fmt", "rgb24",
                "-r", str(self.fps),
                "-i", "-",
                "-i", audio_file,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "21",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output_mp4
            ]

        proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        for frame_idx in range(total_frames):
            cur_time = frame_idx / self.fps
            bars = visualizer.get_bars_for_frame(frame_idx)

            frame_img = self.render_frame(
                frame_idx=frame_idx,
                total_frames=total_frames,
                current_time=cur_time,
                topic=script_data.get("topic", "DAILY DISCIPLINE"),
                author=script_data.get("author", "Marcus Aurelius"),
                word_lines=word_lines,
                word_timings_dict=word_timings_dict,
                visualizer_bars=bars,
                quote_font=quote_font,
                line_height=line_height,
                total_text_height=total_text_height
            )

            # Write raw RGB bytes to ffmpeg stdin pipe
            proc.stdin.write(frame_img.tobytes())

        proc.stdin.close()
        stderr_output = proc.stderr.read()
        proc.wait()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg encoding failed: {stderr_output.decode('utf-8', errors='ignore')}")

        elapsed = time.time() - start_t
        fps_rendered = total_frames / max(elapsed, 0.001)
        print(f"[VideoEngine] Render finished in {elapsed:.1f}s ({fps_rendered:.1f} fps). Output: {output_mp4}")
        return output_mp4

if __name__ == "__main__":
    from agent.generator import get_daily_script
    from agent.voice import VoiceSynthesizer
    
    script = get_daily_script()
    test_voice_file = str(Config.OUTPUT_DIR / "sample_voice.mp3")
    v_data = VoiceSynthesizer.generate_voiceover(script["script"], test_voice_file)
    
    engine = VideoEngine()
    test_out = str(Config.OUTPUT_DIR / "sample_reel.mp4")
    engine.render_video(script, v_data, test_out)
    print("Video rendered successfully!")
