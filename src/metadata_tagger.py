# src/metadata_tagger.py
import os
import sys
import pickle

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def infer_section_title(text: str) -> str:
    first_line = text.strip().split('\n')[0].strip()
    if 0 < len(first_line) < 60:
        return first_line
    return "General Context"

def tag_chunks():
    raw_chunks_path = os.path.join(config.CHUNKS_DIR, "raw_chunks.pkl")
    
    if not os.path.exists(raw_chunks_path):
        print(f"[-] Error: Raw chunks not found at {raw_chunks_path}")
        return

    with open(raw_chunks_path, "rb") as f:
        nodes = pickle.load(f)

    print(f"[+] Loaded {len(nodes)} chunks. Processing precise metadata mapping...\n")
    detected_files = set()
    tagged_count = 0

    for node in nodes:
        filename = node.metadata.get("original_file", "").lower()
        detected_files.add(node.metadata.get("original_file"))
        
        # Exact mapping for your 4 specific manuals
        if "model s" in filename:
            manufacturer = "Tesla"
            model = "Model S"
        elif "model y" in filename or "modely" in filename:
            manufacturer = "Tesla"
            model = "Model Y"
        elif "nexon" in filename:
            manufacturer = "Tata"
            model = "Nexon"
        elif "altroz" in filename:
            manufacturer = "Tata"
            model = "Altroz"
        else:
            manufacturer = "Unknown"
            model = "Unknown Model"

        node.metadata["source_manufacturer"] = manufacturer
        node.metadata["source_model"] = model
        node.metadata["document_type"] = "Owner's Manual"
        node.metadata["section_title"] = infer_section_title(node.text)

        node.excluded_embed_metadata_keys = [
            "original_file", 
            "source_manufacturer", 
            "source_model", 
            "document_type"
        ]
        tagged_count += 1

    tagged_chunks_path = os.path.join(config.CHUNKS_DIR, "tagged_chunks.pkl")
    with open(tagged_chunks_path, "wb") as f:
        pickle.dump(nodes, f)

    print("[+] File mapping verification:")
    for f_name in sorted(detected_files):
        f_lower = f_name.lower()
        mfg, mdl = "Unknown", "Unknown Model"
        if "model s" in f_lower: mfg, mdl = "Tesla", "Model S"
        elif "model y" in f_lower or "modely" in f_lower: mfg, mdl = "Tesla", "Model Y"
        elif "nexon" in f_lower: mfg, mdl = "Tata", "Nexon"
        elif "altroz" in f_lower: mfg, mdl = "Tata", "Altroz"
        print(f"    - '{f_name}' -> [{mfg} | {mdl}]")

if __name__ == "__main__":
    tag_chunks()