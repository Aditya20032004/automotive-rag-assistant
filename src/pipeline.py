# src/pipeline.py
import os
import sys

from llama_index.core import Settings

# Allow importing config and local modules from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from src.retriever import get_retriever
from src.model_loader import get_llm
from src.prompt_template import get_strict_grounding_prompt

def run_diagnostic_pipeline(query: str, manufacturer: str = None, model: str = None) -> dict:
    """
    Runs the complete text RAG diagnostic pipeline.
    Retrieves relevant chunks, formats the strict grounding prompt, 
    queries Phi-3-mini via Ollama, and returns the answer with citations.
    """
    # 1. Initialize our retriever and LLM components
    retriever = get_retriever(manufacturer=manufacturer, model=model)
    llm = get_llm()
    prompt_template = get_strict_grounding_prompt()
    
    # 2. Retrieve top matching text chunks from Chroma
    retrieved_nodes = retriever.retrieve(query)
    
    # Fallback if the vector store is completely empty or returns nothing
    if not retrieved_nodes:
        return {
            "answer": "I do not have enough information in the provided manuals to answer this question.",
            "citations": []
        }
        
    # 3. Combine chunk texts into a single context block
    context_chunks = []
    citations = []
    
    for node in retrieved_nodes:
        context_chunks.append(node.node.text)
        
        # Pull metadata for citation tracking
        meta = node.node.metadata
        citations.append({
            "manufacturer": meta.get("source_manufacturer", "Unknown"),
            "model": meta.get("source_model", "Unknown Model"),
            "section": meta.get("section_title", "General Context"),
            "score": round(float(node.score), 4) if node.score is not None else 0.0
        })
        
    combined_context = "\n\n".join(context_chunks)
    
    # 4. Format the final grounded prompt string
    final_prompt = prompt_template.format(context_str=combined_context, query_str=query)
    
    # 5. Query the local LLM
    print("[*] Generating answer from grounded context...")
    llm_response = llm.complete(final_prompt)
    
    return {
        "answer": llm_response.text.strip(),
        "citations": citations
    }

if __name__ == "__main__":
    # ---------------------------------------------------------
    # QUICK PIPELINE SMOKE TEST
    # ---------------------------------------------------------
    print("[*] Running end-to-end pipeline test query...")
    
    # Adjust this query to target whatever manuals you currently have loaded
    test_query = "How do I pair a key card or key fob?"
    
    result = run_diagnostic_pipeline(
        query=test_query,
        manufacturer="Tesla", 
        model="Model S"
    )
    
    print("\n=================== RAG ANSWER ===================")
    print(result["answer"])
    print("==================================================")
    print("\nSources Cited:")
    for idx, cite in enumerate(result["citations"], 1):
        print(f"  {idx}. [{cite['manufacturer']} {cite['model']}] - Section: {cite['section']} (Match Score: {cite['score']})")