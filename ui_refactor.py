import codecs
import re
import os

def update_file(path, replacements):
    try:
        with codecs.open(path, 'r', 'utf-8') as f:
            text = f.read()
        
        for old, new in replacements:
            if callable(old):
                text = old(text)
            else:
                text = text.replace(old, new)
        
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(text)
        print(f"Updated {path}")
    except Exception as e:
        print(f"Failed to update {path}: {e}")

# 1. Update Navbar.tsx
# Center items and remove "عرض الحكام"
update_file('frontend/src/components/Navbar.tsx', [
    (re.compile(r"\{\s*id:\s*'judge-demo',\s*label:[^\}]+\},?\s*"), ""),
    ('justify-between"', 'justify-between relative"'),
    ('hidden lg:flex items-center gap-8', 'hidden lg:flex items-center justify-center gap-8 absolute left-1/2 -translate-x-1/2')
])

# 2. Update HomePage.tsx
def clean_orbit_rings(text):
    # Remove orbit rings div
    text = re.sub(r'\{/\*\s*Background Orbit Rings\s*\*/\}[\s\S]*?(?=\{/\*\s*Orbit Nodes)', '', text)
    # Remove English text above verify
    text = re.sub(r'<span>Evidence-First Islamic Content Verification</span>', '', text)
    # Lighten Hero Background (from deep emerald to ivory/white with light emerald subtle tint)
    text = text.replace('bg-bayyinah-deep-emerald overflow-hidden', 'bg-bayyinah-ivory overflow-hidden border-b border-gray-100')
    text = text.replace('bg-bayyinah-deep-emerald/90', 'bg-white')
    text = text.replace('text-white', 'text-bayyinah-dark-text')
    text = text.replace('bg-[#042822]/80', 'bg-white')
    text = text.replace('text-white/70', 'text-bayyinah-secondary-text')
    # Make hover text readable
    text = text.replace("isActive ? 'text-white text-base drop-shadow-md' : 'text-white/70 text-xs'", "isActive ? 'text-bayyinah-emerald text-base drop-shadow-md font-bold' : 'text-bayyinah-secondary-text text-xs'")
    # Remove fatwa text completely
    text = re.sub(r'بيّنة نظام ذكاء اصطناعي للتحقق والمساعدة وليست جهة إفتاء', '', text)
    
    # Fix Orbit Card Background
    text = text.replace('bg-bayyinah-deep-emerald/95', 'bg-white')
    return text

update_file('frontend/src/pages/HomePage.tsx', [
    (clean_orbit_rings, "")
])

# 3. Clean up fatwa text globally just in case
for root, dirs, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith('.tsx') or file.endswith('.ts'):
            update_file(os.path.join(root, file), [
                ("بيّنة نظام ذكاء اصطناعي للتحقق والمساعدة وليست جهة إفتاء", "")
            ])

