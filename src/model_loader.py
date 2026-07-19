# src/model_loader.py
import os
import sys

from llama_index.llms.ollama import Ollama

# Allow importing config from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_llm():
    """
    Initializes and returns the LlamaIndex Ollama LLM interface.
    Temperature is locked to 0.0 for strict, factual responses.
    """
    # model is pulled directly from config (default: "phi3:mini")
    llm = Ollama(
        model=config.LLM_MODEL_NAME, 
        request_timeout=120.0, 
        temperature=0.0
    )
    return llm

if __name__ == "__main__":
    print(f"[*] Initializing connection to Ollama (Model: {config.LLM_MODEL_NAME})...")
    llm = get_llm()
    
    print("[*] Testing LLM generation (this may take a few seconds on first run)...")
    try:
        # A simple ping to ensure the model is loaded in VRAM and responding
        response = llm.complete("What is 2+2? Reply with just the number.")
        print(f"[+] LLM Response: {response.text.strip()}")
        print("[+] Success! Ollama is correctly hooked up to LlamaIndex.")
    except Exception as e:
        print(f"[-] Error communicating with Ollama: {e}")
        print("    Ensure Ollama is running in the background and the model is pulled.")