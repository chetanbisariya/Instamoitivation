import math
import os
import subprocess
import time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
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
        self.avatar_cache = self._preload_avatars()

    def _load_fonts(self) -> dict:
        anton_path = Config.FONTS_DIR / "Anton-Regular.ttf"
        inter_path = Config.FONTS_DIR / "Inter-Variable.ttf"
        
        fonts = {}
        try:
            fonts["badge"] = ImageFont.truetype(str(inter_path), 25)
            fonts["quote_large"] = ImageFont.truetype(str(anton_path), 66)
            fonts["quote_medium"] = ImageFont.truetype(str(anton_path), 54)
            fonts["author"] = ImageFont.truetype(str(inter_path), 32)
            fonts["handle"] = ImageFont.truetype(str(inter_path), 28)
            fonts["small"] = ImageFont.truetype(str(inter_path), 22)
            fonts["speaker_name"] = ImageFont.truetype(str(inter_path), 22)
        except Exception as e:
            print(f"[VideoEngine] Font load error: {e}. Using PIL default.")
            default_font = ImageFont.load_default()
            fonts = {k: default_font for k in ["badge", "quote_large", "quote_medium", "author", "handle", "small", "speaker_name"]}
        return fonts

    def _preload_avatars(self) -> dict:
        """Preloads and circularly crops all avatar portraits including custom uploads."""
        avatars = {}
        size = (150, 150)
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)

        all_avatars = Config.get_avatars()
        for av_key, av_info in all_avatars.items():
            av_path = Config.AVATARS_DIR / av_info["file"]
            if av_path.exists():
                try:
                    img = Image.open(av_path).convert("RGBA")
                    img = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)
                    img.putalpha(mask)
                    avatars[av_key] = img
                except Exception as e:
                    print(f"[VideoEngine] Error loading avatar {av_key}: {e}")
        return avatars

    def get_avatar_image(self, avatar_key: str) -> Image.Image | None:
        """Dynamically retrieves avatar, loading newly uploaded ones if not yet cached."""
        if not avatar_key or avatar_key.lower() == "none":
            return None
        if avatar_key not in self.avatar_cache:
            self.avatar_cache = self._preload_avatars()
        return self.avatar_cache.get(avatar_key, None)

    def _create_base_background(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (10, 11, 15))
        draw = ImageDraw.Draw(img)

        # Subtle dark vertical gradient
        for y in range(0, self.height, 4):
            factor = y / self.height
            r = int(8 + factor * 6)
            g = int(9 + factor * 7)
            b = int(13 + factor * 9)
            draw.rectangle([0, y, self.width, y + 4], fill=(r, g, b))

        # Corner crosshairs
        cs = 16
        border_col = (40, 45, 58)
        for (cx, cy) in [(90, 120), (self.width - 90, 120), (90, self.height - 120), (self.width - 90, self.height - 120)]:
            draw.line([(cx - cs, cy), (cx + cs, cy)], fill=border_col, width=2)
            draw.line([(cx, cy - cs), (cx, cy + cs)], fill=border_col, width=2)

        return img

    def _wrap_text_to_lines(self, words: list[str], font: ImageFont.ImageFont, max_width: int) -> list[list[str]]:
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
        category: str,
        avatar_key: str,
        word_lines: list[list[str]],
        word_timings_dict: dict,
        visualizer_bars: np.ndarray,
        quote_font: ImageFont.ImageFont,
        line_height: int,
        total_text_height: int
    ) -> Image.Image:
        frame = self.bg_base.copy()
        draw = ImageDraw.Draw(frame)

        cat_info = Config.CATEGORIES.get(category, Config.CATEGORIES["MOTIVATION"])
        accent_rgb = cat_info["accent_rgb"]
        avg_energy = float(np.mean(visualizer_bars)) if len(visualizer_bars) > 0 else 0.0

        # Dynamic ambient center glow
        center_x, center_y = self.width // 2, int(self.height * 0.46)
        glow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        max_r = 480
        for r in range(max_r, 0, -30):
            alpha = int((1.0 - (r / max_r) ** 1.5) * 22)
            glow_draw.ellipse(
                [center_x - r, center_y - r * 0.75, center_x + r, center_y + r * 0.75],
                fill=(accent_rgb[0] // 3, accent_rgb[1] // 3, accent_rgb[2] // 3, alpha)
            )
        glow = glow.filter(ImageFilter.GaussianBlur(radius=25))
        frame.paste(glow, (0, 0), glow)

        # 1. Narrator Avatar (Center-Top with Audio-Reactive Pulsing Aura)
        avatar_img = self.get_avatar_image(avatar_key)
        show_avatar = avatar_img is not None and Config.SHOW_AVATAR
        
        all_avatars = Config.get_avatars()
        character_name = all_avatars.get(avatar_key, {}).get("name", "Storyteller") if avatar_key else "Storyteller"

        if show_avatar:
            av_cx, av_cy = self.width // 2, 220
            av_radius = 75
            
            # Draw Audio-Reactive Glowing Aura Ring
            pulse_extra = int(avg_energy * 20)
            aura_radius = av_radius + 6 + pulse_extra
            aura_layer = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
            aura_draw = ImageDraw.Draw(aura_layer)
            
            aura_alpha = int(95 + avg_energy * 145)
            aura_draw.ellipse(
                [av_cx - aura_radius, av_cy - aura_radius, av_cx + aura_radius, av_cy + aura_radius],
                fill=(accent_rgb[0], accent_rgb[1], accent_rgb[2], aura_alpha)
            )
            aura_layer = aura_layer.filter(ImageFilter.GaussianBlur(radius=10))
            frame.paste(aura_layer, (0, 0), aura_layer)

            # Circular Avatar Portrait
            av_x = av_cx - av_radius
            av_y = av_cy - av_radius
            frame.paste(avatar_img, (av_x, av_y), avatar_img)

            # Crisp border ring
            draw.ellipse([av_x - 1, av_y - 1, av_x + 151, av_y + 151], outline=accent_rgb, width=3)

            # Narrator Tag below Avatar
            badge_cy = 330
            badge_text = f"•  {character_name.upper()} • {topic.upper()}  •"
        else:
            badge_cy = 230
            cat_tagline = cat_info.get("tagline", category)
            badge_text = f"•  {cat_tagline} : {topic.upper()}  •"

        # 2. Topic / Character Badge
        badge_font = self.fonts["badge"]
        b_box = draw.textbbox((0, 0), badge_text, font=badge_font)
        bw, bh = b_box[2] - b_box[0], b_box[3] - b_box[1]
        badge_cx = self.width // 2
        pad_x, pad_y = 26, 10
        badge_rect = [badge_cx - bw // 2 - pad_x, badge_cy - pad_y, badge_cx + bw // 2 + pad_x, badge_cy + bh + pad_y]
        
        draw.rounded_rectangle(badge_rect, radius=22, fill=(22, 26, 36), outline=(50, 60, 80), width=2)
        draw.text((badge_cx - bw // 2, badge_cy), badge_text, font=badge_font, fill=(225, 232, 245))

        # 3. Hero Kinetic Typography
        quote_start_y = 440 if show_avatar else 420
        start_y = quote_start_y + max(0, (520 - total_text_height) // 2)
        y = start_y

        for line_words in word_lines:
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

                if is_active:
                    fill_color = accent_rgb
                    draw.text((x + 2, y + 2), word, font=quote_font, fill=(accent_rgb[0] // 3, accent_rgb[1] // 3, accent_rgb[2] // 3))
                    draw.text((x, y), word, font=quote_font, fill=fill_color)
                elif is_past:
                    fill_color = (248, 250, 252)
                    draw.text((x, y), word, font=quote_font, fill=fill_color)
                else:
                    fill_color = (78, 88, 106)
                    draw.text((x, y), word, font=quote_font, fill=fill_color)

                space_box = draw.textbbox((0, 0), " ", font=quote_font)
                sw = space_box[2] - space_box[0]
                x += ww + sw

            y += line_height

        # 4. Dynamic Waveform Visualizer
        viz_center_y = 1250
        num_bars = len(visualizer_bars)
        bar_w = 9
        bar_gap = 6
        total_viz_w = num_bars * bar_w + (num_bars - 1) * bar_gap
        viz_start_x = (self.width - total_viz_w) // 2

        for i, val in enumerate(visualizer_bars):
            bx = viz_start_x + i * (bar_w + bar_gap)
            bar_h = int(12 + val * 126)
            by1 = viz_center_y - bar_h // 2
            by2 = viz_center_y + bar_h // 2

            dist_from_center = abs(i - num_bars / 2) / (num_bars / 2)
            r = int(accent_rgb[0] * (1 - dist_from_center) + 235 * dist_from_center)
            g = int(accent_rgb[1] * (1 - dist_from_center) + 242 * dist_from_center)
            b = int(accent_rgb[2] * (1 - dist_from_center) + 255 * dist_from_center)

            draw.rounded_rectangle([bx, by1, bx + bar_w, by2], radius=4, fill=(r, g, b))

        # 5. Author / Narrator Attribution
        attribution_str = author if author else character_name
        author_text = f"—  {attribution_str.upper()}  —"
        author_font = self.fonts["author"]
        a_box = draw.textbbox((0, 0), author_text, font=author_font)
        aw = a_box[2] - a_box[0]
        draw.text(((self.width - aw) // 2, 1400), author_text, font=author_font, fill=(156, 168, 188))

        # 6. Handle & Watermark
        handle_text = Config.INSTAGRAM_HANDLE
        h_font = self.fonts["handle"]
        h_box = draw.textbbox((0, 0), handle_text, font=h_font)
        hw = h_box[2] - h_box[0]
        draw.text(((self.width - hw) // 2, 1680), handle_text, font=h_font, fill=(100, 116, 139))

        reminder_text = f"SAVE THIS REEL • {cat_info.get('label', 'DAILY STORIES').upper()}"
        rem_font = self.fonts["small"]
        r_box = draw.textbbox((0, 0), reminder_text, font=rem_font)
        rw = r_box[2] - r_box[0]
        draw.text(((self.width - rw) // 2, 1726), reminder_text, font=rem_font, fill=(71, 85, 105))

        # 7. Bottom Progress Bar in Category Accent Color
        progress = frame_idx / max(total_frames - 1, 1)
        bar_len = int(self.width * progress)
        if bar_len > 0:
            draw.rectangle([0, self.height - 8, bar_len, self.height], fill=accent_rgb)

        return frame

    def render_video(
        self,
        script_data: dict,
        voice_data: dict,
        output_mp4: str,
        category: str = "MOTIVATION",
        avatar_key: str = "female_innocent",
        bg_music_path: str = None
    ) -> str:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        audio_file = voice_data["audio_path"]
        duration = voice_data["duration"]
        word_timings = voice_data.get("word_timings", [])
        total_frames = int(duration * self.fps)

        word_timings_dict = {}
        for wt in word_timings:
            clean_w = wt["word"].lower().strip(".,!?;:\"'")
            word_timings_dict[clean_w] = wt

        visualizer = AudioSpectrumVisualizer(audio_file, num_bars=42, fps=self.fps)

        words = script_data["script"].split()
        quote_font = self.fonts["quote_large"] if len(words) <= 22 else self.fonts["quote_medium"]
        max_text_width = 860
        word_lines = self._wrap_text_to_lines(words, quote_font, max_text_width)
        
        dummy = Image.new("RGB", (10, 10))
        d_draw = ImageDraw.Draw(dummy)
        sample_box = d_draw.textbbox((0, 0), "Aj", font=quote_font)
        line_height = int((sample_box[3] - sample_box[1]) * 1.35)
        total_text_height = len(word_lines) * line_height

        cat = category.upper() if category.upper() in Config.CATEGORIES else "MOTIVATION"
        cat_info = Config.CATEGORIES[cat]

        if not bg_music_path:
            bg_music = str(Config.MUSIC_DIR / cat_info.get("music_file", "cinematic_ambient_drone.wav"))
        else:
            bg_music = bg_music_path

        has_bg_music = os.path.exists(bg_music)
        print(f"[VideoEngine] Category: {cat} | Avatar: {avatar_key} | Music: {Path(bg_music).name}")
        print(f"[VideoEngine] Rendering {total_frames} frames ({duration:.2f}s) to {output_mp4}...")
        start_t = time.time()

        if has_bg_music:
            music_vol = Config.BACKGROUND_MUSIC_VOLUME
            ffmpeg_cmd = [
                ffmpeg_exe, "-y",
                "-f", "rawvideo",
                "-vcodec", "rawvideo",
                "-s", f"{self.width}x{self.height}",
                "-pix_fmt", "rgb24",
                "-r", str(self.fps),
                "-i", "-",
                "-i", audio_file,
                "-stream_loop", "-1", "-i", bg_music,
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
                topic=script_data.get("topic", "STORIES"),
                author=script_data.get("author", "Storyteller"),
                category=cat,
                avatar_key=avatar_key,
                word_lines=word_lines,
                word_timings_dict=word_timings_dict,
                visualizer_bars=bars,
                quote_font=quote_font,
                line_height=line_height,
                total_text_height=total_text_height
            )

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
