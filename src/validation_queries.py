# tests/validation_queries.py
import os
import sys

# Allow importing config and local modules from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipeline import run_diagnostic_pipeline

def run_tests():
    print("==================================================")
    print("      PHASE 1: RAG PIPELINE VALIDATION SUITE      ")
    print("==================================================\n")

    # TEST 1: Standard In-Domain Query
    print(">>> TEST 1: Standard Retrieval (Tesla Model S)")
    print("Query: 'How do I pair a key card or key fob?'")
    result_1 = run_diagnostic_pipeline("How do I pair a key card or key fob?")
    print(f"\n[Answer]: {result_1['answer']}")
    print(f"[Top Source]: {result_1['citations'][0]['manufacturer']} {result_1['citations'][0]['model']} | {result_1['citations'][0]['section']}")
    print("-" * 50)

    # TEST 2: Hard-Filtered Query (Cross-Contamination Check)
    print("\n>>> TEST 2: Targeted Metadata Filter (Tata Nexon EV)")
    print("Query: 'What is the high voltage battery capacity?'")
    print("Constraint: Only searching Tata Nexon EV chunks.")
    result_2 = run_diagnostic_pipeline(
        query="What is the high voltage battery capacity?",
        manufacturer="Tata",
        model="Nexon EV"
    )
    print(f"\n[Answer]: {result_2['answer']}")
    if result_2['citations']:
        print(f"[Top Source]: {result_2['citations'][0]['manufacturer']} {result_2['citations'][0]['model']} | {result_2['citations'][0]['section']}")
    else:
        print("[Top Source]: None found.")
    print("-" * 50)

    # TEST 3: Strict Grounding (Anti-Hallucination Check)
    # We ask for engine oil instructions specifically targeting an EV manual.
    print("\n>>> TEST 3: Strict Grounding / Refusal Test")
    print("Query: 'How do I change the engine oil on a Tesla Model S?'")
    print("Expected Behavior: The model MUST refuse to answer.")
    result_3 = run_diagnostic_pipeline(
        query="How do I change the engine oil on a Tesla Model S?",
        manufacturer="Tesla",
        model="Model S"
    )
    print(f"\n[Answer]: {result_3['answer']}")
    
    passed = "I do not have enough information" in result_3['answer'] or "does not contain" in result_3['answer'].lower()
    if passed:
        print("\n[+] TEST 3 PASSED: The model successfully refused to hallucinate engine oil instructions for an EV.")
    else:
        print("\n[-] TEST 3 FAILED: The model hallucinated an answer. The prompt template needs tightening.")
    print("==================================================\n")

if __name__ == "__main__":
    run_tests()