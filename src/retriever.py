# src/retriever.py
import os
import sys
import chromadb

from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter

from src.logger import get_logger
logger=get_logger("retriever")
# Allow importing config from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_retriever(manufacturer: str = None, model: str = None):
    """
    Reconnects to ChromaDB and returns a LlamaIndex retriever.
    Dynamically applies exact-match metadata filters if manufacturer/model are provided.
    """
    # 1. Initialize the embedding model (needed to convert the search query into a vector)
    embed_model = HuggingFaceEmbedding(
        model_name=config.EMBEDDING_MODEL_NAME
    )
    Settings.embed_model = embed_model
    Settings.llm = None  # We only need retrieval for this step, no generation yet
    
    # 2. Connect to the existing Chroma DB on disk
    if not os.path.exists(config.VECTOR_STORE_DIR):
        raise FileNotFoundError(f"Vector store not found at {config.VECTOR_STORE_DIR}. Run embed_index.py first.")
        
    db = chromadb.PersistentClient(path=config.VECTOR_STORE_DIR)
    chroma_collection = db.get_collection("auto_manuals")
    
    # 3. Mount LlamaIndex on top of Chroma
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=embed_model
    )
    
    # 4. Construct Metadata Filters if requested
    filters = []
    if manufacturer:
        filters.append(MetadataFilter(key="source_manufacturer", value=manufacturer))
    if model:
        filters.append(MetadataFilter(key="source_model", value=model))
        
    if filters:
        metadata_filters = MetadataFilters(filters=filters)
        retriever = index.as_retriever(
            similarity_top_k=config.RETRIEVAL_TOP_K,
            filters=metadata_filters
        )
    else:
        retriever = index.as_retriever(
            similarity_top_k=config.RETRIEVAL_TOP_K
        )
        
    return retriever

if __name__ == "__main__":
    # ---------------------------------------------------------
    # TEST BLOCK
    # ---------------------------------------------------------
    logger.info("[*] Testing general retriever (No Filters)...")
    base_retriever = get_retriever()
    general_nodes = base_retriever.retrieve("How do I replace the key fob battery?")
    
    logger.info(f"[+] Retrieved {len(general_nodes)} chunks. Sources:")
    for n in general_nodes:
        # Displaying the metadata to prove what we pulled
        logger.info(f"    - {n.metadata.get('source_manufacturer')} {n.metadata.get('source_model')} | {n.metadata.get('section_title')}")
        
    logger.info("\n[*] Testing targeted retriever (Filter: Tata Nexon EV)...")
    ev_retriever = get_retriever(manufacturer="Tata", model="Nexon EV")
    ev_nodes = ev_retriever.retrieve("What is the high voltage battery capacity?")
    
    logger.info(f"[+] Retrieved {len(ev_nodes)} chunks. Sources:")
    for n in ev_nodes:
        logger.info(f"    - {n.metadata.get('source_manufacturer')} {n.metadata.get('source_model')} | {n.metadata.get('section_title')}")