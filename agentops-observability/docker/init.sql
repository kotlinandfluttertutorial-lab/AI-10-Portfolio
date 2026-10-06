-- PostgreSQL initialisation script run once when the container is first created.
-- Creates the application database and enables the pgvector extension.

CREATE DATABASE agentops;
\c agentops;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- pgvector is not required for P05 (no vector search), but enabled for consistency.
-- CREATE EXTENSION IF NOT EXISTS vector;
