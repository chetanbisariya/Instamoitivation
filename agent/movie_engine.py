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

GENRE_PALETTES = {
    "THRILLER": {
        "accent": (239, 68, 68),       # Crimson Red
        "accent_dim": (120, 25, 25),
        "highlight": (254, 202, 202),
        "tag": "SUSPENSE THRILLER",
        "music": "thriller_suspense_drone.wav",
        "icon": "⚡"
    },
    "SCI-FI": {
        "accent": (6, 182, 212),       # Cyan / Neon Teal
        "accent_dim": (15, 80, 95),
        "highlight": (165, 243, 252),
        "tag": "SCI-FI CINEMA",
        "music": "cinematic_ambient_drone.wav",
        "icon": "🛸"
    },
    "ADVENTURE": {
        "accent": (245, 158, 11),      # Amber Gold
        "accent_dim": (120, 75, 10),
        "highlight": (253, 230, 138),
        "tag": "EPIC ADVENTURE",
        "music": "adventure_epic_drone.wav",
        "icon": "🧭"
    },
    "ROMANTIC": {
        "accent": (236, 72, 153),      # Warm Rose
        "accent_dim": (115, 30, 75),
        "highlight": (251, 207, 232),
        "tag": "ROMANTIC CINEMA",
        "music": "romantic_warm_pad.wav",
        "icon": "✨"
    },
    "NOIR": {
        "accent": (148, 163, 184),     # Silver Smoke
        "accent_dim": (60, 68, 80),
        "highlight": (241, 245, 249),
        "tag": "NEO-NOIR MYSTERY",
        "music": "thriller_suspense_drone.wav",
        "icon": "🕵️"
    }
}

