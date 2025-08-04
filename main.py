from src.services.llm.lang_chains import test_llm_only_chain
from src.services.llm.agent import test_llm

if __name__ == "__main__":
    print("This is the main module.")
    test_llm_only_chain("Why is the sky blue? Limit your response to 300 words")
    llm_response = test_llm("Goodmorning. How is your day going?")
    print(f"LLM Response: {llm_response.content}")
