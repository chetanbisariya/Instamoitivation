import datetime
import json
import os
from pathlib import Path
import requests
from agent.config import Config

class SocialPublisher:
    @classmethod
    def publish_to_buffer(cls, video_path: str, caption: str) -> dict:
        access_token = Config.BUFFER_ACCESS_TOKEN
        profile_id = Config.BUFFER_PROFILE_ID

        if not access_token or not profile_id:
            return {
                "success": False,
                "provider": "Buffer",
                "message": "Buffer not configured. Set BUFFER_ACCESS_TOKEN and BUFFER_PROFILE_ID in .env."
            }

        url = "https://api.bufferapp.com/1/updates/create.json"
        headers = {"Authorization": f"Bearer {access_token}"}
        data = {
            "profile_ids[]": profile_id,
            "text": caption,
            "now": False,
            "shorten": False
        }

        try:
            res = requests.post(url, headers=headers, data=data, timeout=30)
            if res.status_code in [200, 201]:
                return {"success": True, "provider": "Buffer", "response": res.json()}
            else:
                return {"success": False, "provider": "Buffer", "error": f"Buffer API error: {res.status_code} - {res.text}"}
        except Exception as e:
            return {"success": False, "provider": "Buffer", "error": f"Buffer connection failed: {str(e)}"}

    @classmethod
    def dispatch_webhook(cls, payload: dict) -> dict:
        webhook_url = Config.WEBHOOK_URL
        if not webhook_url:
            return {"success": False, "provider": "Webhook", "message": "WEBHOOK_URL is not set in .env."}

        headers = {"Content-Type": "application/json", "User-Agent": "InstaMotivationAgent/2.0"}
        try:
            res = requests.post(webhook_url, headers=headers, json=payload, timeout=25)
            if res.status_code in [200, 201, 202, 204]:
                return {"success": True, "provider": "Webhook", "status_code": res.status_code}
            else:
                return {"success": False, "provider": "Webhook", "error": f"Webhook returned status code {res.status_code}"}
        except Exception as e:
            return {"success": False, "provider": "Webhook", "error": f"Webhook dispatch error: {str(e)}"}

    @classmethod
    def record_manifest(cls, video_path: str, script_data: dict, voice_data: dict, publish_status: str = "SAVED") -> dict:
        video_p = Path(video_path)
        manifest_path = video_p.with_suffix(".json")

        manifest = {
            "video_path": str(video_p.resolve()),
            "video_filename": video_p.name,
            "category": script_data.get("category", "MOTIVATION"),
            "topic": script_data.get("topic", "STORIES"),
            "author": script_data.get("author", "Unknown"),
            "avatar": script_data.get("avatar", Config.DEFAULT_AVATAR),
            "script": script_data.get("script", ""),
            "caption": script_data.get("caption", ""),
            "hashtags": script_data.get("hashtags", []),
            "duration": voice_data.get("duration", 0),
            "voice_name": voice_data.get("voice_name", "Neural Voice"),
            "voice_provider": voice_data.get("provider", "Unknown"),
            "created_at": datetime.datetime.now().isoformat(),
            "status": publish_status
        }

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        return manifest

    @classmethod
    def queue_post(cls, video_path: str, script_data: dict, voice_data: dict) -> dict:
        caption = script_data.get("caption", "")
        results = {
            "timestamp": datetime.datetime.now().isoformat(),
            "video_path": video_path,
            "buffer": None,
            "webhook": None,
            "status": "SAVED_LOCALLY"
        }

        if Config.BUFFER_ACCESS_TOKEN and Config.BUFFER_PROFILE_ID:
            buf_res = cls.publish_to_buffer(video_path, caption)
            results["buffer"] = buf_res
            if buf_res.get("success"):
                results["status"] = "QUEUED_TO_BUFFER"

        if Config.WEBHOOK_URL:
            webhook_payload = {
                "event": "daily_reel_ready",
                "video_path": os.path.abspath(video_path),
                "video_filename": os.path.basename(video_path),
                "category": script_data.get("category", "MOTIVATION"),
                "topic": script_data.get("topic"),
                "author": script_data.get("author"),
                "script": script_data.get("script"),
                "caption": caption,
                "hashtags": script_data.get("hashtags", []),
                "duration": voice_data.get("duration"),
                "created_at": datetime.datetime.now().isoformat()
            }
            wh_res = cls.dispatch_webhook(webhook_payload)
            results["webhook"] = wh_res
            if wh_res.get("success"):
                results["status"] = "DISPATCHED_TO_WEBHOOK"

        cls.record_manifest(video_path, script_data, voice_data, publish_status=results["status"])
        return results
