import codecs
import re

with codecs.open('frontend/src/pages/HomePage.tsx', 'r', 'utf-8') as f:
    text = f.read()

# Locate the box:
box_regex = re.compile(
    r'\{/\*\s*WHAT DO THESE NUMBERS MEAN.*?<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>.*?<div[^>]*>(.*?)</div>\s*</div>\s*</div>',
    re.DOTALL
)

def box_replacer(match):
    title = match.group(1).strip()
    desc = match.group(2).strip()
    inner_grid = match.group(3)
    
    # Extract the 5 cards
    card_regex = re.compile(r'<div[^>]*>(.*?)</div>', re.DOTALL)
    cards = card_regex.findall(inner_grid)
    
    # Restructure into short adjacent cards
    new_html = f'''{{/* RESTUCTURED BOX */}}
          <div className="mt-12">
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-bayyinah-dark-text mb-2">{title}</h3>
              <p className="text-base text-bayyinah-secondary-text">{desc}</p>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">'''
    
    for i, card_text in enumerate(cards):
        card_text = card_text.strip()
        if card_text:
            new_html += f'''
              <div className="group bg-white p-5 rounded-2xl border border-gray-100 hover:border-bayyinah-emerald/40 hover:shadow-subtle hover:-translate-y-1 transition-all duration-300">
                <span className="text-bayyinah-emerald font-bold mb-2 block text-lg">0{i+1}</span>
                <h4 className="text-bayyinah-dark-text font-bold text-sm leading-relaxed">{card_text}</h4>
              </div>'''
            
    new_html += '''
            </div>
          </div>'''
          
    return new_html

new_text = box_regex.sub(box_replacer, text)

with codecs.open('frontend/src/pages/HomePage.tsx', 'w', 'utf-8') as f:
    f.write(new_text)

print("Box restructured.")
