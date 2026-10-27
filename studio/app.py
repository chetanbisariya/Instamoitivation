import datetime
import glob
import json
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent.config import Config
from agent.runner import DailyReelAgent
from agent.publisher import SocialPublisher

app = FastAPI(title="Instagram Motivation Agent Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = DailyReelAgent()

class GenerateRequest(BaseModel):
    topic: str = ""
    prompt: str = ""

class ConfigUpdateRequest(BaseModel):
    instagram_handle: str = ""
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = ""
    buffer_access_token: str = ""
    buffer_profile_id: str = ""
    webhook_url: str = ""
    gemini_api_key: str = ""
    schedule_time: str = ""

@app.get("/api/config")
def get_config():
    return {
        "instagram_handle": Config.INSTAGRAM_HANDLE,
        "default_topic": Config.DEFAULT_TOPIC,
        "elevenlabs_configured": bool(Config.ELEVENLABS_API_KEY),
        "elevenlabs_voice_id": Config.ELEVENLABS_VOICE_ID,
        "fallback_voice": Config.FALLBACK_TTS_VOICE,
        "gemini_configured": bool(Config.GEMINI_API_KEY),
        "buffer_configured": bool(Config.BUFFER_ACCESS_TOKEN and Config.BUFFER_PROFILE_ID),
        "webhook_configured": bool(Config.WEBHOOK_URL),
        "webhook_url": Config.WEBHOOK_URL,
        "schedule_time": Config.SCHEDULE_TIME,
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
    if req.elevenlabs_api_key: updates["ELEVENLABS_API_KEY"] = req.elevenlabs_api_key
    if req.elevenlabs_voice_id: updates["ELEVENLABS_VOICE_ID"] = req.elevenlabs_voice_id
    if req.buffer_access_token: updates["BUFFER_ACCESS_TOKEN"] = req.buffer_access_token
    if req.buffer_profile_id: updates["BUFFER_PROFILE_ID"] = req.buffer_profile_id
    if req.webhook_url: updates["WEBHOOK_URL"] = req.webhook_url
    if req.gemini_api_key: updates["GEMINI_API_KEY"] = req.gemini_api_key
    if req.schedule_time: updates["SCHEDULE_TIME"] = req.schedule_time

    # Update or append
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

    # Reload in-memory
    if req.instagram_handle: Config.INSTAGRAM_HANDLE = req.instagram_handle
    if req.elevenlabs_api_key: Config.ELEVENLABS_API_KEY = req.elevenlabs_api_key
    if req.elevenlabs_voice_id: Config.ELEVENLABS_VOICE_ID = req.elevenlabs_voice_id
    if req.buffer_access_token: Config.BUFFER_ACCESS_TOKEN = req.buffer_access_token
    if req.buffer_profile_id: Config.BUFFER_PROFILE_ID = req.buffer_profile_id
    if req.webhook_url: Config.WEBHOOK_URL = req.webhook_url
    if req.gemini_api_key: Config.GEMINI_API_KEY = req.gemini_api_key
    if req.schedule_time: Config.SCHEDULE_TIME = req.schedule_time

    return {"success": True, "message": "Configuration updated successfully."}

@app.get("/api/reels")
def list_reels():
    """Lists all generated reels with their manifest metadata."""
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
            "topic": meta.get("topic", "MOTIVATION"),
            "author": meta.get("author", "Daily Stoic"),
            "script": meta.get("script", ""),
            "caption": meta.get("caption", ""),
            "hashtags": meta.get("hashtags", []),
            "duration": meta.get("duration", 0),
            "status": meta.get("status", "SAVED_LOCALLY")
        })
    return reels

@app.post("/api/generate")
def generate_reel(req: GenerateRequest):
    try:
        result = agent.run_pipeline(topic=req.topic, custom_prompt=req.prompt)
        return {
            "success": True,
            "reel": {
                "filename": result["video_filename"],
                "url": f"/media/{result['video_filename']}",
                "topic": result["script_data"].get("topic"),
                "author": result["script_data"].get("author"),
                "caption": result["script_data"].get("caption"),
                "script": result["script_data"].get("script"),
                "hashtags": result["script_data"].get("hashtags", []),
                "duration": result["voice_data"].get("duration"),
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

# Serve static frontend files
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("studio.app:app", host="0.0.0.0", port=8000, reload=True)
