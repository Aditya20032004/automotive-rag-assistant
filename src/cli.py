# src/cli.py
import os
import sys

# Allow importing config and local modules from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipeline import run_diagnostic_pipeline

def interactive_loop():
    print("==================================================")
    print("      AUTOMOTIVE RAG ASSISTANT - INTERACTIVE      ")
    print("==================================================")
    print("Type 'exit' or 'quit' at any time to stop.\n")
    
    while True:
        query = input("\n[?] Enter your diagnostic question:\n> ")
        if query.lower() in ['exit', 'quit']:
            print("Exiting RAG CLI. Goodbye!")
            break
            
        print("\n[Optional] Filter by a specific vehicle? (Press Enter to skip)")
        
        manufacturer = input("Manufacturer (e.g., Tesla, Tata): ").strip().title()
        model = input("Model (e.g., Model S, Nexon): ").strip().title()
        
        # Convert empty strings to None so the retriever knows not to filter
        manufacturer = manufacturer if manufacturer else None
        model = model if model else None
        
        print(f"\n[*] Querying database... (Filters -> Make: {manufacturer}, Model: {model})")
        result = run_diagnostic_pipeline(query=query, manufacturer=manufacturer, model=model)
        
        print("\n=================== RAG ANSWER ===================")
        print(result["answer"])
        print("==================================================")
        print("\nSources Cited:")
        if result["citations"]:
            for idx, cite in enumerate(result["citations"], 1):
                print(f"  {idx}. [{cite['manufacturer']} {cite['model']}] - Section: {cite['section']} (Match Score: {cite['score']})")
        else:
            print("  No context retrieved. Database filter may be too restrictive.")
        print("-" * 50)

if __name__ == "__main__":
    interactive_loop()