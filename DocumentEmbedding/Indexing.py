import faiss
import numpy as np

class Indexing:
    def __init__(self, embedding_dim: int, indexing_method: str = "IndexFlatL2"):
        if indexing_method == "IndexFlatL2":
            self.index = faiss.IndexFlatL2(embedding_dim)
        else:
            raise ValueError("Unsupported indexing method: " + indexing_method)

    def add_embeddings(self, embeddings: list[list[float]]):
        try:
            self.index.add(np.array(embeddings).astype('float32'))
        except Exception as e:
            print(f"Error adding embeddings to index: {e}")
            raise e
    def search(self, query_embedding: list[float], top_k: int = 5):
        try:
            distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
            return distances[0], indices[0]
        except Exception as e:
            print(f"Error during search: {e}")
            raise e
    def embed_query(self, query: str, embedding_model):
        try:
            return embedding_model.embed([query])[0]
        except Exception as e:
            print(f"Error embedding query: {e}")
            raise e
    def save_index(self, file_path: str):
        try:
            faiss.write_index(self.index, file_path)
        except Exception as e:
            print(f"Error saving index to {file_path}: {e}")
            raise e
    def load_index(self, file_path: str) :
        try:
            embeddings = faiss.read_index(file_path)
            return embeddings
        except Exception as e:
            print(f"Error loading index from {file_path}: {e}")
            raise e
    