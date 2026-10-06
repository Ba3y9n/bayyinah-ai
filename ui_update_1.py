import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
html = html.replace('Readex Pro', 'Cairo').replace('Readex+Pro:wght@300;400;500;600;700', 'Cairo:wght@200..1000')
with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('frontend/tailwind.config.js', 'r', encoding='utf-8') as f:
    tw = f.read()
tw = tw.replace('"Readex Pro"', '"Cairo"')
with open('frontend/tailwind.config.js', 'w', encoding='utf-8') as f:
    f.write(tw)

with open('frontend/src/components/Navbar.tsx', 'r', encoding='utf-8') as f:
    nav = f.read()

# Fix encoding issues in Navbar
nav = nav.replace("label: 'ط§ظ„ط±ط¦ظٹط³ظٹط©'", "label: 'الرئيسية'")
nav = nav.replace("label: 'ط§ظ„طھط­ظ‚ظ‚'", "label: 'التحقق'")
nav = nav.replace("label: 'ط§ظ„ظ…طµط§ط¯ط± ط§ظ„ظ…ط¹طھظ…ط¯ط©'", "label: 'المصادر المعتمدة'")
nav = nav.replace("label: 'ط·ط¨ظ‚ط© ط§ظ„ط¨ط­ط« ظˆط§ظ„طھط­ظ‚ظ‚'", "label: 'طبقة البحث والتحقق'")
nav = nav.replace("label: 'ط­ط§ظ„ط© ط§ظ„ظ†ط¸ط§ظ…'", "label: 'حالة النظام'")
nav = nav.replace("alt=\"ط¨ظٹظ‘ظ†ط© AI\"", "alt=\"بيّنة AI\"")

# Center navigation
nav = nav.replace(
    '<nav className="hidden lg:flex items-center justify-center gap-8 absolute left-1/2 -translate-x-1/2">',
    '<nav className="hidden lg:flex flex-1 items-center justify-center gap-8">'
)
with open('frontend/src/components/Navbar.tsx', 'w', encoding='utf-8') as f:
    f.write(nav)

print("Navbar and Font updated.")

