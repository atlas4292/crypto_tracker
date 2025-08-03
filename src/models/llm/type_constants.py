from enum import Enum, unique

@unique
class Embedding_Model_types(Enum):
    OPENAI = "OpenAI"
    OLLAMA = "Ollama"
    HUGGINGFACE = "HuggingFace"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
    
@unique
class LLM_Model_types(Enum):
    GEMMA_12B = "Gemma3:12b"
    QWEN_7B = "qwen2:7b"
    MISTRAL_NEMO = "mistral-nemo:latest"
    BAKLLAVA = "bakllava:latest"
    LLAMA_3_1_8B = "llama3.1:8b"
    DEVSTRAL = "devstral:24b"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
