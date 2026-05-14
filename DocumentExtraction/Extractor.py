
# Correct imports
import fitz  # PyMuPDF
import pymupdf4llm
import pathlib
import os
import logging

class Extractor:
    def __init__(self, source_path: str, target_path: str, parser=None):
        self.path = pathlib.Path(source_path)
        self.target_path = pathlib.Path(target_path)

        # Parser handling: use provided parser if callable, else use pymupdf4llm.to_markdown
        if parser and callable(parser):
            self.parser = parser
        else:
            self.parser = pymupdf4llm.to_markdown

        markDown = None
        try:
            markDown = self.parser(str(self.path))
        except FileNotFoundError:
            logging.error("Source file not found: %s", self.path)
        except Exception as e:
            logging.error("Error during markdown extraction: %s", e)

        if markDown is not None:
            # Ensure target directory exists
            try:
                output_file = self.target_path / (self.path.stem + ".md")
                os.makedirs(self.target_path.parent, exist_ok=True)
                output_file.write_text(markDown, encoding="utf-8")
            except Exception as e:
                logging.error("Failed to write markdown to target: %s", e)
        else:
            logging.error("Markdown extraction failed; nothing written.")
        