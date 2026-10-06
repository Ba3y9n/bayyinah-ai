import codecs
with codecs.open('backend/app/services/tiktok_acquisition_service.py', 'r', 'utf-8') as f:
    text = f.read()

text = text.replace("from .url_resolver import url_resolver", "")

old_code = """        video_id = self.extract_video_id(url)
        oembed_res = url_resolver.resolve(url)

        if self.has_display_api_access:"""

new_code = """        video_id = self.extract_video_id(url)
        oembed_title = "محتوى تيك توك"
        oembed_author = "مستخدم"
        try:
            import urllib.parse, requests
            oembed_url = f"https://www.tiktok.com/oembed?url={urllib.parse.quote(url)}"
            res = requests.get(oembed_url, timeout=5)
            if res.ok:
                data = res.json()
                oembed_title = data.get("title", oembed_title)
                oembed_author = data.get("author_name", oembed_author)
        except Exception:
            pass

        if self.has_display_api_access:"""

text = text.replace(old_code, new_code)
text = text.replace('getattr(oembed_res, "title", "غير محدد")', 'oembed_title')
text = text.replace('getattr(oembed_res, "author", "user")', 'oembed_author')
text = text.replace('oembed_res.title', 'oembed_title')
text = text.replace('oembed_res.author', 'oembed_author')

with codecs.open('backend/app/services/tiktok_acquisition_service.py', 'w', 'utf-8') as f:
    f.write(text)
