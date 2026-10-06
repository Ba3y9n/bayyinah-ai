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
            elif hasattr(old, 'sub'):
                text = old.sub(new, text)
            else:
                text = text.replace(old, new)
        
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(text)
        print(f"Updated {path}")
    except Exception as e:
        print(f"Failed to update {path}: {e}")

# 1. Update Navbar.tsx
update_file('frontend/src/components/Navbar.tsx', [
    (re.compile(r"\{\s*id:\s*'judge-demo',\s*label:[^\}]+\},?\s*"), ""),
    ('justify-between"', 'justify-between relative"'),
    ('hidden lg:flex items-center gap-8', 'hidden lg:flex items-center justify-center gap-8 absolute left-1/2 -translate-x-1/2')
])
