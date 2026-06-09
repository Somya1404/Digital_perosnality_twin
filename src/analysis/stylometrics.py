from collections import Counter
import re
import pandas as pd
from typing import Dict, List, Any

class StylometricAnalyzer:
    """
    Phase 2: Personality Analysis - Stylometric Engine
    Analyzes vocabulary usage patterns, structural habits, and punctuation styles.
    """
    def __init__(self):
        pass

    def compute_sentence_length_stats(self, texts: List[str]) -> Dict[str, float]:
        """
        Calculates mean and standard deviation of sentence lengths.
        """
        lengths = []
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                continue
            sentences = re.split(r"[.!?]+", text)
            for s in sentences:
                words = s.strip().split()
                if len(words) > 0:
                    lengths.append(len(words))
        
        if not lengths:
            return {"mean_sentence_length": 0.0, "std_sentence_length": 0.0}
            
        df = pd.Series(lengths)
        return {
            "mean_sentence_length": float(df.mean()),
            "std_sentence_length": float(df.std()) if len(df) > 1 else 0.0
        }

    def extract_top_vocabulary(self, texts: List[str], top_n: int = 50) -> List[Dict[str, Any]]:
        """
        Builds a vocabulary profile showing top frequently used keywords.
        """
        words = []
        for text in texts:
            if isinstance(text, str):
                # Simple tokenization without punctuation
                words.extend(re.findall(r"\b\w+\b", text.lower()))
        
        counts = Counter(words)
        return [{"word": word, "count": count} for word, count in counts.most_common(top_n)]

    def extract_punctuation_signatures(self, texts: List[str]) -> Dict[str, float]:
        """
        Identifies character-level features like exclamation and question marks frequency.
        """
        total_chars = 0
        puncts = {"!": 0, "?": 0, "...": 0}
        
        for text in texts:
            if not isinstance(text, str):
                continue
            total_chars += len(text)
            puncts["!"] += text.count("!")
            puncts["?"] += text.count("?")
            puncts["..."] += text.count("...")
            
        if total_chars == 0:
            return {"exclamation_rate": 0.0, "question_rate": 0.0, "ellipse_rate": 0.0}
            
        return {
            "exclamation_rate": float(puncts["!"] / total_chars),
            "question_rate": float(puncts["?"] / total_chars),
            "ellipse_rate": float(puncts["..."] / total_chars)
        }
