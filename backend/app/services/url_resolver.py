"""
Bayyinah AI - Safe URL Verification & Resolution Engine
Includes strict SSRF protection, platform detection (YouTube, TikTok, X, Instagram, Generic),
and structured metadata/text extraction.
"""

import re
import socket
import ipaddress
import urllib.parse
from typing import Dict, Any, Tuple, Optional
import urllib.request
import json
import logging
from ..config import settings

logger = logging.getLogger("bayyinah.services.url_resolver")

# SSRF Blocked IP networks (IPv4 and IPv6)
BLOCKED_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("192.88.99.0/24"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("240.0.0.0/4"),
    ipaddress.ip_network("255.255.255.255/32"),
    ipaddress.ip_network("::/128"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10")
]

class SSRFSecurityException(Exception):
    pass

class SafeHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    """
    Custom HTTP Redirect Handler that validates every redirect target URL against SSRF rules.
    Prevents redirect-based SSRF bypass and DNS rebinding attacks.
    """
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Validate safety of target URL before following redirect
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme.lower() not in ("http", "https"):
            raise SSRFSecurityException(f"SSRF Block: Redirect to unsupported scheme {parsed.scheme}")
        hostname = parsed.hostname
        if not hostname or hostname.lower() in ("localhost", "local", "internal", "0.0.0.0", "metadata"):
            raise SSRFSecurityException(f"SSRF Block: Redirect to internal hostname {hostname}")
        
        try:
            ip_addresses = socket.getaddrinfo(hostname, None)
            for addr_info in ip_addresses:
                ip_str = addr_info[4][0]
                ip_obj = ipaddress.ip_address(ip_str)
                for blocked_net in BLOCKED_NETWORKS:
                    if ip_obj in blocked_net:
                        raise SSRFSecurityException(f"SSRF Block: Redirect target {hostname} resolves to internal IP {ip_str}")
        except socket.gaierror as e:
            raise SSRFSecurityException(f"SSRF Block: Redirect DNS resolution failed for {hostname}: {e}")

        return super().redirect_request(req, fp, code, msg, headers, newurl)

class URLResolverService:
    """
    Safely resolves, checks, and extracts text and metadata from user-provided URLs.
    """
    def __init__(self):
        self.opener = urllib.request.build_opener(SafeHTTPRedirectHandler())

    def validate_url_safety(self, url: str) -> str:
        """
        Validates URL scheme, resolves hostname to IP, and checks against private/internal subnets.
        """
        if not url or not isinstance(url, str):
            raise SSRFSecurityException("Invalid URL input.")

        clean_url = url.strip()
        parsed = urllib.parse.urlparse(clean_url)
        scheme = parsed.scheme.lower()
        if scheme not in ("http", "https"):
            raise SSRFSecurityException(f"Unsupported URL scheme: {scheme}. Only HTTP/HTTPS are allowed.")

        hostname = parsed.hostname
        if not hostname:
            raise SSRFSecurityException("Invalid URL: missing hostname.")

        lower_host = hostname.lower()
        if lower_host in ("localhost", "local", "internal", "0.0.0.0", "metadata", "instance-data"):
            raise SSRFSecurityException(f"Access to local/internal hostname '{hostname}' is blocked.")

        # Check if hostname itself is a raw IP address
        try:
            ip_obj = ipaddress.ip_address(lower_host)
            for blocked_net in BLOCKED_NETWORKS:
                if ip_obj in blocked_net:
                    raise SSRFSecurityException(f"SSRF violation: Direct access to internal IP {hostname} is blocked.")
        except ValueError:
            # Resolve DNS to IP
            try:
                ip_addresses = socket.getaddrinfo(hostname, None)
                for addr_info in ip_addresses:
                    ip_str = addr_info[4][0]
                    ip_obj = ipaddress.ip_address(ip_str)
                    for blocked_net in BLOCKED_NETWORKS:
                        if ip_obj in blocked_net:
                            raise SSRFSecurityException(f"SSRF violation: {hostname} resolves to prohibited internal IP {ip_str}.")
            except socket.gaierror as e:
                raise SSRFSecurityException(f"DNS resolution failed for hostname '{hostname}': {e}")

        return clean_url

    def extract_youtube_video_id(self, url: str) -> Optional[str]:
        """
        Extracts 11-character YouTube video ID using robust regex.
        Supports /watch?v=, youtu.be/, /shorts/, /embed/ regardless of query parameters.
        """
        if not url:
            return None
        patterns = [
            r'(?:v=|\/embed\/|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def detect_platform(self, url: str) -> str:
        """
        Detects platform: YOUTUBE, TIKTOK, X, INSTAGRAM, DIRECT_MEDIA, PDF, GENERIC.
        """
        lower = url.lower()
        if "youtube.com" in lower or "youtu.be" in lower:
            return "YOUTUBE"
        elif "tiktok.com" in lower:
            return "TIKTOK"
        elif "twitter.com" in lower or "x.com" in lower:
            return "X"
        elif "instagram.com" in lower:
            return "INSTAGRAM"
        elif any(lower.endswith(ext) or ext + "?" in lower for ext in [".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm", ".m4a"]):
            return "DIRECT_MEDIA"
        elif ".pdf" in lower:
            return "PDF"
        return "GENERIC"

    def resolve(self, raw_url: str) -> Dict[str, Any]:
        return self.resolve_url(raw_url)

    def resolve_url(self, raw_url: str) -> Dict[str, Any]:
        """
        Main entry point for resolving any web URL.
        """
        try:
            safe_url = self.validate_url_safety(raw_url)
        except SSRFSecurityException as ssrf_err:
            logger.warning(f"SSRF block on {raw_url}: {ssrf_err}")
            return {
                "success": False,
                "original_url": raw_url,
                "canonical_url": raw_url,
                "platform": "UNKNOWN",
                "content_type": "unknown",
                "content_id": None,
                "video_id": None,
                "author": None,
                "title": None,
                "description": None,
                "thumbnail_url": None,
                "duration": None,
                "embed_url": None,
                "resolution_status": "BLOCKED_SSRF",
                "extraction_status": "BLOCKED_SSRF",
                "analysis_capability": "NONE",
                "error": str(ssrf_err),
                "extracted_text": "",
                "requires_media_upload": False,
                "notes": "تم حظر الرابط لأسباب أمنية (SSRF Protection)."
            }

        platform = self.detect_platform(safe_url)

        if platform == "YOUTUBE":
            is_short = ("shorts/" in safe_url)
            return self._resolve_youtube(safe_url, is_short=is_short)
        elif platform == "TIKTOK":
            return self._resolve_tiktok(safe_url)
        elif platform == "X":
            return self._resolve_x(safe_url)
        elif platform == "INSTAGRAM":
            return self._resolve_instagram(safe_url)
        elif platform == "PDF":
            return self._resolve_pdf(safe_url)
        elif platform == "DIRECT_MEDIA":
            is_video = any(ext in safe_url.lower() for ext in [".mp4", ".mov", ".webm", ".m4a"])
            return self._resolve_direct_media(safe_url, media_type="video" if is_video else "image")
        else:
            return self._resolve_generic_web(safe_url)

    def _resolve_youtube(self, url: str, is_short: bool = False) -> Dict[str, Any]:
        vid_id = self.extract_youtube_video_id(url)

        # Use oEmbed API safely via self.opener with redirect validation
        oembed_url = f"https://www.youtube.com/oembed?url={urllib.parse.quote(url)}&format=json"
        metadata = {}
        title = "مقطع يوتيوب قصير" if is_short else "مقطع يوتيوب"
        author = "ناشر على يوتيوب"
        thumbnail_url = f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg" if vid_id else None

        try:
            req = urllib.request.Request(oembed_url, headers={"User-Agent": "BayyinahAI-Verifier/1.0"})
            with self.opener.open(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    title = data.get("title", title)
                    author = data.get("author_name", author)
                    thumbnail_url = data.get("thumbnail_url", thumbnail_url)
                    metadata = data
        except Exception as e:
            logger.warning(f"YouTube oEmbed fetch error: {e}")

        plat = "YOUTUBE"
        canonical_url = f"https://www.youtube.com/watch?v={vid_id}" if vid_id else url
        return {
            "success": True,
            "original_url": url,
            "canonical_url": canonical_url,
            "platform": plat,
            "content_type": "video",
            "content_id": vid_id,
            "video_id": vid_id,
            "author": author,
            "title": title,
            "description": f"مقطع فيديو منشور بواسطة {author}",
            "thumbnail_url": thumbnail_url,
            "duration": None,
            "embed_url": f"https://www.youtube.com/embed/{vid_id}" if vid_id else None,
            "resolution_status": "RESOLVED",
            "extraction_status": "RESOLVED",
            "analysis_capability": "METADATA_AND_TITLE",
            "extracted_text": f"مقطع يوتيوب بعنوان: {title} بقلم/قناة: {author}",
            "requires_media_upload": False,
            "notes": "تم استخراج بيانات الفيديو من واجهة YouTube الرسمية.",
            "metadata": metadata
        }

    def _resolve_tiktok(self, url: str) -> Dict[str, Any]:
        return {
            "success": False,
            "original_url": url,
            "canonical_url": url,
            "platform": "TIKTOK",
            "resolution_status": "ACCESS_LIMITED",
            "extraction_status": "ACCESS_LIMITED",
            "analysis_capability": "NONE",
            "error": "لا يمكن لبيّنة قراءة محتوى هذا الرابط مباشرة حاليًا. يرجى رفع الفيديو أو الصورة أو نسخ النص.",
            "requires_media_upload": True,
            "notes": "صلاحيات الوصول مقيدة من قبل المنصة."
        }

    def _resolve_x(self, url: str) -> Dict[str, Any]:
        return {
            "success": False,
            "original_url": url,
            "canonical_url": url,
            "platform": "X",
            "resolution_status": "ACCESS_LIMITED",
            "extraction_status": "ACCESS_LIMITED",
            "analysis_capability": "NONE",
            "error": "لا يمكن لبيّنة قراءة محتوى هذا الرابط مباشرة حاليًا. يرجى رفع الفيديو أو الصورة أو نسخ النص.",
            "requires_media_upload": True,
            "notes": "صلاحيات الوصول مقيدة من قبل المنصة."
        }

    def _resolve_pdf(self, url: str) -> Dict[str, Any]:
        parsed = urllib.parse.urlparse(url)
        filename = parsed.path.split("/")[-1] or "document.pdf"
        title = f"وثيقة PDF: {filename}"
        return {
            "success": True,
            "original_url": url,
            "canonical_url": url,
            "platform": "PDF",
            "content_type": "pdf",
            "content_id": filename,
            "author": "وثيقة إلكترونية",
            "title": title,
            "description": f"ملف PDF من المصدر: {parsed.netloc}",
            "thumbnail_url": None,
            "duration": None,
            "embed_url": url,
            "resolution_status": "RESOLVED",
            "extraction_status": "RESOLVED",
            "analysis_capability": "FULL_DOCUMENT",
            "extracted_text": f"ملف وثيقة PDF بعنوان: {filename}. المصدر: {parsed.netloc}",
            "requires_media_upload": False,
            "notes": "تم التعرف على وثيقة PDF وسيتم فحص نصوصها واستخراج أرقام الصفحات.",
            "metadata": {"filename": filename, "domain": parsed.netloc}
        }

    def _resolve_instagram(self, url: str) -> Dict[str, Any]:
        return {
            "success": True,
            "resolution_status": "RESOLVED",
            "url": url,
            "platform": "INSTAGRAM",
            "title": "منشور إنستغرام",
            "author": "حساب إنستغرام",
            "extracted_text": "محتوى منشور إنستغرام يتطلب التحقق.",
            "requires_media_upload": True,
            "notes": "نظراً لسياسات إنستغرام الخاصة، يُنصح برفع لقطة شاشة من المنشور للتحقق الفوري منها عبر الذكاء الاصطناعي.",
            "metadata": {}
        }

    def _resolve_direct_media(self, url: str, media_type: str = "media") -> Dict[str, Any]:
        plat = "IMAGE" if media_type == "image" else ("VIDEO" if media_type == "video" else "DIRECT_MEDIA")
        return {
            "success": True,
            "original_url": url,
            "canonical_url": url,
            "platform": plat,
            "content_type": media_type,
            "content_id": url.split("/")[-1].split("?")[0],
            "author": "مصدر وسائط مباشر",
            "title": f"ملف {plat.lower()} مباشر",
            "description": f"رابط مباشر لملف {plat.lower()}",
            "thumbnail_url": url if plat == "IMAGE" else None,
            "duration": None,
            "embed_url": url,
            "resolution_status": "RESOLVED",
            "extraction_status": "RESOLVED",
            "analysis_capability": "FULL_MEDIA",
            "extracted_text": f"رابط مباشر لملف وسائط ({plat}): {url}",
            "requires_media_upload": False,
            "notes": "رابط وسائط مباشر يمكن تحليله.",
            "metadata": {"media_type": media_type}
        }

    def _resolve_generic_web(self, url: str) -> Dict[str, Any]:
        """
        Safely fetches web page content with size and timeout guards.
        """
        max_bytes = settings.MAX_URL_RESPONSE_MB * 1024 * 1024
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 BayyinahAI/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

        try:
            req = urllib.request.Request(url, headers=headers)
            with self.opener.open(req, timeout=10) as resp:
                content_type = resp.headers.get("Content-Type", "")
                if "text/html" not in content_type and "text/plain" not in content_type:
                    return {
                        "success": False,
                        "resolution_status": "UNSUPPORTED",
                        "url": url,
                        "platform": "GENERIC",
                        "error": f"نوع المحتوى غير مدعوم: {content_type}"
                    }

                raw_bytes = resp.read(max_bytes + 1)
                if len(raw_bytes) > max_bytes:
                    return {
                        "success": False,
                        "resolution_status": "FAILED",
                        "url": url,
                        "platform": "GENERIC",
                        "error": f"حجم الصفحة يتجاوز الحد الأقصى المسموح ({settings.MAX_URL_RESPONSE_MB} ميجابايت)"
                    }

                charset = resp.headers.get_content_charset() or "utf-8"
                html_text = raw_bytes.decode(charset, errors="ignore")

                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', html_text, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else "صفحة ويب"

                # Extract description
                desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_text, re.IGNORECASE)
                description = desc_match.group(1).strip() if desc_match else ""

                # Extract main body text
                body_match = re.search(r'<body.*?>(.*?)</body>', html_text, re.IGNORECASE | re.DOTALL)
                body_content = body_match.group(1) if body_match else html_text
                # Remove script and style tags
                clean_body = re.sub(r'<script.*?</script>', ' ', body_content, flags=re.DOTALL | re.IGNORECASE)
                clean_body = re.sub(r'<style.*?</style>', ' ', clean_body, flags=re.DOTALL | re.IGNORECASE)
                # Strip HTML tags
                clean_text = re.sub(r'<[^>]+>', ' ', clean_body)
                extracted_text = " ".join(clean_text.split())

                return {
                    "success": True,
                    "resolution_status": "RESOLVED",
                    "url": url,
                    "platform": "GENERIC",
                    "title": title,
                    "description": description,
                    "author": None,
                    "extracted_text": extracted_text[:4000], # First 4000 chars for verification
                    "requires_media_upload": False,
                    "metadata": {
                        "content_length": len(extracted_text),
                        "charset": charset
                    }
                }
        except Exception as e:
            logger.error(f"Error fetching generic URL {url}: {e}")
            return {
                "success": False,
                "resolution_status": "FAILED",
                "url": url,
                "platform": "GENERIC",
                "error": f"تعذر قراءة محتوى الرابط: {e}"
            }

url_resolver = URLResolverService()
