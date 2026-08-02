import chromadb
from typing import List, Dict, Tuple, Optional, Any, cast
from src.core.memory.vector_db.base_vector_db import VectorDBInterface


class ChromaVectorDB(VectorDBInterface):
    def __init__(self, collection_name: str = "agent_memory", persist_directory: str = "./chroma_data"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name)

    def insert_vectors(self, vectors: List[List[float]], metadata: List[Dict[str, str]], ids: List[str]) -> None:
        if not ids:
            return
          
        self.collection.add(
            embeddings=cast(Any, vectors),
            metadatas=cast(Any, metadata),
            ids=ids
        )

    def semantic_search(self, query_vector: List[float], top_k: int, metadata_filters: Optional[Dict[str, str]] = None) -> List[Tuple[str, Dict[str, str], float]]:
        results = self.collection.query(
            query_embeddings=cast(Any, [query_vector]),
            n_results=top_k,
            where=cast(Any, metadata_filters) if metadata_filters else None
        )

        output = []
        if results['ids'] and results['ids'][0]:
            for i in range(len(results['ids'][0])):
                doc_id = results['ids'][0][i]
                meta = results['metadatas'][0][i] if results['metadatas'] else {}
                dist = results['distances'][0][i] if results['distances'] else 0.0

                # Chroma's Metadata type allows floats/ints/bools, but our Domain strictly
                # uses Dict[str, str]. We cast the returned dict back to our domain type.
                output.append(
                    (doc_id, cast(Dict[str, str], meta), float(dist)))

        return output

    def fetch_metadata(self, vector_id: str) -> Dict[str, str]:
        results = self.collection.get(ids=[vector_id])
        if results['metadatas'] and len(results['metadatas']) > 0:
            return cast(Dict[str, str], results['metadatas'][0])
        return {}
