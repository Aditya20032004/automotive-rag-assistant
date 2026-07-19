# src/clean.py
import os
import re
import sys

# Allow importing config from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.logger import get_logger
logger = get_logger("clean")
def clean_text(text: str) -> str:
    """
    Applies regex patterns to remove PDF extraction artifacts and normalize whitespace.
    """
    # 1. Remove the page break markers from Step 2
    text = re.sub(r'\n\n---PAGE_BREAK---\n\n', '\n\n', text)
    
    # 2. Fix hyphenated words broken across lines (e.g., "mechan-\nical" -> "mechanical")
    text = re.sub(r'([a-zA-Z]+)-\n([a-zA-Z]+)', r'\1\2', text)
    
    # 3. Remove isolated page numbers (lines that consist only of 1 to 3 digits)
    text = re.sub(r'(?m)^\s*\d{1,3}\s*$', '', text)
    
    # 4. Normalize excessive newlines (replace 3+ consecutive newlines with exactly 2)
    # This preserves paragraph breaks but condenses massive white gaps.
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 5. Replace multiple horizontal spaces (or tabs) with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def clean_all_manuals():
    if not os.path.exists(config.EXTRACTED_TEXT_DIR):
        logger.info(f"[-] Error: Extracted text directory not found at {config.EXTRACTED_TEXT_DIR}")
        return

    txt_files = [f for f in os.listdir(config.EXTRACTED_TEXT_DIR) if f.endswith(".txt") and not f.endswith("_clean.txt")]
    
    if not txt_files:
        logger.info("[!] No raw .txt files found to clean.")
        return

    logger.info(f"[+] Found {len(txt_files)} text file(s) to clean.\n")

    for filename in txt_files:
        input_path = os.path.join(config.EXTRACTED_TEXT_DIR, filename)
        clean_filename = filename.replace(".txt", "_clean.txt")
        output_path = os.path.join(config.EXTRACTED_TEXT_DIR, clean_filename)

        logger.info(f"[*] Cleaning: {filename}...")
        
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
                
            original_len = len(raw_text)
            cleaned_text = clean_text(raw_text)
            cleaned_len = len(cleaned_text)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)
                
            reduction = original_len - cleaned_len
            logger.info(f"[+] Saved {clean_filename} (Removed {reduction} characters of noise)\n")
            
        except Exception as e:
            logger.info(f"[-] Failed to clean {filename}: {str(e)}\n")

if __name__ == "__main__":
    clean_all_manuals()