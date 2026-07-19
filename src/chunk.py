# src/chunk.py
import os
import sys
import pickle
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from src.logger import get_logger
logger=get_logger("chunk") 

# Allow importing config from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def generate_chunks():
    """
    Reads cleaned text files, chunks them using SentenceSplitter, 
    and saves the raw LlamaIndex TextNodes to disk for metadata tagging.
    """
    if not os.path.exists(config.EXTRACTED_TEXT_DIR):
        logger.info(f"[-] Error: Extracted text directory not found at {config.EXTRACTED_TEXT_DIR}")
        return

    clean_files = [f for f in os.listdir(config.EXTRACTED_TEXT_DIR) if f.endswith("_clean.txt")]
    
    if not clean_files:
        logger.info("[!] No _clean.txt files found. Please run src/clean.py first.")
        return

    logger.info(f"[+] Found {len(clean_files)} clean text file(s).")
    logger.info(f"[*] Chunking at size {config.CHUNK_SIZE}, overlap {config.CHUNK_OVERLAP}...\n")

    # Initialize the LlamaIndex splitter
    splitter = SentenceSplitter(
        chunk_size=config.CHUNK_SIZE, 
        chunk_overlap=config.CHUNK_OVERLAP
    )

    all_nodes = []

    for filename in clean_files:
        filepath = os.path.join(config.EXTRACTED_TEXT_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            
        # Wrap the text in a LlamaIndex Document
        doc = Document(text=text, metadata={"original_file": filename})
        
        # Parse the document into a list of TextNode objects
        nodes = splitter.get_nodes_from_documents([doc])
        all_nodes.extend(nodes)
        
        logger.info(f"[+] {filename} -> Generated {len(nodes)} chunks.")

    # Save the raw chunks to a pickle file so Step 5 can add metadata
    output_path = os.path.join(config.CHUNKS_DIR, "raw_chunks.pkl")
    with open(output_path, "wb") as f:
        pickle.dump(all_nodes, f)
        
    logger.info(f"\n[+] Successfully saved {len(all_nodes)} total chunks to {output_path}")

if __name__ == "__main__":
    generate_chunks()