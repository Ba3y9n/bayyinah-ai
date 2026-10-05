import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.db.database import SessionLocal
from sqlalchemy import text

OFFICIAL_URLS = [
    "https://dawa.center",
    "https://islamic-content.com",
    "https://islamic-content.com/dictionary",
    "https://quranpedia.net",
    "https://dorar.net/tafseer",
    "https://dorar.net/hadith",
    "https://shamela.ws",
    "https://dorar.net/aqeeda",
    "https://dorar.net/feqhia",
    "https://dorar.net/history",
    "https://dawa.center/file/7937"
]

def main():
    with SessionLocal() as db:
        print("1. Updating check constraint on sources.scientific_status...")
        db.execute(text("ALTER TABLE sources DROP CONSTRAINT IF EXISTS sources_scientific_status_check;"))
        db.execute(text("""
            ALTER TABLE sources ADD CONSTRAINT sources_scientific_status_check 
            CHECK (scientific_status = ANY (ARRAY['APPROVED'::text, 'REVIEW_REQUIRED'::text, 'RESTRICTED'::text, 'DISABLED'::text, 'UNAPPROVED'::text]));
        """))
        
        print("2. Setting non-allowlist sources to UNAPPROVED...")
        db.execute(text("UPDATE sources SET scientific_status = 'UNAPPROVED', approved_by_challenge = false;"))
        
        print("3. Approving official 11 challenge sources...")
        for url in OFFICIAL_URLS:
            db.execute(text("""
                UPDATE sources 
                SET scientific_status = 'APPROVED', approved_by_challenge = true, is_active = true 
                WHERE url = :u OR official_url = :u;
            """), {"u": url})
            
        db.commit()
        
        rows = db.execute(text("SELECT id, name, url, scientific_status, approved_by_challenge FROM sources ORDER BY scientific_status ASC;")).fetchall()
        print(f"\nTotal sources in DB: {len(rows)}")
        for r in rows:
            status_tag = f"[{r[3]}]"
            print(f"  {status_tag:14} {r[2]} ({r[1]})")

if __name__ == "__main__":
    main()
