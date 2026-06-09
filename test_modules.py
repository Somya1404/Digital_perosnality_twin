"""
Quick test script to verify all modules are working correctly.
Run this from the project root: python test_modules.py
"""

import sys
import os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_preprocessor():
    print("\n[1] Testing DataPreprocessor...")
    from src.pipeline.preprocessor import DataPreprocessor
    import pandas as pd

    pp = DataPreprocessor()
    sample = "Hey u r awesome lol!! Check https://google.com 😊🚀"
    cleaned = pp.clean_text(sample)
    emojis = pp.extract_emojis(sample)

    print(f"  Original : {sample}")
    print(f"  Cleaned  : {cleaned}")
    print(f"  Emojis   : {emojis}")
    print("  ✅ DataPreprocessor OK")

def test_stylometrics():
    print("\n[2] Testing StylometricAnalyzer...")
    from src.analysis.stylometrics import StylometricAnalyzer

    analyzer = StylometricAnalyzer()
    texts = [
        "I absolutely love this idea! It is innovative.",
        "Basically we should leverage all resources.",
        "Dynamic teams always win. Let us focus on strategy.",
    ]
    vocab = analyzer.extract_top_vocabulary(texts, top_n=5)
    stats = analyzer.compute_sentence_length_stats(texts)
    punct = analyzer.extract_punctuation_signatures(texts)

    print(f"  Top Vocab : {vocab}")
    print(f"  Sent Stats: {stats}")
    print(f"  Punctuation: {punct}")
    print("  ✅ StylometricAnalyzer OK")

def test_personality():
    print("\n[3] Testing PersonalityAnalyzer...")
    from src.analysis.personality import PersonalityAnalyzer

    analyzer = PersonalityAnalyzer()
    texts = [
        "I absolutely love this! So innovative and dynamic! 🚀",
        "Basically we need to leverage all strategies.",
        "I am honestly not sure about this approach tbh.",
    ]
    sentiment = analyzer.analyze_sentiment_trends(texts)
    big_five = analyzer.infer_big_five_traits(texts)

    print(f"  Sentiment : {sentiment}")
    print(f"  Big Five  : {big_five}")
    print("  ✅ PersonalityAnalyzer OK")

def test_explainer():
    print("\n[4] Testing ExplainableAIEngine...")
    from src.model.explain import ExplainableAIEngine

    xai = ExplainableAIEngine()
    profile = {
        "frequent_vocabulary": [
            {"word": "absolutely", "count": 48},
            {"word": "innovative", "count": 35},
            {"word": "strategy", "count": 29},
        ],
        "stylometrics": {
            "mean_sentence_length": 14.5,
            "top_emojis": ["🚀", "🔥"],
        }
    }
    result = xai.explain_generation(
        prompt="What do you think?",
        response="I absolutely think the strategy is innovative! 🚀",
        personality_profile=profile
    )
    print(f"  Confidence Score : {result['confidence_score']}")
    print(f"  Influential Tokens: {result['influential_tokens']}")
    print(f"  Reasoning: {result['reasoning']}")
    print("  ✅ ExplainableAIEngine OK")

def test_loader():
    print("\n[5] Testing DataLoader...")
    from src.pipeline.loader import DataLoader

    loader = DataLoader()
    sample_file = os.path.join("data", "raw", "sample_chat.txt")
    if os.path.exists(sample_file):
        lines = loader.load_txt(sample_file)
        print(f"  Loaded {len(lines)} lines from sample_chat.txt")
        print(f"  First line: {lines[0]}")
        print("  ✅ DataLoader OK")
    else:
        print("  ⚠️  sample_chat.txt not found, skipping loader test")

if __name__ == "__main__":
    print("=" * 55)
    print("  Digital Personality Twin — Module Tests")
    print("=" * 55)
    try:
        test_preprocessor()
        test_stylometrics()
        test_personality()
        test_explainer()
        test_loader()
        print("\n" + "=" * 55)
        print("  ✅ ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 55)
    except Exception as e:
        print(f"\n  ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
