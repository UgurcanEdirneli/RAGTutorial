# Entry point for the project
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from DocumentExtraction.Extractor import Extractor
from DocumentExtraction.Parser import Parser
import pickle
from pathlib import Path
if __name__ == "__main__":
    # Example usage
    source = ".\\Documents\\pdfs"
    extracted = ".\\Documents\\ExtractedText"
    parsed = ".\\Documents\\ParsedText"

    parser = Parser(extracted)
    parser.parser_md(save_path=extracted, pickle_path = parsed,  override=True)
    with open("Documents\\ParsedText\\AYBÜ ÖĞMER TANITIM.pkl", "rb") as f:
        data = pickle.load(f)
        print(type(data))

    