import os
import pandas as pd
from typing import List

class DataLoader:
    """
    Loads raw text data from different file formats:
    - Plain .txt files (one message per line)
    - .csv files with a designated text column
    """

    def load_txt(self, filepath: str) -> List[str]:
        """Load a plain text file where each line is one message."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines

    def load_csv(self, filepath: str, text_column: str = "text") -> List[str]:
        """Load a CSV file and extract a specific text column."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        df = pd.read_csv(filepath)
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found. Available: {list(df.columns)}")
        return df[text_column].dropna().tolist()

    def load_any(self, filepath: str, text_column: str = "text") -> List[str]:
        """Auto-detect format and load file."""
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == ".txt":
            return self.load_txt(filepath)
        elif ext == ".csv":
            return self.load_csv(filepath, text_column)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Use .txt or .csv")
