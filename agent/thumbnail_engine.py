import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from agent.config import Config

class ThumbnailEngine:
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.fonts = self._load_fonts()

    def _load_fonts(self) -> dict:
        anton_path = Config.FONTS_DIR / "Anton-Regular.ttf"
        inter_path = Config.FONTS_DIR / "Inter-Variable.ttf"
        fonts = {}
        try:
            fonts["badge"] = ImageFont.truetype(str(inter_path), 28)
            fonts["title_huge"] = ImageFont.truetype(str(anton_path), 82)
            fonts["title_large"] = ImageFont.truetype(str(anton_path), 68)
            fonts["hook"] = ImageFont.truetype(str(inter_path), 34)
            fonts["handle"] = ImageFont.truetype(str(inter_path), 30)
            fonts["meta"] = ImageFont.truetype(str(inter_path), 22)
        except Exception:
            default_font = ImageFont.load_default()
            fonts = {k: default_font for k in ["badge", "title_huge", "title_large", "hook", "handle", "meta"]}
        return fonts

    def _get_font(self, font_key: str, text: str = ""):
        if text and any(ord(c) > 127 for c in text):
            u_paths = [
                "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
                "/Library/Fonts/Arial Unicode.ttf",
                "/System/Library/Fonts/Supplemental/DevanagariMT.ttc"
            ]
            sizes = {
                "badge": 28,
                "title_huge": 72,
                "title_large": 58,
                "hook": 32,
                "handle": 30,
                "meta": 22
            }
            sz = sizes.get(font_key, 32)
            for up in u_paths:
                if os.path.exists(up):
                    try:
                        return ImageFont.truetype(up, sz)
                    except Exception:
                        pass
        return self.fonts.get(font_key, self.fonts["badge"])

    def generate_cover(
        self,
        title: str,
        category: str = "MOTIVATION",
        hook: str = "",
        keywords: list[str] = None,
        avatar_key: str = "female_innocent",
        output_path: str = None
    ) -> str:
        img = Image.new("RGB", (self.width, self.height), (8, 9, 14))
        draw = ImageDraw.Draw(img)

        # 1. Atmospheric Deep Cinema Background Gradient
        for y in range(0, self.height, 4):
            factor = y / self.height
            r = int(7 + factor * 14)
            g = int(8 + factor * 15)
            b = int(14 + factor * 22)
            draw.rectangle([0, y, self.width, y + 4], fill=(r, g, b))

        cat_upper = category.upper()
        if "THRILLER" in cat_upper or "MOVIE_THRILLER" in cat_upper:
            accent_col = (239, 68, 68)      # Crimson
            badge_text = "● SUSPENSE THRILLER PREMIERE"
        elif "SCI-FI" in cat_upper or "MOVIE_SCI-FI" in cat_upper:
            accent_col = (6, 182, 212)      # Cyan
            badge_text = "● SCI-FI CINEMA PREMIERE"
        elif "ADVENTURE" in cat_upper or "MOVIE_ADVENTURE" in cat_upper:
            accent_col = (245, 158, 11)     # Amber Gold
            badge_text = "● EPIC ADVENTURE STORY"
        elif "ROMANTIC" in cat_upper or "MOVIE_ROMANTIC" in cat_upper:
            accent_col = (244, 63, 94)      # Warm Rose
            badge_text = "● ROMANTIC & POETIC"
        else:
            accent_col = (245, 158, 11)     # Gold
            badge_text = f"● {cat_upper}"

        # 2. Dramatic Center Glow
        glow = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        center_x, center_y = self.width // 2, int(self.height * 0.44)
        for r in range(480, 0, -20):
            alpha = int((1.0 - (r / 480) ** 1.3) * 40)
            glow_draw.ellipse(
                (center_x - r, center_y - r, center_x + r, center_y + r),
                fill=(accent_col[0], accent_col[1], accent_col[2], alpha)
            )
        img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
        draw = ImageDraw.Draw(img)

        # 3. Top Category Badge Pill
        badge_y = 280
        b_box = draw.textbbox((0, 0), badge_text, font=self.fonts["badge"])
        bw = b_box[2] - b_box[0]
        bx = (self.width - bw) // 2
        draw.rounded_rectangle(
            [bx - 24, badge_y - 8, bx + bw + 24, badge_y + 36],
            radius=18,
            fill=(18, 22, 32),
            outline=accent_col,
            width=2
        )
        draw.text((bx, badge_y), badge_text, font=self.fonts["badge"], fill=(255, 255, 255))

        # 4. Narrator Avatar Portrait with Glowing Rings
        if avatar_key and avatar_key.lower() != "none":
            avatars = Config.get_avatars()
            av_info = avatars.get(avatar_key, {})
            av_file = Config.AVATARS_DIR / av_info.get("file", "female_innocent.jpg")
            if av_file.exists():
                try:
                    av_raw = Image.open(av_file).convert("RGBA")
                    av_size = (180, 180)
                    av_img = ImageOps.fit(av_raw, av_size, method=Image.Resampling.LANCZOS)
                    mask = Image.new("L", av_size, 0)
                    m_draw = ImageDraw.Draw(mask)
                    m_draw.ellipse((0, 0, av_size[0], av_size[1]), fill=255)
                    av_img.putalpha(mask)

                    av_center_y = badge_y + 160
                    # Outer glowing aura
                    for ar in range(115, 90, -3):
                        draw.ellipse(
                            (center_x - ar, av_center_y - ar, center_x + ar, av_center_y + ar),
                            outline=accent_col
                        )
                    # Paste portrait
                    img.paste(av_img, (center_x - 90, av_center_y - 90), av_img)
                    draw.ellipse(
                        (center_x - 93, av_center_y - 93, center_x + 93, av_center_y + 93),
                        outline=(255, 255, 255),
                        width=3
                    )
                except Exception as e:
                    print(f"[ThumbnailEngine] Avatar draw error: {e}")

        # 5. Bold High-Impact Clickbait Title
        title_y = badge_y + 300
        title_text = title.upper()
        # Word wrap title to at most 3 lines
        words = title_text.split()
        lines = []
        cur_l = []
        t_font = self._get_font("title_huge" if len(words) <= 5 else "title_large", title_text)
        for w in words:
            test_l = cur_l + [w]
            test_str = " ".join(test_l)
            bbox = draw.textbbox((0, 0), test_str, font=t_font)
            if bbox[2] - bbox[0] <= 900 or not cur_l:
                cur_l.append(w)
            else:
                lines.append(cur_l)
                cur_l = [w]
        if cur_l:
            lines.append(cur_l)

        line_h = 86 if len(words) <= 5 else 74
        for i, l_words in enumerate(lines):
            l_str = " ".join(l_words)
            bbox = draw.textbbox((0, 0), l_str, font=t_font)
            lx = (self.width - (bbox[2] - bbox[0])) // 2
            ly = title_y + i * line_h
            # Drop shadow
            draw.text((lx + 3, ly + 3), l_str, font=t_font, fill=(0, 0, 0))
            draw.text((lx, ly), l_str, font=t_font, fill=(255, 255, 255))

        # 6. Keywords Pill Bar or Hook Subtitle
        next_y = title_y + len(lines) * line_h + 35
        if keywords and len(keywords) >= 3:
            kw_text = f"◆ {keywords[0].upper()}   •   ◆ {keywords[1].upper()}   •   ◆ {keywords[2].upper()}"
            kw_font = self._get_font("hook", kw_text)
            k_box = draw.textbbox((0, 0), kw_text, font=kw_font)
            kw_w = k_box[2] - k_box[0]
            kx = (self.width - kw_w) // 2
            draw.rounded_rectangle(
                [kx - 24, next_y - 8, kx + kw_w + 24, next_y + 46],
                radius=14,
                fill=(22, 28, 40),
                outline=accent_col,
                width=1
            )
            draw.text((kx, next_y), kw_text, font=kw_font, fill=(255, 215, 0))
        elif hook:
            hook_font = self._get_font("hook", hook)
            h_box = draw.textbbox((0, 0), f'"{hook}"', font=hook_font)
            hw = h_box[2] - h_box[0]
            hx = (self.width - min(hw, 900)) // 2
            draw.text((hx, next_y), f'"{hook[:55]}..."', font=hook_font, fill=(200, 210, 230))

        # 7. Instagram Branding Footer
        footer_y = self.height - 240
        handle_text = Config.INSTAGRAM_HANDLE if Config.INSTAGRAM_HANDLE.startswith("@") else f"@{Config.INSTAGRAM_HANDLE}"
        h_font = self._get_font("handle", handle_text)
        h_box = draw.textbbox((0, 0), handle_text, font=h_font)
        hw = h_box[2] - h_box[0]
        draw.text(((self.width - hw) // 2, footer_y), handle_text, font=h_font, fill=(255, 255, 255))

        sub_footer = "AI STORYTELLING & CINEMA STUDIO • TAP TO WATCH"
        sf_box = draw.textbbox((0, 0), sub_footer, font=self.fonts["meta"])
        sf_w = sf_box[2] - sf_box[0]
        draw.text(((self.width - sf_w) // 2, footer_y + 44), sub_footer, font=self.fonts["meta"], fill=(120, 130, 150))

        if not output_path:
            clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
            output_path = str(Config.OUTPUT_DIR / f"cover_{clean_title[:20].lower().replace(' ', '_')}.jpg")

        img.save(output_path, "JPEG", quality=95)
        print(f"[ThumbnailEngine] Saved cover thumbnail -> {output_path}")
        return output_path
