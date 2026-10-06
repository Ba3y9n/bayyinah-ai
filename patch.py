import codecs
import re

with codecs.open('backend/app/services/evidence_gate.py', 'r', 'utf-8') as f:
    text = f.read()

new_validate_source = '''    @staticmethod
    def validate_source(source_id: Optional[str], source_url: Optional[str] = None) -> bool:
        """Validates that the source belongs to the official allowlist."""
        approved_map = {s["id"]: s for s in OFFICIAL_SOURCE_ALLOWLIST}
        
        is_id_approved = source_id and source_id in approved_map
        is_url_approved = source_url and is_url_in_allowlist(source_url)

        # Both must be present and valid. If URL is given, it must map to the same approved source ID.
        if source_id and source_url:
            if not (is_id_approved and is_url_approved):
                return False
            # Check domain match loosely
            expected_domain = approved_map[source_id].get("domain", "")
            if expected_domain and expected_domain not in source_url:
                return False
            return True
        elif source_id:
            return is_id_approved
        elif source_url:
            return is_url_approved
        return False'''

# Use regex to replace the old method
pattern = re.compile(r'    @staticmethod\s+def validate_source.*?return False', re.DOTALL)
text = pattern.sub(new_validate_source, text)

with codecs.open('backend/app/services/evidence_gate.py', 'w', 'utf-8') as f:
    f.write(text)
