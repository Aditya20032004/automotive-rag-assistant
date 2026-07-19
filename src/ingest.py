# converts raw ppdf manuals into processed text reuired foor chunking, embedding, searching, tokenising, etc

import os
import fitz
import sys
from src.logger import get_logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
logger = get_logger("ingest")
def extract_text_from_pdf():
    if not os.path.exists(config.RAW_MANUALS_DIR):
        print(f"Dir not found")
        return
    pdf_file=[f for f in os.listdir(config.RAW_MANUALS_DIR) if f.lower().endswith('.pdf')]
    if not pdf_file:
        print(f"warning no pdf filles found in path raw manuals")
        logger.info("pdf files empty")
        return
    logger.info(f"Found {len(pdf_file)} in the raw manuals")
    for filename in pdf_file:
        filepath=os.path.join(config.RAW_MANUALS_DIR,filename)
        output_filename=os.path.splitext(filename)[0]+".txt"
        output_filename_path=os.path.join(config.EXTRACTED_TEXT_DIR,output_filename)
        logger.info(f"Processing file :: {filename}")
        try:
            doc=fitz.open(filepath)
            extracted_pages=[]

            for page_num in range(len(doc)):
                page=doc[page_num]
                page_text=page.get_text("text")
                if page_text.strip():
                    extracted_pages.append(page_text)
            doc.close()
            full_text = "\n\n---PAGE_BREAK---\n\n".join(extracted_pages)
            with open(output_filename_path,'w') as f:
                f.write(full_text)
            logger.info(f"Saved extracted text to {output_filename_path}")
        except Exception as e:
            logger.info(f"Failure in processing: {e}")
    
if __name__=='__main__':
    extract_text_from_pdf()