import abc
from typing import List, Dict, Tuple, Optional


class VectorDBInterface(abc.ABC):
    """
    Generic Abstract Base Class for Vector Database implementations.
    Decouples storage and retrieval logic from the main LongTermMemory system.
    """

    @abc.abstractmethod
    def insert_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, str]], ids: List[str]) -> None:
        """Inserts embeddings and their associated metadata into the vector store."""
        pass

    @abc.abstractmethod
    def semantic_search(self, query_vector: List[float], top_k: int, metadata_filters: Optional[Dict[str, str]] = None) -> List[Tuple[str, Dict[str, str], float]]:
        """
        Performs a semantic similarity search.
        Returns a list of Tuples containing: (Vector ID, Metadata Dictionary, Distance/Score)
        """
        pass

    @abc.abstractmethod
    def fetch_metadata(self, vector_id: str) -> Dict[str, str]:
        """Fetches the metadata payload associated with a specific vector ID."""
        pass