class MovieEngine:
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.fonts = self._load_fonts()
        self.avatar_cache = self._preload_avatars()

    def _load_fonts(self) -> dict:
        anton_path = Config.FONTS_DIR / "Anton-Regular.ttf"
        inter_path = Config.FONTS_DIR / "Inter-Variable.ttf"
        
        fonts = {}
        try:
            fonts["badge"] = ImageFont.truetype(str(inter_path), 22)
            fonts["title"] = ImageFont.truetype(str(anton_path), 58)
            fonts["act_header"] = ImageFont.truetype(str(anton_path), 36)
            fonts["keyword_pill"] = ImageFont.truetype(str(inter_path), 24)
            fonts["dialogue_large"] = ImageFont.truetype(str(anton_path), 52)
            fonts["dialogue_medium"] = ImageFont.truetype(str(anton_path), 42)
            fonts["meta"] = ImageFont.truetype(str(inter_path), 20)
            fonts["timeline"] = ImageFont.truetype(str(inter_path), 18)
        except Exception as e:
            print(f"[MovieEngine] Font load error: {e}. Fallback to default.")
            default_font = ImageFont.load_default()
            fonts = {k: default_font for k in ["badge", "title", "act_header", "keyword_pill", "dialogue_large", "dialogue_medium", "meta", "timeline"]}
        return fonts

    def _preload_avatars(self) -> dict:
        avatars = {}
        size = (140, 140)
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
                    print(f"[MovieEngine] Avatar load error: {e}")
        return avatars

    def get_avatar_image(self, avatar_key: str) -> Image.Image | None:
        if not avatar_key or avatar_key.lower() == "none":
            return None
        if avatar_key not in self.avatar_cache:
            self.avatar_cache = self._preload_avatars()
        return self.avatar_cache.get(avatar_key, None)

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

    def render_movie_frame(
        self,
        frame_idx: int,
        total_frames: int,
        current_time: float,
        movie_data: dict,
        act_info: dict,
        avatar_img: Image.Image | None,
        visualizer_bars: np.ndarray,
        palette: dict
    ) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (7, 8, 12))
        draw = ImageDraw.Draw(img)

        # 1. Anamorphic Cinematic Background Gradient
        for y in range(0, self.height, 4):
            factor = y / self.height
            # Vignette curve: darker at top/bottom, slightly warmer in mid
            curve = math.sin(factor * math.pi)
            r = int(6 + curve * (palette["accent"][0] * 0.08))
            g = int(7 + curve * (palette["accent"][1] * 0.08))
            b = int(11 + curve * (palette["accent"][2] * 0.08))
            draw.rectangle([0, y, self.width, y + 4], fill=(r, g, b))

        # 2. Cinematic Lens Flare Streak (horizontal line across mid-height)
        streak_y = 510
        for dy in range(-3, 4):
            alpha_streak = int(max(0, 1.0 - abs(dy) / 4.0) * 45)
            draw.line([(60, streak_y + dy), (self.width - 60, streak_y + dy)], fill=(palette["accent"][0], palette["accent"][1], palette["accent"][2]))

        # 3. Top Widescreen Cinema Header Badge
        top_y = 110
        genre_tag = palette["tag"]
        badge_text = f"● 3-KEYWORD SHORT FILM  |  {genre_tag}"
        bbox = draw.textbbox((0, 0), badge_text, font=self.fonts["badge"])
        badge_w = bbox[2] - bbox[0]
        badge_x = (self.width - badge_w) // 2

        # Badge pill container
        draw.rounded_rectangle(
            [badge_x - 18, top_y - 6, badge_x + badge_w + 18, top_y + 28],
            radius=14,
            fill=(20, 24, 34),
            outline=(palette["accent"][0], palette["accent"][1], palette["accent"][2]),
            width=1
        )
        draw.text((badge_x, top_y), badge_text, font=self.fonts["badge"], fill=palette["highlight"])

        # 4. Film Title (e.g. "THE SILENT PROTOCOL")
        title_y = top_y + 48
        film_title = movie_data.get("title", "UNTITLED SHORT").upper()
        t_box = draw.textbbox((0, 0), film_title, font=self.fonts["title"])
        t_w = t_box[2] - t_box[0]
        t_x = (self.width - t_w) // 2
        # Title drop shadow
        draw.text((t_x + 2, title_y + 2), film_title, font=self.fonts["title"], fill=(0, 0, 0))
        draw.text((t_x, title_y), film_title, font=self.fonts["title"], fill=(255, 255, 255))

        # 5. 3-Keyword Interactive Track Bar
        keywords = movie_data.get("keywords", ["Word 1", "Word 2", "Word 3"])
        current_act_num = act_info["act_num"]  # 1, 2, or 3
        
        pills_y = title_y + 80
        total_pills_w = 900
        pill_w = 280
        pill_gap = 20
        start_pill_x = (self.width - (pill_w * 3 + pill_gap * 2)) // 2

        for i, kw in enumerate(keywords[:3]):
            act_idx = i + 1
            px = start_pill_x + i * (pill_w + pill_gap)
            is_active = (act_idx == current_act_num)
            
            # Active vs inactive pill appearance
            if is_active:
                pulse = 0.5 + 0.5 * math.sin(current_time * 6.0)
                glow_r = int(palette["accent"][0] * (0.8 + 0.2 * pulse))
                glow_g = int(palette["accent"][1] * (0.8 + 0.2 * pulse))
                glow_b = int(palette["accent"][2] * (0.8 + 0.2 * pulse))
                bg_color = (35, 42, 58)
                outline_color = (glow_r, glow_g, glow_b)
                border_width = 3
                text_color = (255, 255, 255)
                prefix = f"ACT {act_idx} ★"
            else:
                bg_color = (18, 20, 26)
                outline_color = (45, 52, 65)
                border_width = 1
                text_color = (130, 140, 160)
                prefix = f"ACT {act_idx}"

            draw.rounded_rectangle(
                [px, pills_y, px + pill_w, pills_y + 44],
                radius=10,
                fill=bg_color,
                outline=outline_color,
                width=border_width
            )

            pill_label = f"{prefix} {kw.upper()}"
            pk_box = draw.textbbox((0, 0), pill_label, font=self.fonts["keyword_pill"])
            pk_w = pk_box[2] - pk_box[0]
            draw.text((px + (pill_w - pk_w) // 2, pills_y + 8), pill_label, font=self.fonts["keyword_pill"], fill=text_color)

        # 6. Current Act Title Banner (e.g. "ACT II: THE VAULT")
        act_banner_y = pills_y + 68
        current_act_title = act_info.get("act_title", f"ACT {current_act_num}").upper()
        act_box = draw.textbbox((0, 0), current_act_title, font=self.fonts["act_header"])
        act_w = act_box[2] - act_box[0]
        act_x = (self.width - act_w) // 2

        # Glowing act tag banner
        draw.text((act_x, act_banner_y), current_act_title, font=self.fonts["act_header"], fill=palette["accent"])

        # 7. Cinematic Avatar / Narrator Portrait with Audio-Reactive Aura
        avg_energy = float(np.mean(visualizer_bars)) if len(visualizer_bars) > 0 else 0.0
        avatar_center_y = act_banner_y + 140
        avatar_center_x = self.width // 2

        if avatar_img:
            # Aura ring
            aura_radius = int(82 + avg_energy * 26)
            for r in range(aura_radius, 70, -2):
                alpha = int((1.0 - (r - 70) / (aura_radius - 70 + 1)) * 120 * avg_energy)
                draw.ellipse(
                    (avatar_center_x - r, avatar_center_y - r, avatar_center_x + r, avatar_center_y + r),
                    outline=(palette["accent"][0], palette["accent"][1], palette["accent"][2])
                )

            # Circular avatar paste
            av_w, av_h = avatar_img.size
            img.paste(avatar_img, (avatar_center_x - av_w // 2, avatar_center_y - av_h // 2), avatar_img)

            # Outer metallic border
            draw.ellipse(
                (avatar_center_x - 72, avatar_center_y - 72, avatar_center_x + 72, avatar_center_y + 72),
                outline=(240, 245, 255),
                width=3
            )

        # 8. 42-Band Audio Spectrum Visualizer
        vis_y = avatar_center_y + 92
        num_bars = len(visualizer_bars)
        if num_bars > 0:
            total_vis_w = 680
            bar_w = int(total_vis_w / num_bars) - 2
            start_vis_x = (self.width - total_vis_w) // 2

            for i, val in enumerate(visualizer_bars):
                bx = start_vis_x + i * (bar_w + 2)
                bar_h = int(val * 48)
                if bar_h > 2:
                    interp = i / num_bars
                    cr = int(palette["accent"][0] * (1.0 - interp * 0.4))
                    cg = int(palette["accent"][1] * (1.0 - interp * 0.4))
                    cb = int(palette["accent"][2])
                    draw.rounded_rectangle(
                        [bx, vis_y - bar_h // 2, bx + bar_w, vis_y + bar_h // 2],
                        radius=2,
                        fill=(cr, cg, cb)
                    )

        # 9. Dynamic Cinematic Subtitle / Dialogue
        # Subtitles for the CURRENT ACT only, with kinetic word illumination!
        dialogue_words = act_info.get("words", [])
        word_lines = act_info.get("word_lines", [])
        font_d = self.fonts["dialogue_large"] if len(dialogue_words) <= 16 else self.fonts["dialogue_medium"]
        
        subtitles_box_top = vis_y + 55
        line_height = 56 if font_d == self.fonts["dialogue_large"] else 46
        total_text_h = len(word_lines) * line_height
        start_text_y = subtitles_box_top + (260 - total_text_h) // 2

        # Subtitle cinematic card backing
        card_margin = 70
        draw.rounded_rectangle(
            [card_margin, subtitles_box_top - 15, self.width - card_margin, subtitles_box_top + 285],
            radius=18,
            fill=(14, 17, 24),
            outline=(35, 42, 56),
            width=1
        )

        # Active keyword badge inside the dialogue card
        active_kw = keywords[current_act_num - 1] if current_act_num <= len(keywords) else ""
        card_header = f"ACT {current_act_num} FOCUS:  {active_kw.upper()}"
        draw.text((card_margin + 28, subtitles_box_top + 10), card_header, font=self.fonts["meta"], fill=palette["highlight"])

        # Render word lines with kinetic illumination
        for line_idx, line_words in enumerate(word_lines):
            dummy = Image.new("RGB", (10, 10))
            d_d = ImageDraw.Draw(dummy)
            line_str = " ".join(line_words)
            l_box = d_d.textbbox((0, 0), line_str, font=font_d)
            line_w = l_box[2] - l_box[0]
            cur_x = (self.width - line_w) // 2
            cur_y = start_text_y + line_idx * line_height + 25

            for w in line_words:
                clean_w = w.lower().strip(".,!?;:\"'")
                w_box = d_d.textbbox((0, 0), w, font=font_d)
                w_w = w_box[2] - w_box[0]
                space_w = d_d.textbbox((0, 0), " ", font=font_d)[2]

                # Check if this word is spoken right now
                wt = act_info.get("timings_dict", {}).get(clean_w, None)
                if wt and wt["start"] <= current_time <= wt["end"] + 0.15:
                    word_color = palette["highlight"]
                    # Kinetic glow under active word
                    draw.rounded_rectangle(
                        [cur_x - 3, cur_y - 2, cur_x + w_w + 3, cur_y + line_height - 12],
                        radius=4,
                        fill=palette["accent_dim"]
                    )
                elif wt and current_time > wt["end"]:
                    word_color = (255, 255, 255)
                else:
                    word_color = (140, 150, 170)

                # If word is the active keyword itself, give it gold shimmer!
                if clean_w == active_kw.lower().strip(".,!?;:\"'"):
                    word_color = (255, 215, 0)

                draw.text((cur_x, cur_y), w, font=font_d, fill=word_color)
                cur_x += w_w + space_w

        # 10. 3-Act Segmented Cinema Timeline Bar
        timeline_y = self.height - 240
        seg_gap = 14
        seg_w = (self.width - 160 - seg_gap * 2) // 3
        start_tl_x = 80

        act_progresses = act_info.get("act_progresses", [0.0, 0.0, 0.0])

        for act_i in range(3):
            tx = start_tl_x + act_i * (seg_w + seg_gap)
            prog = act_progresses[act_i]
            is_cur = (act_i + 1 == current_act_num)

            # Segment background track
            draw.rounded_rectangle([tx, timeline_y, tx + seg_w, timeline_y + 10], radius=5, fill=(30, 36, 48))

            # Filled segment
            if prog > 0.0:
                fill_w = int(seg_w * min(1.0, prog))
                bar_col = palette["accent"] if is_cur else (100, 115, 135)
                draw.rounded_rectangle([tx, timeline_y, tx + fill_w, timeline_y + 10], radius=5, fill=bar_col)

            # Act label below bar
            act_lbl = f"ACT {act_i + 1}"
            l_box = draw.textbbox((0, 0), act_lbl, font=self.fonts["timeline"])
            lw = l_box[2] - l_box[0]
            lbl_col = palette["highlight"] if is_cur else (100, 110, 125)
            draw.text((tx + (seg_w - lw) // 2, timeline_y + 16), act_lbl, font=self.fonts["timeline"], fill=lbl_col)

        # 11. Footer: Instagram Watermark & Movie Tag
        footer_y = self.height - 140
        handle_text = f"@{Config.INSTAGRAM_HANDLE}"
        h_box = draw.textbbox((0, 0), handle_text, font=self.fonts["badge"])
        h_w = h_box[2] - h_box[0]
        draw.text(((self.width - h_w) // 2, footer_y), handle_text, font=self.fonts["badge"], fill=(180, 190, 210))

        sub_footer = "AI CINEMATIC MICRO-STUDIO • GENERATED FROM 3 KEYWORDS"
        sf_box = draw.textbbox((0, 0), sub_footer, font=self.fonts["timeline"])
        sf_w = sf_box[2] - sf_box[0]
        draw.text(((self.width - sf_w) // 2, footer_y + 36), sub_footer, font=self.fonts["timeline"], fill=(80, 90, 110))

        return img

    def render_movie(
        self,
        movie_data: dict,
        voice_data: dict,
        output_mp4: str,
        avatar_key: str = "female_innocent",
        genre: str = "THRILLER"
    ) -> str:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        audio_file = voice_data["audio_path"]
        duration = voice_data["duration"]
        word_timings = voice_data.get("word_timings", [])
        total_frames = int(duration * self.fps)

        g = genre.upper() if genre.upper() in GENRE_PALETTES else "THRILLER"
        palette = GENRE_PALETTES[g]

        # Break script into Act 1, Act 2, Act 3
        scene1 = movie_data.get("scene1", "")
        scene2 = movie_data.get("scene2", "")
        scene3 = movie_data.get("scene3", "")
        scene_titles = movie_data.get("scene_titles", ["ACT I: INCIDENT", "ACT II: CONFLICT", "ACT III: CLIMAX"])

        words_s1 = scene1.split()
        words_s2 = scene2.split()
        words_s3 = scene3.split()
        total_word_count = max(1, len(words_s1) + len(words_s2) + len(words_s3))

        # Calculate time boundaries for each act
        dur1 = (len(words_s1) / total_word_count) * duration
        dur2 = (len(words_s2) / total_word_count) * duration
        act1_end = dur1
        act2_end = dur1 + dur2

        timings_dict = {}
        for wt in word_timings:
            cw = wt["word"].lower().strip(".,!?;:\"'")
            timings_dict[cw] = wt

        # Pre-wrap word lines for each act
        font_d = self.fonts["dialogue_large"]
        max_dialogue_w = 860
        s1_lines = self._wrap_text_to_lines(words_s1, font_d, max_dialogue_w)
        s2_lines = self._wrap_text_to_lines(words_s2, font_d, max_dialogue_w)
        s3_lines = self._wrap_text_to_lines(words_s3, font_d, max_dialogue_w)

        visualizer = AudioSpectrumVisualizer(audio_file, num_bars=38, fps=self.fps)
        avatar_img = self.get_avatar_image(avatar_key)

        bg_music = str(Config.MUSIC_DIR / palette["music"])
        has_bg_music = os.path.exists(bg_music)

        print(f"[MovieEngine] 🎬 Rendering 3-Keyword Short Movie: '{movie_data.get('title')}'")
        print(f"[MovieEngine] Genre: {g} | Avatar: {avatar_key} | Duration: {duration:.2f}s ({total_frames} frames)")
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

            # Determine which act is currently active
            if cur_time < act1_end:
                cur_act_num = 1
                cur_act_title = scene_titles[0] if len(scene_titles) > 0 else "ACT I: INCITING INCIDENT"
                cur_words = words_s1
                cur_lines = s1_lines
                p1 = cur_time / max(0.01, dur1)
                p2 = 0.0
                p3 = 0.0
            elif cur_time < act2_end:
                cur_act_num = 2
                cur_act_title = scene_titles[1] if len(scene_titles) > 1 else "ACT II: RISING CONFLICT"
                cur_words = words_s2
                cur_lines = s2_lines
                p1 = 1.0
                p2 = (cur_time - act1_end) / max(0.01, dur2)
                p3 = 0.0
            else:
                cur_act_num = 3
                cur_act_title = scene_titles[2] if len(scene_titles) > 2 else "ACT III: THE CLIMAX"
                cur_words = words_s3
                cur_lines = s3_lines
                p1 = 1.0
                p2 = 1.0
                p3 = (cur_time - act2_end) / max(0.01, duration - act2_end)

            act_info = {
                "act_num": cur_act_num,
                "act_title": cur_act_title,
                "words": cur_words,
                "word_lines": cur_lines,
                "timings_dict": timings_dict,
                "act_progresses": [p1, p2, p3]
            }

            frame_img = self.render_movie_frame(
                frame_idx=frame_idx,
                total_frames=total_frames,
                current_time=cur_time,
                movie_data=movie_data,
                act_info=act_info,
                avatar_img=avatar_img,
                visualizer_bars=bars,
                palette=palette
            )

            proc.stdin.write(frame_img.tobytes())

        proc.stdin.close()
        stderr_output = proc.stderr.read()
        proc.wait()

        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg movie encoding failed: {stderr_output.decode('utf-8', errors='ignore')}")

        elapsed = time.time() - start_t
        fps_rendered = total_frames / max(elapsed, 0.001)
        print(f"[MovieEngine] 🎬 Short movie render complete in {elapsed:.1f}s ({fps_rendered:.1f} fps) -> {output_mp4}")
        return output_mp4
