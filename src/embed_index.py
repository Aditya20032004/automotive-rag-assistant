# src/embed_index.py
import os
import sys
import pickle
import chromadb

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.logger import get_logger
logger=get_logger("embed_index")
# Allow importing config from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def build_vector_index():
    tagged_chunks_path = os.path.join(config.CHUNKS_DIR, "tagged_chunks.pkl")
    
    if not os.path.exists(tagged_chunks_path):
        logger.info(f"[-] Error: Tagged chunks not found at {tagged_chunks_path}")
        return

    logger.info("[*] Loading tagged chunks...")
    with open(tagged_chunks_path, "rb") as f:
        nodes = pickle.load(f)

    logger.info(f"[+] Loaded {len(nodes)} chunks.")
    
    # 1. Initialize the embedding model
    logger.info(f"[*] Loading embedding model: {config.EMBEDDING_MODEL_NAME}...")
    embed_model = HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL_NAME)

    # 2. Setup ChromaDB client and collection
    logger.info(f"[*] Initializing ChromaDB at {config.VECTOR_STORE_DIR}...")
    db = chromadb.PersistentClient(path=config.VECTOR_STORE_DIR)
    chroma_collection = db.get_or_create_collection("auto_manuals")
    
    # 3. Create the vector store and storage context
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # 4. Initialize an empty VectorStoreIndex 
    # We pass the embed_model here so it knows how to convert text to vectors
    logger.info("[*] Creating empty index structure...")
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model,
    )

    # 5. Batched embedding and insertion to prevent OOM
    batch_size = 64
    total_batches = (len(nodes) + batch_size - 1) // batch_size
    
    logger.info(f"[*] Beginning batched ingestion (Batch Size: {batch_size}, Total Batches: {total_batches})")
    
    for i in range(0, len(nodes), batch_size):
        batch = nodes[i : i + batch_size]
        batch_num = (i // batch_size) + 1
        
        logger.info(f"    -> Embedding and inserting batch {batch_num}/{total_batches}...")
        index.insert_nodes(batch)

    logger.info("\n[+] Indexing complete! ChromaDB is now populated and saved to disk.")
    logger.info(f"[+] Total documents in Chroma collection: {chroma_collection.count()}")

if __name__ == "__main__":
    build_vector_index()