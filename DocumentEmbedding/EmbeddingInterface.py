import torch
class EmbeddingInterface():
    def __init__(self, model_name: str, device: str = "auto"):
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            if device in ["cuda", "cpu"]:
                self.device = device
            else:
                raise ValueError("Invalid device. Please choose either 'cuda' or 'cpu'.")
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name, device=self.device)
        except Exception as e:
            print(f"Error loading model '{model_name}': {e}")
            raise e
    def embed_chunks(self, texts: list[str]) -> list[list[float]]:
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=True)
            return embeddings.cpu().tolist()  # Ensure embeddings are on CPU and convert to list
        except Exception as e:
            print(f"Error during embedding: {e}")
            raise e
    
