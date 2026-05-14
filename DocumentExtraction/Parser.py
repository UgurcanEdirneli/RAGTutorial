from pathlib import Path
import os
class Parser():
    def __init__(self, source_path: str):
        self.source = Path(source_path)
        

    def parser_md(self, save_path: str, pickle_path: str, override: bool = False):
        target = Path(save_path)
        pickle_path = Path(pickle_path)
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
        try: 
            for md_file in self.source.glob("*.md"):
                parsed_text = []
                with open(md_file, "r", encoding="utf-8") as md:
                    md_doc = md.readlines()
                    paragraph = ""
                    for line in md_doc:
                        if line.startswith("#"):
                            parsed_text.append(paragraph)
                            paragraph = ""
                            paragraph += line + "\n"
                        else:
                            paragraph += line + "\n"
                    Parser.drop_text(parsed_text)
                    parsed_text = Parser._chunker(parsed_text)
                try:
                    import pickle
                    current_pickle_path = pickle_path / (md_file.stem + ".pkl")
                    if current_pickle_path.exists() and not override:
                        print("Pickle file exists for this file: " + str(md_file))
                    else:
                        indexed_chunks = {i : chunk for i, chunk in enumerate(parsed_text)}
                        with open(current_pickle_path, "wb") as f:
                            pickle.dump(indexed_chunks, f)
                        print("Overridden successfully!")
                    print("Parsed text saved successfully!") 
                except Exception as e:
                    print("An error ocurred inside try : ", e)
        except Exception as e:
            print("An error ocurred : ", e)
            return None
    @staticmethod
    def drop_text(texts: list[str]) -> None:
        # Remove chunks that are empty or contain only a header line
        texts[:] = [
            t for t in texts
            if t.strip() and not (t.strip().startswith("#") and len(t.strip().splitlines()) == 1)
        ]
    @staticmethod
    def _chunker(texts: list[str]) -> list[str]:
        print("Chunker is working")
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        print(f"chunker is called for parsed text with length: {len(texts)}")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=120,
            separators=["\n\n", "\n", " ", ""]
                            )
         # Flatten the list of lists
        chunks = []
        for t in texts:
            chunks.extend(splitter.split_text(t))
        print(f"{len(chunks)} chunks produced")
        return chunks