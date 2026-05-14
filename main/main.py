# Entry point for the project
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from DocumentExtraction.Extractor import Extractor
from DocumentExtraction.Parser import Parser
from DocumentEmbedding.Indexing import Indexing
from DocumentEmbedding.EmbeddingInterface import EmbeddingInterface
import pickle
from pathlib import Path
if __name__ == "__main__":
    # Example usage
    source = ".\\Documents\\pdfs"
    extracted = ".\\Documents\\ExtractedText"
    parsed = ".\\Documents\\ParsedText"
    embeddings_path = ".\\Documents\\Embeddings"
    if Path(extracted).exists():
        if list(Path(source).glob("*.pdf")).__len__() == 0:
            print("No PDF files found in the source directory.")
        else:
            if list(Path(extracted).glob("*.md")).__len__() == 0:
                for pdf_file in Path(source).glob("*.pdf"):
                    extractor = Extractor(str(pdf_file), extracted)
    else:
        print("No extracted files found in the extracted directory.")
    if Path(parsed).exists():
        if list(Path(parsed).glob("*.pkl")).__len__() == 0:
            print("No parsed files found in the parsed directory.")
            parser = Parser(extracted)
            parser.parser_md(parsed, parsed, override=False)
        else:
            print("Parsed files already exist in the parsed directory.")
            documents = []
            for pkl_file in Path(parsed).glob("*.pkl"):
                with open(pkl_file, "rb") as f:
                    indexed_chunks = pickle.load(f) 
                    documents.append(indexed_chunks)
                    print(f"Loaded indexed chunks from {pkl_file}: {len(indexed_chunks)} chunks")
    else:
        print("No parsed files found.")
    if Path(embeddings_path).exists():
        if list(Path(embeddings_path).glob("*.faiss")).__len__() == 0:
            print("No embedding files found in the embeddings directory.")
            if list(Path(parsed).glob("*.pkl")).__len__() > 0:
                print("Some parsed files found embedding them into vectors...")
                embedding_model = EmbeddingInterface("paraphrase-multilingual-MiniLM-L12-v2")
                for pkl_file in Path(parsed).glob("*.pkl"):
                    with open(pkl_file, "rb") as f:
                        indexed_chunks = pickle.load(f) 
                        documents.append(indexed_chunks)
                        print(f"Loaded indexed chunks from {pkl_file}: {len(indexed_chunks)} chunks")
                        chunks = list(indexed_chunks.values())
                        embeddings = embedding_model.embed_chunks(chunks)
                        print(f"Generated embeddings for {pkl_file}: {len(embeddings)} embeddings")
                        index = Indexing(embedding_dim=len(embeddings[0]))
                        index.add_embeddings(embeddings)
                        index.save_index(str(Path(embeddings_path) / (pkl_file.stem + ".faiss")))
        else:
            print("Embedding files already exist in the embeddings directory.")
    else:
        print("No embedding files found.")
        print("Creating embeddings directory...")
        os.makedirs(embeddings_path, exist_ok=True)
        embedding_model = EmbeddingInterface("paraphrase-multilingual-MiniLM-L12-v2")
        for pkl_file in Path(parsed).glob("*.pkl"):
            with open(pkl_file, "rb") as f:
                indexed_chunks = pickle.load(f) 
                documents.append(indexed_chunks)
                print(f"Loaded indexed chunks from {pkl_file}: {len(indexed_chunks)} chunks")
                chunks = list(indexed_chunks.values())
                embeddings = embedding_model.embed_chunks(chunks)
                print(f"Generated embeddings for {pkl_file}: {len(embeddings)} embeddings")
                index = Indexing(embedding_dim=len(embeddings[0]))
                index.add_embeddings(embeddings)
                index.save_index(str(Path(embeddings_path) / (pkl_file.stem + ".faiss")))
    

    