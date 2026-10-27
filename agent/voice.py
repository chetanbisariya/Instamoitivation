import asyncio
import base64
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
        cleaned = re.sub(r'#\w+', '', text)
        cleaned = re.sub(r'[\U00010000-\U0010ffff]', '', cleaned, flags=re.UNICODE)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    @classmethod
    def resolve_voice_ids(cls, voice_key: str = None) -> tuple[str, str, str]:
        all_voices = Config.get_voices()
        if not voice_key or voice_key not in all_voices:
            voice_key = "ava_female" if "girl" in str(voice_key).lower() or "female" in str(voice_key).lower() else "christopher_male"
            
        voice_info = all_voices.get(voice_key, all_voices.get("christopher_male", {}))
        edge_id = voice_info.get("edge_id", "en-US-ChristopherNeural")
        eleven_id = voice_info.get("eleven_id", "pNInz6obpgDQGcFmaJgB")
        name = voice_info.get("name", "Neural Voice")
        return edge_id, eleven_id, name

    @classmethod
    def clone_voice_with_elevenlabs(cls, name: str, audio_file_path: str, description: str = "") -> dict:
        """
        Uses ElevenLabs Instant Voice Cloning API to clone a voice from an uploaded audio sample.
        """
        api_key = Config.ELEVENLABS_API_KEY
        if not api_key:
            return {
                "success": False,
                "message": "ElevenLabs API key is not configured. Please set ELEVENLABS_API_KEY in settings to clone voices."
            }

        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {"xi-api-key": api_key}
        
        try:
            with open(audio_file_path, "rb") as af:
                files = [("files", (Path(audio_file_path).name, af, "audio/mpeg"))]
                data = {
                    "name": name,
                    "description": description or f"Custom cloned voice for {name}"
                }
                res = requests.post(url, headers=headers, data=data, files=files, timeout=60)
                
            if res.status_code in [200, 201]:
                voice_data = res.json()
                voice_id = voice_data.get("voice_id")
                return {
                    "success": True,
                    "voice_id": voice_id,
                    "message": f"Voice '{name}' cloned successfully in ElevenLabs! Voice ID: {voice_id}"
                }
            else:
                return {
                    "success": False,
                    "message": f"ElevenLabs cloning error: {res.status_code} - {res.text}"
                }
        except Exception as e:
            return {"success": False, "message": f"Voice cloning exception: {str(e)}"}

    @classmethod
    def process_direct_audio(cls, audio_file_path: str, script_text: str = "") -> dict:
        """
        Processes a user-uploaded spoken voice recording directly without TTS.
        Calculates audio duration and builds word-level alignment pacing.
        """
        duration = cls.get_audio_duration(audio_file_path)
        words = script_text.split() if script_text else ["Spoken", "Narration"]
        
        word_timings = []
        pad_start = 0.3
        pad_end = 0.4
        effective_dur = max(duration - pad_start - pad_end, 1.0)
        total_chars = sum(len(w) for w in words)
        curr_time = pad_start
        
        for w in words:
            word_dur = (len(w) / max(total_chars, 1)) * effective_dur
            word_dur = max(word_dur, 0.20)
            word_timings.append({
                "word": w,
                "start": curr_time,
                "end": curr_time + word_dur
            })
            curr_time += word_dur + 0.04

        return {
            "audio_path": audio_file_path,
            "duration": duration,
            "provider": "User Custom Audio",
            "voice_key": "user_uploaded",
            "voice_name": "Custom Uploaded Voice",
            "word_timings": word_timings,
            "word_count": len(words)
        }

    @classmethod
    def synthesize_with_elevenlabs(cls, text: str, output_path: str, voice_id: str = None) -> tuple[bool, str, list]:
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
                audio_bytes = base64.b64decode(data.get("audio_base64", ""))
                with open(output_path, "wb") as f:
                    f.write(audio_bytes)
                
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
                std_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
                res_std = requests.post(std_url, headers={"xi-api-key": api_key, "Content-Type": "application/json"}, json=payload, timeout=30)
                if res_std.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(res_std.content)
                    return True, "ElevenLabs standard synthesis succeeded", []
                else:
                    return False, f"ElevenLabs API error: {res_std.status_code}", []
            else:
                return False, f"ElevenLabs API error: {res.status_code}", []
        except Exception as e:
            return False, f"ElevenLabs request exception: {str(e)}", []

    @classmethod
    async def _async_edge_tts(cls, text: str, output_path: str, voice: str) -> None:
        communicate = edge_tts.Communicate(text, voice, rate="-3%", pitch="-1Hz")
        await communicate.save(output_path)

    @classmethod
    def synthesize_with_edge_tts(cls, text: str, output_path: str, voice: str = None) -> tuple[bool, str, list]:
        voice_name = voice or Config.FALLBACK_TTS_VOICE or "en-US-AvaNeural"
        try:
            asyncio.run(cls._async_edge_tts(text, output_path, voice_name))
            return True, f"Edge-TTS synthesis succeeded with voice {voice_name}", []
        except Exception as e:
            return False, f"Edge-TTS failed: {str(e)}", []

    @classmethod
    def generate_voiceover(cls, text: str, output_path: str, voice_key: str = None) -> dict:
        clean_text = cls.clean_text_for_speech(text)
        words = clean_text.split()
        
        edge_id, eleven_id, display_name = cls.resolve_voice_ids(voice_key)

        provider = "ElevenLabs"
        success, msg, word_timings = False, "", []
        
        if Config.ELEVENLABS_API_KEY:
            success, msg, word_timings = cls.synthesize_with_elevenlabs(clean_text, output_path, voice_id=eleven_id)
        
        if not success:
            provider = f"Neural Voice ({display_name})"
            success, msg, word_timings = cls.synthesize_with_edge_tts(clean_text, output_path, voice=edge_id)
            if not success:
                fallback_v = "en-US-ChristopherNeural"
                success, msg, word_timings = cls.synthesize_with_edge_tts(clean_text, output_path, voice=fallback_v)
                if not success:
                    raise RuntimeError(f"All TTS synthesis options failed: {msg}")

        duration = cls.get_audio_duration(output_path)
        
        if not word_timings and words:
            pad_start = 0.35
            pad_end = 0.45
            effective_dur = max(duration - pad_start - pad_end, 1.0)
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
                curr_time += word_dur + 0.04
                
        return {
            "audio_path": output_path,
            "duration": duration,
            "provider": provider,
            "voice_key": voice_key or "default",
            "voice_name": display_name,
            "word_timings": word_timings,
            "word_count": len(words)
        }

    @staticmethod
    def get_audio_duration(file_path: str) -> float:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [ffmpeg_exe, "-i", file_path, "-f", "null", "-"]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', res.stderr)
        if match:
            h, m, s = match.groups()
            return int(h) * 3600 + int(m) * 60 + float(s)
        return 15.0
