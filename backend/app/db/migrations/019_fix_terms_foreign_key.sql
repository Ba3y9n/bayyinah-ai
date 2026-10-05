-- Migration 019: Fix terms foreign key to reference canonical sources table
ALTER TABLE terms DROP CONSTRAINT IF EXISTS terms_source_id_fkey;

-- Convert source_id column to UUID safely
ALTER TABLE terms ALTER COLUMN source_id TYPE UUID USING 
    CASE 
        WHEN source_id IS NOT NULL AND source_id ~ '^[0-9a-fA-F-]{36}$' THEN source_id::uuid 
        ELSE NULL 
    END;

-- Re-add foreign key constraint pointing to canonical sources table
ALTER TABLE terms ADD CONSTRAINT terms_source_id_fkey FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE SET NULL;
