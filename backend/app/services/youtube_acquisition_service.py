"""
Bayyinah AI - YouTube Social Content Acquisition Service (Phase 4)

Responsible ONLY for acquiring YouTube content (metadata, transcripts/captions, or media fallback).
All acquired content is strictly labeled as USER_SOCIAL_CONTENT (untrusted user content).
Does NOT perform religious reasoning, retrieval, or evidence verification.
"""

import os
import json
import re
import urllib.parse
import urllib.request
import logging
from typing import Dict, Any, Optional, List
from ..config import settings
from .url_resolver import url_resolver, SSRFSecurityException

logger = logging.getLogger("bayyinah.services.youtube_acquisition")

class YouTubeAcquisitionService:
    """
    Acquires YouTube metadata, captions/transcript, or audio stream for verification.
    Submits claims to Phase 3 Video Understanding & Phase 1 Verification Retrieval.
    """

    def acquire_youtube_content(self, url: str) -> Dict[str, Any]:
        """
        Main entry point to acquire content from a YouTube URL.
        Returns acquired metadata, transcripts/claims, or flags if direct video upload is required.
        """
        # Validate SSRF safety & extract video ID
        safe_url = url_resolver.validate_url_safety(url)
        video_id = url_resolver.extract_youtube_video_id(safe_url)

        if not video_id:
            return {
                "success": False,
                "error": "تعذر استخراج معرّف فيديو YouTube صحيح من الرابط المدخل.",
                "platform": "YOUTUBE",
                "resolution_status": "FAILED"
            }

        canonical_url = f"https://www.youtube.com/watch?v={video_id}"

        # 1. Acquire Metadata via oEmbed
        meta_res = url_resolver._resolve_youtube(safe_url)
        title = meta_res.get("title") or "مقطع يوتيوب"
        author = meta_res.get("author") or "ناشر على يوتيوب"
        thumbnail_url = meta_res.get("thumbnail_url")

        # 2. Acquire Transcript / Captions
        transcript_data = self._fetch_youtube_captions(video_id)
        
        claims_list = []
        has_transcript = False
        full_transcript = ""

        if transcript_data.get("success") and transcript_data.get("transcript_items"):
            has_transcript = True
            raw_items = transcript_data["transcript_items"]
            full_transcript = " ".join([item.get("text", "") for item in raw_items])
            
            # Chunk transcript into timestamped segments (each ~20-30 seconds or grouped sentences)
            claims_list = self._segment_transcript_into_claims(raw_items, video_id, canonical_url, title, author)

        return {
            "success": True,
            "platform": "YOUTUBE",
            "video_id": video_id,
            "canonical_url": canonical_url,
            "title": title,
            "author": author,
            "thumbnail_url": thumbnail_url,
            "has_transcript": has_transcript,
            "transcript": full_transcript,
            "claims": claims_list,
            "provenance_type": "USER_SOCIAL_CONTENT",
            "acquisition_method": "CAPTIONS" if has_transcript else "METADATA_ONLY",
            "notes": "المحتوى مستخرج من YouTube كـ USER_SOCIAL_CONTENT لتسهيل التحقق."
        }

    def _fetch_youtube_captions(self, video_id: str) -> Dict[str, Any]:
        """
        Attempts to fetch public Arabic or multi-language YouTube captions/subtitles via YouTube timedtext API.
        """
        # Try official YouTube timedtext tracks listing
        timedtext_list_url = f"https://www.youtube.com/api/timedtext?type=list&v={video_id}"
        try:
            req = urllib.request.Request(timedtext_list_url, headers={"User-Agent": "Mozilla/5.0 BayyinahAI/1.0"})
            with url_resolver.opener.open(req, timeout=5) as resp:
                xml_content = resp.read().decode("utf-8", errors="ignore")
                
                # Check for Arabic track ('ar') or auto-generated track
                lang_code = None
                if 'lang_code="ar"' in xml_content:
                    lang_code = "ar"
                elif 'lang_code="' in xml_content:
                    # Match first available language code
                    match = re.search(r'lang_code="([^"]+)"', xml_content)
                    if match:
                        lang_code = match.group(1)

                if lang_code:
                    caption_url = f"https://www.youtube.com/api/timedtext?v={video_id}&lang={lang_code}&fmt=json3"
                    creq = urllib.request.Request(caption_url, headers={"User-Agent": "Mozilla/5.0 BayyinahAI/1.0"})
                    with url_resolver.opener.open(creq, timeout=5) as cresp:
                        cdata = json.loads(cresp.read().decode("utf-8"))
                        events = cdata.get("events", [])
                        parsed_items = []
                        for ev in events:
                            segs = ev.get("segs")
                            if not segs:
                                continue
                            start_ms = ev.get("tStartMs", 0)
                            dur_ms = ev.get("dDurationMs", 0)
                            text = "".join([s.get("utf8", "") for s in segs if s.get("utf8")]).strip()
                            if text and text != "\n":
                                start_sec = start_ms // 1000
                                end_sec = (start_ms + dur_ms) // 1000
                                parsed_items.append({
                                    "start": self._format_seconds(start_sec),
                                    "end": self._format_seconds(end_sec),
                                    "start_sec": start_sec,
                                    "end_sec": end_sec,
                                    "text": text
                                })
                        if parsed_items:
                            return {"success": True, "language": lang_code, "transcript_items": parsed_items}
        except Exception as e:
            logger.info(f"YouTube timedtext API notice for video {video_id}: {e}")

        # Try youtube-transcript-api if installed
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            api_instance = YouTubeTranscriptApi()
            transcript_list = api_instance.fetch(video_id, languages=['ar', 'en'])
            parsed_items = []
            for item in transcript_list:
                start_sec = int(item.get("start", 0))
                dur_sec = int(item.get("duration", 0))
                parsed_items.append({
                    "start": self._format_seconds(start_sec),
                    "end": self._format_seconds(start_sec + dur_sec),
                    "start_sec": start_sec,
                    "end_sec": start_sec + dur_sec,
                    "text": item.get("text", "").strip()
                })
            if parsed_items:
                return {"success": True, "language": "auto", "transcript_items": parsed_items}
        except Exception:
            pass

        return {"success": False, "transcript_items": []}

    def _segment_transcript_into_claims(
        self, 
        raw_items: List[Dict[str, Any]], 
        video_id: str, 
        canonical_url: str,
        video_title: str,
        channel_title: str
    ) -> List[Dict[str, Any]]:
        """
        Groups transcript items into 20-40 second timestamped segments for claim extraction.
        """
        claims = []
        current_texts = []
        start_sec = raw_items[0]["start_sec"] if raw_items else 0
        last_end_sec = start_sec

        for item in raw_items:
            current_texts.append(item["text"])
            last_end_sec = item["end_sec"]

            # Group every 30 seconds or when text ends with a period/question mark
            if (last_end_sec - start_sec >= 25) or (len(" ".join(current_texts)) > 200):
                segment_text = " ".join(current_texts).strip()
                if len(segment_text) >= 15:
                    claims.append({
                        "platform": "YOUTUBE",
                        "video_id": video_id,
                        "canonical_url": canonical_url,
                        "video_title": video_title,
                        "channel_title": channel_title,
                        "timestamp_start": self._format_seconds(start_sec),
                        "timestamp_end": self._format_seconds(last_end_sec),
                        "extracted_excerpt": segment_text[:300],
                        "claim_text": segment_text[:250],
                        "content_type": "GeneralClaim"
                    })
                current_texts = []
                start_sec = last_end_sec

        if current_texts:
            segment_text = " ".join(current_texts).strip()
            if len(segment_text) >= 15:
                claims.append({
                    "platform": "YOUTUBE",
                    "video_id": video_id,
                    "canonical_url": canonical_url,
                    "video_title": video_title,
                    "channel_title": channel_title,
                    "timestamp_start": self._format_seconds(start_sec),
                    "timestamp_end": self._format_seconds(last_end_sec),
                    "extracted_excerpt": segment_text[:300],
                    "claim_text": segment_text[:250],
                    "content_type": "GeneralClaim"
                })

        return claims

    def _format_seconds(self, total_seconds: int) -> str:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

youtube_acquisition_service = YouTubeAcquisitionService()
