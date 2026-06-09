import nltk
try:
    from nltk.sentiment import SentimentIntensityAnalyzer
    nltk.download('vader_lexicon', quiet=True)
except ImportError:
    SentimentIntensityAnalyzer = None

from typing import Dict, List, Any

class PersonalityAnalyzer:
    """
    Phase 2: Personality Analysis Engine
    Infers user's Big Five personality dimensions and emotional baselines.
    """
    def __init__(self):
        if SentimentIntensityAnalyzer:
            self.sia = SentimentIntensityAnalyzer()
        else:
            self.sia = None

    def analyze_sentiment_trends(self, texts: List[str]) -> Dict[str, float]:
        """
        Runs sentiment analysis across all processed texts to determine average emotional score.
        """
        if not self.sia:
            return {"positive": 0.33, "neutral": 0.34, "negative": 0.33}
            
        pos, neu, neg = 0.0, 0.0, 0.0
        count = 0
        
        for text in texts:
            if not isinstance(text, str) or not text.strip():
                continue
            scores = self.sia.polarity_scores(text)
            pos += scores["pos"]
            neu += scores["neu"]
            neg += scores["neg"]
            count += 1
            
        if count == 0:
            return {"positive": 0.0, "neutral": 1.0, "negative": 0.0}
            
        return {
            "positive": float(pos / count),
            "neutral": float(neu / count),
            "negative": float(neg / count)
        }

    def infer_big_five_traits(self, texts: List[str]) -> Dict[str, float]:
        """
        Heuristic-based Big Five Trait Inference based on stylometric signatures
        (e.g., word count, punctuation frequency, positive sentiment).
        In a production setting, this would run a dedicated multi-task transformer.
        """
        sentiment = self.analyze_sentiment_trends(texts)
        total_words = sum(len(t.split()) for t in texts if isinstance(t, str))
        avg_len = total_words / max(len(texts), 1)
        
        # Openness: correlates with rich vocabulary and longer, complex sentences
        openness = min(1.0, max(0.0, 0.3 + (avg_len / 40.0)))
        
        # Conscientiousness: correlates with precise grammar and structured lengths
        conscientiousness = min(1.0, max(0.0, 0.5 + (sentiment["neutral"] * 0.3)))
        
        # Extraversion: correlates with positive emotion, emojis, exclamation marks
        exclamations = sum(t.count("!") for t in texts if isinstance(t, str))
        extraversion = min(1.0, max(0.0, 0.2 + (sentiment["positive"] * 0.6) + (min(exclamations, 5) * 0.1)))
        
        # Agreeableness: correlates with high positive sentiment, low negative sentiment
        agreeableness = min(1.0, max(0.0, 0.5 + (sentiment["positive"] - sentiment["negative"])))
        
        # Neuroticism: correlates with negative sentiment rates
        neuroticism = min(1.0, max(0.0, 0.1 + (sentiment["negative"] * 0.8)))
        
        return {
            "openness": float(round(openness, 2)),
            "conscientiousness": float(round(conscientiousness, 2)),
            "extraversion": float(round(extraversion, 2)),
            "agreeableness": float(round(agreeableness, 2)),
            "neuroticism": float(round(neuroticism, 2))
        }
