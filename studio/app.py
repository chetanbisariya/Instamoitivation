import datetime
import glob
import json
import os
import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image, ImageOps

from agent.config import Config
from agent.runner import DailyReelAgent
from agent.voice import VoiceSynthesizer
from agent.publisher import SocialPublisher

app = FastAPI(title="Instagram Story & Motivation Agent Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = DailyReelAgent()

class GenerateRequest(BaseModel):
    category: str = "MOTIVATION"
    voice: str = ""
    avatar: str = ""
    topic: str = ""
    prompt: str = ""

class ConfigUpdateRequest(BaseModel):
    instagram_handle: str = ""
    default_category: str = ""
    default_voice: str = ""
    default_avatar: str = ""
    show_avatar: bool = True
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""
    buffer_access_token: str = ""
    buffer_profile_id: str = ""
    webhook_url: str = ""
    gemini_api_key: str = ""
    schedule_time: str = ""
    schedule_category_rotation: bool = True

@app.get("/api/options")
def get_options():
    return {
        "categories": Config.CATEGORIES,
        "voices": Config.get_voices(),
        "avatars": Config.get_avatars(),
        "defaults": {
            "category": Config.DEFAULT_CATEGORY,
            "voice": Config.DEFAULT_VOICE,
            "avatar": Config.DEFAULT_AVATAR,
            "show_avatar": Config.SHOW_AVATAR,
            "schedule_time": Config.SCHEDULE_TIME,
            "rotation_enabled": Config.SCHEDULE_CATEGORY_ROTATION
        }
    }

@app.get("/api/config")
def get_config():
    return {
        "instagram_handle": Config.INSTAGRAM_HANDLE,
        "default_category": Config.DEFAULT_CATEGORY,
        "default_voice": Config.DEFAULT_VOICE,
        "default_avatar": Config.DEFAULT_AVATAR,
        "show_avatar": Config.SHOW_AVATAR,
        "elevenlabs_configured": bool(Config.ELEVENLABS_API_KEY),
        "elevenlabs_voice_id": Config.ELEVENLABS_VOICE_ID,
        "gemini_configured": bool(Config.GEMINI_API_KEY),
        "buffer_configured": bool(Config.BUFFER_ACCESS_TOKEN and Config.BUFFER_PROFILE_ID),
        "webhook_configured": bool(Config.WEBHOOK_URL),
        "webhook_url": Config.WEBHOOK_URL,
        "schedule_time": Config.SCHEDULE_TIME,
        "schedule_category_rotation": Config.SCHEDULE_CATEGORY_ROTATION,
        "output_dir": str(Config.OUTPUT_DIR)
    }

@app.post("/api/config")
def update_config(req: ConfigUpdateRequest):
    env_path = Config.BASE_DIR / ".env"
    lines = []
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    updates = {}
    if req.instagram_handle: updates["INSTAGRAM_HANDLE"] = req.instagram_handle
    if req.default_category: updates["DEFAULT_CATEGORY"] = req.default_category
    if req.default_voice: updates["DEFAULT_VOICE"] = req.default_voice
    if req.default_avatar: updates["DEFAULT_AVATAR"] = req.default_avatar
    updates["SHOW_AVATAR"] = "true" if req.show_avatar else "false"
    updates["SCHEDULE_CATEGORY_ROTATION"] = "true" if req.schedule_category_rotation else "false"
    if req.elevenlabs_api_key: updates["ELEVENLABS_API_KEY"] = req.elevenlabs_api_key
    if req.elevenlabs_voice_id: updates["ELEVENLABS_VOICE_ID"] = req.elevenlabs_voice_id
    if req.buffer_access_token: updates["BUFFER_ACCESS_TOKEN"] = req.buffer_access_token
    if req.buffer_profile_id: updates["BUFFER_PROFILE_ID"] = req.buffer_profile_id
    if req.webhook_url: updates["WEBHOOK_URL"] = req.webhook_url
    if req.gemini_api_key: updates["GEMINI_API_KEY"] = req.gemini_api_key
    if req.schedule_time: updates["SCHEDULE_TIME"] = req.schedule_time

    new_lines = []
    found_keys = set()
    for line in lines:
        matched = False
        for k, v in updates.items():
            if line.startswith(f"{k}="):
                new_lines.append(f"{k}={v}\n")
                found_keys.add(k)
                matched = True
                break
        if not matched:
            new_lines.append(line)

    for k, v in updates.items():
        if k not in found_keys:
            new_lines.append(f"{k}={v}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    if req.instagram_handle: Config.INSTAGRAM_HANDLE = req.instagram_handle
    if req.default_category: Config.DEFAULT_CATEGORY = req.default_category
    if req.default_voice: Config.DEFAULT_VOICE = req.default_voice
    if req.default_avatar: Config.DEFAULT_AVATAR = req.default_avatar
    Config.SHOW_AVATAR = req.show_avatar
    Config.SCHEDULE_CATEGORY_ROTATION = req.schedule_category_rotation
    if req.elevenlabs_api_key: Config.ELEVENLABS_API_KEY = req.elevenlabs_api_key
    if req.elevenlabs_voice_id: Config.ELEVENLABS_VOICE_ID = req.elevenlabs_voice_id
    if req.buffer_access_token: Config.BUFFER_ACCESS_TOKEN = req.buffer_access_token
    if req.buffer_profile_id: Config.BUFFER_PROFILE_ID = req.buffer_profile_id
    if req.webhook_url: Config.WEBHOOK_URL = req.webhook_url
    if req.gemini_api_key: Config.GEMINI_API_KEY = req.gemini_api_key
    if req.schedule_time: Config.SCHEDULE_TIME = req.schedule_time

    return {"success": True, "message": "Settings updated successfully."}

@app.post("/api/upload/avatar")
async def upload_custom_avatar(
    avatar_file: UploadFile = File(...),
    name: str = Form(...),
    gender: str = Form("Custom"),
    description: str = Form("Custom Narrator Character")
):
    """Uploads a custom character image and integrates it into the avatar system."""
    try:
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in name if c.isalnum()).lower() or "character"
        avatar_id = f"custom_{safe_name}_{timestamp_str}"
        filename = f"{avatar_id}.jpg"

        dest_path = Config.AVATARS_DIR / filename
        static_dest_path = Config.BASE_DIR / "studio" / "static" / "avatars" / filename
        static_dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Process and save as square JPEG
        image = Image.open(avatar_file.file).convert("RGB")
        image = ImageOps.fit(image, (500, 500), method=Image.Resampling.LANCZOS)
        image.save(dest_path, "JPEG", quality=92)
        image.save(static_dest_path, "JPEG", quality=92)

        avatar_data = {
            "name": name.strip(),
            "gender": gender.strip(),
            "file": filename,
            "description": description.strip() or f"Custom character {name}",
            "custom": True
        }
        Config.save_custom_avatar(avatar_id, avatar_data)

        # Invalidate video engine avatar cache
        agent.video_engine.avatar_cache = agent.video_engine._preload_avatars()

        return {
            "success": True,
            "avatar_id": avatar_id,
            "avatar_data": avatar_data,
            "message": f"Character '{name}' uploaded and ready to narrate!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Avatar upload failed: {str(e)}")

@app.post("/api/upload/voice")
async def upload_custom_voice(
    audio_file: UploadFile = File(...),
    name: str = Form(...),
    clone_mode: bool = Form(False),
    description: str = Form("")
):
    """Uploads a voice recording sample for cloning or direct use."""
    try:
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in name if c.isalnum()).lower() or "voice"
        voice_id = f"custom_voice_{safe_name}_{timestamp_str}"
        ext = Path(audio_file.filename).suffix or ".mp3"
        filename = f"{voice_id}{ext}"
        saved_path = Config.UPLOADS_DIR / filename

        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        cloned_voice_id = ""
        clone_msg = "Saved locally"

        if clone_mode and Config.ELEVENLABS_API_KEY:
            clone_res = VoiceSynthesizer.clone_voice_with_elevenlabs(
                name=name,
                audio_file_path=str(saved_path),
                description=description or f"Custom clone for {name}"
            )
            if clone_res.get("success"):
                cloned_voice_id = clone_res.get("voice_id", "")
                clone_msg = f"Cloned in ElevenLabs (ID: {cloned_voice_id})"
            else:
                clone_msg = f"Local save only (Cloning notice: {clone_res.get('message')})"

        voice_data = {
            "name": f"{name} (Custom)",
            "gender": "Custom",
            "edge_id": "en-US-AvaNeural",
            "eleven_id": cloned_voice_id or "21m00Tcm4TlvDq8ikWAM",
            "audio_file": str(saved_path),
            "description": description.strip() or f"Custom uploaded voice ({clone_msg})",
            "custom": True
        }
        Config.save_custom_voice(voice_id, voice_data)

        return {
            "success": True,
            "voice_id": voice_id,
            "voice_data": voice_data,
            "message": f"Voice '{name}' registered successfully! ({clone_msg})"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice upload failed: {str(e)}")

@app.post("/api/generate-with-audio")
async def generate_with_custom_audio(
    audio_file: UploadFile = File(...),
    category: str = Form("ROMANTIC"),
    avatar: str = Form("female_innocent"),
    topic: str = Form("MY SPOKEN STORY"),
    script: str = Form(...),
    author: str = Form("Me")
):
    """Directly produces a 1080x1920 reel from the user's uploaded voice recording."""
    try:
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = Path(audio_file.filename).suffix or ".mp3"
        saved_audio = Config.OUTPUT_DIR / f"user_voice_{timestamp_str}{ext}"

        with open(saved_audio, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        # Process user audio duration & word timings
        voice_data = VoiceSynthesizer.process_direct_audio(str(saved_audio), script)

        cat = category.upper() if category.upper() in Config.CATEGORIES else "ROMANTIC"
        script_data = {
            "category": cat,
            "topic": topic.upper(),
            "author": author,
            "script": script,
            "caption": f"{script}\n\n— {author}\n\n#story #reels #viral #fyp"
        }

        video_filename = f"reel_custom_{cat.lower()}_{timestamp_str}.mp4"
        video_path = str(Config.OUTPUT_DIR / video_filename)

        agent.video_engine.render_video(
            script_data=script_data,
            voice_data=voice_data,
            output_mp4=video_path,
            category=cat,
            avatar_key=avatar
        )

        publish_result = SocialPublisher.queue_post(video_path, script_data, voice_data)

        return {
            "success": True,
            "reel": {
                "filename": video_filename,
                "url": f"/media/{video_filename}",
                "category": cat,
                "topic": topic,
                "author": author,
                "avatar": avatar,
                "caption": script_data["caption"],
                "script": script,
                "duration": voice_data["duration"],
                "provider": "User Custom Audio",
                "status": publish_result["status"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Custom audio reel generation failed: {str(e)}")

@app.get("/api/reels")
def list_reels():
    mp4_files = sorted(glob.glob(str(Config.OUTPUT_DIR / "*.mp4")), key=os.path.getmtime, reverse=True)
    reels = []
    for f in mp4_files:
        p = Path(f)
        manifest_p = p.with_suffix(".json")
        meta = {}
        if manifest_p.exists():
            try:
                with open(manifest_p, "r", encoding="utf-8") as mf:
                    meta = json.load(mf)
            except Exception:
                pass
        
        reels.append({
            "filename": p.name,
            "url": f"/media/{p.name}",
            "size_mb": round(p.stat().st_size / (1024 * 1024), 2),
            "created_at": datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "category": meta.get("category", "MOTIVATION"),
            "topic": meta.get("topic", "STORIES"),
            "author": meta.get("author", "Storyteller"),
            "avatar": meta.get("avatar", "female_innocent"),
            "script": meta.get("script", ""),
            "caption": meta.get("caption", ""),
            "hashtags": meta.get("hashtags", []),
            "duration": meta.get("duration", 0),
            "voice_name": meta.get("voice_name", "Neural Voice"),
            "status": meta.get("status", "SAVED_LOCALLY")
        })
    return reels

@app.post("/api/generate")
def generate_reel(req: GenerateRequest):
    try:
        result = agent.run_pipeline(
            category=req.category,
            voice_key=req.voice,
            avatar_key=req.avatar,
            topic=req.topic,
            custom_prompt=req.prompt
        )
        return {
            "success": True,
            "reel": {
                "filename": result["video_filename"],
                "url": f"/media/{result['video_filename']}",
                "category": result["category"],
                "topic": result["script_data"].get("topic"),
                "author": result["script_data"].get("author"),
                "avatar": result["avatar_key"],
                "caption": result["script_data"].get("caption"),
                "script": result["script_data"].get("script"),
                "hashtags": result["script_data"].get("hashtags", []),
                "duration": result["voice_data"].get("duration"),
                "voice_name": result["voice_data"].get("voice_name"),
                "provider": result["voice_data"].get("provider"),
                "status": result["publish_result"]["status"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/publish/{filename}")
def publish_reel(filename: str):
    video_p = Config.OUTPUT_DIR / filename
    if not video_p.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    manifest_p = video_p.with_suffix(".json")
    meta = {}
    if manifest_p.exists():
        with open(manifest_p, "r", encoding="utf-8") as f:
            meta = json.load(f)

    caption = meta.get("caption", "")
    script_data = {"topic": meta.get("topic"), "author": meta.get("author"), "script": meta.get("script"), "caption": caption, "hashtags": meta.get("hashtags", [])}
    voice_data = {"duration": meta.get("duration", 15), "provider": meta.get("voice_provider", "Unknown")}

    res = SocialPublisher.queue_post(str(video_p), script_data, voice_data)
    return res

@app.get("/media/{filename}")
def serve_media(filename: str):
    file_p = Config.OUTPUT_DIR / filename
    if not file_p.exists():
        raise HTTPException(status_code=404, detail="File not found")
    media_type = "video/mp4" if filename.endswith(".mp4") else "audio/mpeg"
    return FileResponse(file_p, media_type=media_type)

static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("studio.app:app", host="0.0.0.0", port=8000, reload=True)
