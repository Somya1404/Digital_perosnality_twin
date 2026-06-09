import re
import emoji
import pandas as pd
from typing import Dict, List, Any

# Load spaCy English model (make sure to download it using: python -m spacy download en_core_web_sm)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except (ImportError, ModuleNotFoundError):
    nlp = None

class DataPreprocessor:
    """
    Phase 1: Data Collection & Preprocessing
    Cleans raw conversational data from different files, formats, and channels.
    """
    def __init__(self, remove_stopwords: bool = False):
        self.remove_stopwords = remove_stopwords
        # Simple slang mapping table
        self.slang_map = {
            "u": "you",
            "r": "are",
            "btw": "by the way",
            "lol": "laugh out loud",
            "idk": "i do not know",
            "imo": "in my opinion",
            "tbh": "to be honest",
            "omg": "oh my god",
            "gtg": "got to go",
            "brb": "be right back"
        }
    def clean_text(self, text: str) -> str:
        """
        Cleans and normalizes raw text by handling URLs, system messages, 
        reducing double spacing, and mapping common chat slang.
        """
        if not isinstance(text, str):
            return ""
        
        # 1. Convert to lowercase
        text = text.lower().strip()
        
        # 2. Remove URLs
        text = re.sub(r"https?://\S+|www\.\S+", "", text)
        
        # 3. Replace slang
        words = text.split()
        normalized_words = [self.slang_map.get(w, w) for w in words]
        text = " ".join(normalized_words)
        
        # 4. Collapse multiple white spaces
        text = re.sub(r"\s+", " ", text)
        
        return text
    def extract_emojis(self, text: str) -> List[str]:
        """
        Extracts emojis from text using the emoji library helper.
        """
        if not isinstance(text, str):
            return []
        return [c for c in text if emoji.is_emoji(c)]
    def extract_linguistic_features(self, text: str) -> Dict[str, Any]:
        """
        Extracts complex linguistic variables using spaCy, including Part of Speech (POS)
        counts, punctuation frequencies, and total sentence tokenization.
        """
        if not nlp or not text:
            return {
                "tokens_count": len(text.split()),
                "nouns": 0, "verbs": 0, "adjectives": 0, "punctuations": 0
            }
        
        doc = nlp(text)
        features = {
            "tokens_count": len(doc),
            "nouns": sum(1 for token in doc if token.pos_ == "NOUN"),
            "verbs": sum(1 for token in doc if token.pos_ == "VERB"),
            "adjectives": sum(1 for token in doc if token.pos_ == "ADJ"),
            "punctuations": sum(1 for token in doc if token.pos_ == "PUNCT"),
        }
        return features
    def process_chat_dataframe(self, df: pd.DataFrame, text_col: str) -> pd.DataFrame:
        """
        Transforms raw chat dataframe to extract structural metadata and clean messages.
        """
        df = df.copy()
        df["cleaned_text"] = df[text_col].apply(self.clean_text)
        df["emojis"] = df[text_col].apply(self.extract_emojis)
        
        # Feature extraction
        features = df["cleaned_text"].apply(self.extract_linguistic_features)
        features_df = pd.DataFrame(list(features))
        
        return pd.concat([df, features_df], axis=1)
