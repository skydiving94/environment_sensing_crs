from typing import List
from sentence_transformers import SentenceTransformer


class LocalEmbedder:
    """
    Generates text embeddings locally using HuggingFace's sentence-transformers.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # 'all-MiniLM-L6-v2' is a lightweight, highly performant model mapping text to 384 dimensions.
        self.model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> List[float]:
        """Converts a single string into a vector."""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Converts a batch of strings into a list of vectors."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
