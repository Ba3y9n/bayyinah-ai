import io
import sys
sys.path.append(".")
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw
from app.services.gemini_service import gemini_service

img = Image.new('RGB', (600, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((20, 80), "Hadith: Innama al-a'malu bin-niyyat", fill=(0, 0, 0))
buf = io.BytesIO()
img.save(buf, format='JPEG')
img_bytes = buf.getvalue()

res = gemini_service.extract_text_from_image(img_bytes)
print("Gemini raw OCR return:", repr(res))
