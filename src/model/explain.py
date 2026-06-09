from typing import List, Dict, Any
import re

class ExplainableAIEngine:
    """
    Phase 5: Explainable AI
    Calculates why a particular model output was generated.
    Highlights specific training vocabulary matches and generates structural confidence ratings.
    """
    def __init__(self):
        pass

    def explain_generation(
        self, 
        prompt: str, 
        response: str, 
        personality_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyzes the generated output text and matches features with the target personality profile.
        Computes a similarity confidence score based on the target style profile.
        """
        # 1. Identify which vocabulary words from training influenced this response
        vocab_profile = personality_profile.get("frequent_vocabulary", [])
        vocab_words = {item["word"].lower(): item["count"] for item in vocab_profile}
        
        response_words = re.findall(r"\b\w+\b", response.lower())
        
        influential_tokens = []
        for word in response_words:
            if word in vocab_words:
                influential_tokens.append({
                    "token": word,
                    "frequency_in_dataset": vocab_words[word],
                    "attribution_weight": float(min(1.0, vocab_words[word] / 50.0))
                })
        
        # Deduplicate influential tokens
        unique_tokens = {item["token"]: item for item in influential_tokens}
        influential_tokens = list(unique_tokens.values())
        
        # 2. Confidence scoring mechanism based on Stylometric Alignment
        target_metrics = personality_profile.get("stylometrics", {})
        
        # Average length alignment
        target_len = target_metrics.get("mean_sentence_length", 12.0)
        actual_len = len(response_words)
        length_ratio = min(actual_len, target_len) / max(actual_len, target_len, 1.0)
        
        # Emoji alignment
        target_emojis = target_metrics.get("top_emojis", [])
        actual_emojis = [c for c in response if c in target_emojis]
        emoji_alignment = 1.0 if actual_emojis else 0.5
        
        confidence_score = float(round((length_ratio * 0.6 + emoji_alignment * 0.4), 2))
        
        return {
            "confidence_score": confidence_score,
            "influential_tokens": sorted(influential_tokens, key=lambda x: x["attribution_weight"], reverse=True)[:5],
            "reasoning": f"Generated output mirrors vocabulary patterns. Length compatibility matched at {int(length_ratio*100)}%."
        }
