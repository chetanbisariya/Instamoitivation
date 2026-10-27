import asyncio
import json
import os
import re
import subprocess
import requests
from pathlib import Path
import edge_tts
from agent.config import Config

class VoiceSynthesizer:
    @staticmethod
    def clean_text_for_speech(text: str) -> str:
        """Removes markdown, emojis, and hashtags for crisp speech synthesis."""
        # Remove emojis and hashtag blocks
        cleaned = re.sub(r'#\w+', '', text)
        cleaned = re.sub(r'[\U00010000-\U0010ffff]', '', cleaned, flags=re.UNICODE)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    @classmethod
    def synthesize_with_elevenlabs(cls, text: str, output_path: str, voice_id: str = None) -> tuple[bool, str, list]:
        """
        Synthesizes speech using ElevenLabs API.
        Returns: (success, message, word_timings)
        """
        api_key = Config.ELEVENLABS_API_KEY
        if not api_key:
            return False, "ELEVENLABS_API_KEY is not set.", []
            
        voice = voice_id or Config.ELEVENLABS_VOICE_ID or "pNInz6obpgDQGcFmaJgB"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps"
        
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "text": text,
            "model_id": Config.ELEVENLABS_MODEL_ID or "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.60,
                "similarity_boost": 0.85,
                "style": 0.25,
                "use_speaker_boost": True
            }
        }
        
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                data = res.json()
                import base64
                audio_bytes = base64.b64decode(data.get("audio_base64", ""))
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
                
                # Extract word timestamps if alignment is provided
                word_timings = []
                alignment = data.get("alignment", {})
                chars = alignment.get("characters", [])
                char_starts = alignment.get("character_start_times_seconds", [])
                char_ends = alignment.get("character_end_times_seconds", [])
                
                if chars and char_starts and char_ends:
                    curr_word = ""
                    w_start = None
                    for i, ch in enumerate(chars):
                        if ch.isalnum() or ch in "'-":
                            if w_start is None:
                                w_start = char_starts[i]
                            curr_word += ch
                        else:
                            if curr_word and w_start is not None:
                                word_timings.append({
                                    "word": curr_word,
                                    "start": w_start,
                                    "end": char_ends[i-1] if i > 0 else char_starts[i]
                                })
                                curr_word = ""
                                w_start = None
                    if curr_word and w_start is not None:
                        word_timings.append({
                            "word": curr_word,
                            "start": w_start,
                            "end": char_ends[-1]
                        })
                        
                return True, "ElevenLabs synthesis succeeded with alignment", word_timings
            elif res.status_code == 404:
                # If with-timestamps not supported on this endpoint/tier, try standard endpoint
                std_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
                res_std = requests.post(std_url, headers={"xi-api-key": api_key, "Content-Type": "application/json"}, json=payload, timeout=30)
                if res_std.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(res_std.content)
                    return True, "ElevenLabs standard synthesis succeeded", []
                else:
                    return False, f"ElevenLabs API error: {res_std.status_code} {res_std.text}", []
            else:
                return False, f"ElevenLabs API error: {res.status_code} {res.text}", []
        except Exception as e:
            return False, f"ElevenLabs request exception: {str(e)}", []

    @classmethod
    async def _async_edge_tts(cls, text: str, output_path: str, voice: str) -> None:
        communicate = edge_tts.Communicate(text, voice, rate="-4%", pitch="-2Hz")
        await communicate.save(output_path)

    @classmethod
    def synthesize_with_edge_tts(cls, text: str, output_path: str, voice: str = None) -> tuple[bool, str, list]:
        """Free fallback high quality TTS using Microsoft Edge neural voice."""
        voice_name = voice or Config.FALLBACK_TTS_VOICE or "en-US-ChristopherNeural"
        try:
            asyncio.run(cls._async_edge_tts(text, output_path, voice_name))
            return True, f"Edge-TTS synthesis succeeded with voice {voice_name}", []
        except Exception as e:
            return False, f"Edge-TTS failed: {str(e)}", []

    @classmethod
    def generate_voiceover(cls, text: str, output_path: str) -> dict:
        """
        Synthesizes voiceover trying ElevenLabs first, falling back to Edge-TTS.
        Also parses audio duration and calculates word pacing.
        """
        clean_text = cls.clean_text_for_speech(text)
        words = clean_text.split()
        
        provider = "ElevenLabs"
        success, msg, word_timings = cls.synthesize_with_elevenlabs(clean_text, output_path)
        
        if not success:
            print(f"[Voice] {msg}. Falling back to Edge-TTS ({Config.FALLBACK_TTS_VOICE})...")
            provider = "Edge-TTS"
            success, msg, word_timings = cls.synthesize_with_edge_tts(clean_text, output_path)
            if not success:
                raise RuntimeError(f"All TTS providers failed: {msg}")
        
        # Measure audio duration using ffmpeg probe
        duration = cls.get_audio_duration(output_path)
        
        # If word timings were not provided by API alignment, generate proportional timings
        if not word_timings and words:
            # Distribute words evenly across duration with padding
            pad_start = 0.4
            pad_end = 0.5
            effective_dur = max(duration - pad_start - pad_end, 1.0)
            
            # Weight word lengths by character count
            total_chars = sum(len(w) for w in words)
            curr_time = pad_start
            
            for w in words:
                word_dur = (len(w) / max(total_chars, 1)) * effective_dur
                word_dur = max(word_dur, 0.22)
                word_timings.append({
                    "word": w,
                    "start": curr_time,
                    "end": curr_time + word_dur
                })
                curr_time += word_dur + 0.05
                
        return {
            "audio_path": output_path,
            "duration": duration,
            "provider": provider,
            "word_timings": word_timings,
            "word_count": len(words)
        }

    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        """Calculates audio duration in seconds via imageio_ffmpeg."""
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe, "-i", file_path,
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        # Parse Duration: 00:00:15.32 from stderr
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', res.stderr)
        if match:
            h, m, s = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(s)
        return 15.0 # fallback default duration

if __name__ == "__main__":
    out_file = str(Config.OUTPUT_DIR / "test_voice.mp3")
    res = VoiceSynthesizer.generate_voiceover(
        "Motivation is an emotion. Discipline is a decision. Show up and do the work anyway.",
        out_file
    )
    print("Synthesized audio successfully:", res["provider"], f"Duration: {res['duration']:.2f}s")
