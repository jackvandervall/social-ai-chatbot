-- Enable the pgvector extension to work with embedding vectors
create extension if not exists vector;

-- Create the knowledge base table for storing RAG documents
create table knowledge_base (
  id bigserial primary key,
  content text,
  metadata jsonb,
  source_url text,
  source_type text,
  embedding vector(1536)
);

-- Create a function to search for documents
create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  source_url text,
  source_type text,
  similarity float
) language sql stable as $$
  select
    knowledge_base.id,
    knowledge_base.content,
    knowledge_base.metadata,
    knowledge_base.source_url,
    knowledge_base.source_type,
    1 - (knowledge_base.embedding <=> query_embedding) as similarity
  from knowledge_base
  where 1 - (knowledge_base.embedding <=> query_embedding) > match_threshold
  order by knowledge_base.embedding <=> query_embedding
  limit match_count;
$$;
