# src/debug_meta.py
import os
import sys
import pickle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def inspect_pickle_metadata():
    raw_path = os.path.join(config.CHUNKS_DIR, "raw_chunks.pkl")
    tagged_path = os.path.join(config.CHUNKS_DIR, "tagged_chunks.pkl")
    
    if os.path.exists(raw_path):
        with open(raw_path, "rb") as f:
            raw_nodes = pickle.load(f)
        print(f"[Raw Chunks] Total: {len(raw_nodes)}")
        if raw_nodes:
            print(f"[Raw Chunks] Sample metadata keys: {list(raw_nodes[0].metadata.keys())}")
            print(f"[Raw Chunks] Sample 'original_file' value: {raw_nodes[0].metadata.get('original_file')}\n")
            
    if os.path.exists(tagged_path):
        with open(tagged_path, "rb") as f:
            tagged_nodes = pickle.load(f)
        print(f"[Tagged Chunks] Total: {len(tagged_nodes)}")
        if tagged_nodes:
            print(f"[Tagged Chunks] Sample full metadata: {tagged_nodes[0].metadata}")

if __name__ == "__main__":
    inspect_pickle_metadata()