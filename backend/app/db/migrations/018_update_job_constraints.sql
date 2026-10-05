-- Migration 018: Relax ingestion_jobs constraints to support Autonomous Knowledge Acquisition Engine jobs
ALTER TABLE ingestion_jobs DROP CONSTRAINT IF EXISTS ingestion_jobs_job_type_check;
ALTER TABLE ingestion_jobs DROP CONSTRAINT IF EXISTS ingestion_jobs_status_check;

ALTER TABLE ingestion_jobs ADD CONSTRAINT ingestion_jobs_job_type_check CHECK (
    job_type IN (
        'FULL', 'INCREMENTAL', 'REINDEX', 'EMBEDDING_ONLY',
        'DISCOVER_SOURCE', 'FETCH_DOCUMENT', 'EXTRACT_DOCUMENT',
        'NORMALIZE_DOCUMENT', 'DEDUPLICATE_DOCUMENT', 'CHUNK_DOCUMENT',
        'GENERATE_EMBEDDINGS', 'VALIDATE_EVIDENCE', 'PUBLISH_DOCUMENT',
        'REVERIFY_DOCUMENT', 'HEALTH_CHECK_SOURCE', 'DISCOVER_AND_EXPAND',
        'BATCH_INGEST'
    )
);

ALTER TABLE ingestion_jobs ADD CONSTRAINT ingestion_jobs_status_check CHECK (
    status IN (
        'QUEUED', 'RUNNING', 'PROCESSING', 'COMPLETED', 'SUCCESS',
        'FAILED', 'RETRYING', 'REVIEW_REQUIRED', 'DEAD_LETTER', 'INDEXED'
    )
);
