# src/prompt_template.py
from llama_index.core import PromptTemplate

def get_strict_grounding_prompt() -> PromptTemplate:
    """
    Returns a LlamaIndex PromptTemplate that enforces strict grounding.
    It explicitly instructs the LLM to refuse to answer if the context
    does not contain the relevant information, preventing hallucinations.
    """
    template_str = (
        "You are an expert automotive diagnostic assistant. "
        "You are provided with context from official vehicle owner's manuals.\n"
        "Your task is to answer the user's question based strictly on the provided context.\n"
        "If the answer cannot be found in the context, you must explicitly state: "
        "'I do not have enough information in the provided manuals to answer this question.'\n"
        "Do not fabricate answers, guess, or use outside knowledge.\n\n"
        "Context Information:\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Question: {query_str}\n\n"
        "Answer:"
    )
    return PromptTemplate(template_str)

if __name__ == "__main__":
    print("[*] Testing prompt template initialization...")
    prompt = get_strict_grounding_prompt()
    
    # Test formatting with dummy data
    test_context = "The Tata Nexon EV high voltage battery capacity is 30.2 kWh or 40.5 kWh depending on the variant."
    test_query = "What is the battery capacity?"
    
    formatted_prompt = prompt.format(context_str=test_context, query_str=test_query)
    print("\n[+] Successfully formatted prompt:")
    print("====================================")
    print(formatted_prompt)
    print("====================================")