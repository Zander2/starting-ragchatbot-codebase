import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    """Configuration settings for the RAG system"""
    # OpenRouter API settings for Anthropic models
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    ANTHROPIC_MODEL: str = "anthropic/claude-3.5-sonnet"  # OpenRouter format
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Embedding model settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Document processing settings
    CHUNK_SIZE: int = 800       # Size of text chunks for vector storage
    CHUNK_OVERLAP: int = 100     # Characters to overlap between chunks
    MAX_RESULTS: int = 5         # Maximum search results to return
    MAX_HISTORY: int = 2         # Number of conversation messages to remember
    
    # Database paths
    CHROMA_PATH: str = "./chroma_db"  # ChromaDB storage location

config = Config()


