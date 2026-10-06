import codecs
import re

with codecs.open('frontend/src/pages/HomePage.tsx', 'r', 'utf-8') as f:
    text = f.read()

# 1. Update HowItWorks component (Timeline)
# "استخدم خطًا إرشاديًا أو أسهمًا لبيان ترتيب الخطوات"
# The timeline currently has a line `<div className="absolute top-1/2 left-0 right-0 h-px bg-gray-200 -translate-y-1/2 z-0 min-w-[800px]"></div>`
# I'll update it to be interactive and accessible.
how_it_works_replace = [
    ('min-w-[800px]"></div>', 'min-w-[800px]"></div>\n        <div className="absolute top-1/2 right-0 h-0.5 bg-bayyinah-emerald -translate-y-1/2 z-0 transition-all duration-500 ease-out" style={{ width: `${(activeTab / (steps.length - 1)) * 100}%`, minWidth: \'0\' }}></div>'),
    ('className="relative z-10 flex flex-col items-center gap-3 min-w-[120px] cursor-pointer group"', 'className="relative z-10 flex flex-col items-center gap-3 min-w-[120px] cursor-pointer group focus:outline-none focus:ring-2 focus:ring-bayyinah-emerald/50 rounded-lg p-2" aria-selected={isActive} role="tab"'),
    ('div className="relative mb-12 flex items-center justify-between overflow-x-auto pb-6 hide-scrollbar"', 'div className="relative mb-12 flex items-center justify-between overflow-x-auto pb-6 hide-scrollbar" role="tablist"'),
]

# 2. Update WhyBayyinah component
why_bayyinah_replace = [
    ('bg-white p-6 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald/30', 'bg-white p-8 rounded-3xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300 group focus-within:ring-2 focus-within:ring-bayyinah-emerald'),
    ('text-bayyinah-emerald group-hover:scale-110', 'text-bayyinah-emerald transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3'),
]

for old, new in how_it_works_replace + why_bayyinah_replace:
    text = text.replace(old, new)

with codecs.open('frontend/src/pages/HomePage.tsx', 'w', 'utf-8') as f:
    f.write(text)

print("Updated sections")
