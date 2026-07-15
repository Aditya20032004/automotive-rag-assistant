# config.py
import os

# Project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Data Paths
RAW_MANUALS_DIR = os.path.join(ROOT_DIR, "data", "raw_manuals")
PROCESSED_DIR = os.path.join(ROOT_DIR, "data", "processed")
EXTRACTED_TEXT_DIR = os.path.join(PROCESSED_DIR, "extracted_text")
CHUNKS_DIR = os.path.join(PROCESSED_DIR, "chunks")

# Vector Store Path
VECTOR_STORE_DIR = os.path.join(ROOT_DIR, "vector_store")

# RAG Hyperparameters (OOM prevention for 6GB VRAM)
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
RETRIEVAL_TOP_K = 4

# Model Configurations
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "phi3:mini" # Ollama identifier

# Ensure directories exist on import
for path in [RAW_MANUALS_DIR, EXTRACTED_TEXT_DIR, CHUNKS_DIR, VECTOR_STORE_DIR]:
    os.makedirs(path, exist_ok=True)