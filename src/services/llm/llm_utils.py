from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from models.llm.type_constants import Embedding_Model_types, LLM_Model_types

def create_embeddings_for_data(embedding_model_family_name: Embedding_Model_types, 
                               embedding_model_name: LLM_Model_types, 
                               config = {}):
    """
    Get embedding model based on the family name and model name.

    Args:
        embedding_model_family_name (str): The family name of the embedding model.
        embedding_model_name (str): The specific model name to use.
        config (dict): Additional configuration parameters for the embedding model.

    Returns:
        An instance of the appropriate embedding model class.
    Raises:
        ValueError: If the embedding model family name is not recognized.
    """
    embedding_map = {
        Embedding_Model_types.OPENAI: OpenAIEmbeddings(
            model=embedding_model_name.value,
            base_url=config.get("base_url", "https://api.openai.com/v1"),
            model_kwargs={"temperature": config.get("temperature", 0.0)},

        ),
        Embedding_Model_types.OLLAMA: OllamaEmbeddings(
            model=embedding_model_name.value,
            base_url=config.get("base_url", "http://localhost:11434"),
            temperature=config.get("temperature", 0.0),            
        ),
        Embedding_Model_types.HUGGINGFACE: HuggingFaceEmbeddings(
            model_name=embedding_model_name.value,
            model_kwargs={"device": config.get("device", "cpu")},
        )
    }

    if embedding_model_family_name in embedding_map:
        return embedding_map[embedding_model_family_name]        
    else:
        raise ValueError(f"Embedding model {embedding_model_family_name} not found in the map.")

