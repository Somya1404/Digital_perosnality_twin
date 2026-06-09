from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import pandas as pd
import json
from src.pipeline.preprocessor import DataPreprocessor
from src.analysis.stylometrics import StylometricAnalyzer
from src.analysis.personality import PersonalityAnalyzer
from src.model.explain import ExplainableAIEngine
app = FastAPI(
    title="Digital Personality Twin API",
    description="Backend engine for training, analyzing, and chatting with an AI digital twin.",
    version="1.0.0"
)
# Enable CORS for frontend interface communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mock In-Memory Database for demonstration purposes
DB = {
    "twins": {},
    "conversations": {}
}
# Initial pre-loaded profile for demonstration if database is empty
MOCK_TWIN_ID = "64f1b2c3d4e5f6a7b8c9d0e1"
DB["twins"][MOCK_TWIN_ID] = {
    "id": MOCK_TWIN_ID,
    "username": "Alex Rivers",
    "status": "COMPLETED",
    "personality_profile": {
        "big_five": {
            "openness": 0.82,
            "conscientiousness": 0.65,
            "extraversion": 0.74,
            "agreeableness": 0.78,
            "neuroticism": 0.38
        },
        "stylometrics": {
            "mean_sentence_length": 14.5,
            "exclamation_rate": 0.03,
            "top_emojis": ["🚀", "🔥", "💡"],
            "ellipse_rate": 0.01
        },
        "frequent_vocabulary": [
            {"word": "absolutely", "count": 48},
            {"word": "innovative", "count": 35},
            {"word": "strategy", "count": 29},
            {"word": "dynamic", "count": 22},
            {"word": "leverage", "count": 18}
        ]
    }
}
class ChatInput(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
# Serve frontend via StaticFiles instead of direct root route
@app.post("/api/v1/twin/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Phase 1: Processes raw text messages and builds initial personality metrics.
    """
    try:
        contents = await file.read()
        lines = contents.decode("utf-8").split("\n")
        
        # Build DataFrame
        df = pd.DataFrame({"text": lines})
        df = df[df["text"].str.strip() != ""]
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            
        # 1. Pipeline Processing
        preprocessor = DataPreprocessor()
        processed_df = preprocessor.process_chat_dataframe(df, "text")
        
        texts = processed_df["cleaned_text"].tolist()
        
        # 2. Stylometrics Engine
        stylometrics_analyzer = StylometricAnalyzer()
        vocab = stylometrics_analyzer.extract_top_vocabulary(texts, top_n=10)
        punct = stylometrics_analyzer.extract_punctuation_signatures(texts)
        sent_len = stylometrics_analyzer.compute_sentence_length_stats(texts)
        
        # Flatten Emojis
        all_emojis = []
        for em_list in processed_df["emojis"]:
            all_emojis.extend(em_list)
        from collections import Counter
        top_emojis = [e for e, _ in Counter(all_emojis).most_common(3)]
        if not top_emojis:
            top_emojis = ["🤔", "💡"]
            
        # 3. Personality Analysis
        personality_analyzer = PersonalityAnalyzer()
        big_five = personality_analyzer.infer_big_five_traits(texts)
        
        # Generate new Twin entry
        import uuid
        twin_id = str(uuid.uuid4())
        
        DB["twins"][twin_id] = {
            "id": twin_id,
            "username": file.filename.split(".")[0],
            "status": "READY_TO_TRAIN",
            "personality_profile": {
                "big_five": big_five,
                "stylometrics": {
                    "mean_sentence_length": round(sent_len["mean_sentence_length"], 2),
                    "exclamation_rate": round(punct["exclamation_rate"], 4),
                    "top_emojis": top_emojis,
                    "ellipse_rate": round(punct["ellipse_rate"], 4)
                },
                "frequent_vocabulary": vocab
            }
        }
        
        return DB["twins"][twin_id]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File parsing error: {str(e)}")
@app.get("/api/v1/twin/{twin_id}/profile")
def get_profile(twin_id: str):
    """
    Fetches the profile stats & Big Five matrix for visualization.
    """
    if twin_id not in DB["twins"]:
        raise HTTPException(status_code=404, detail="Twin profile not found.")
    return DB["twins"][twin_id]
@app.post("/api/v1/twin/{twin_id}/train")
def trigger_training(twin_id: str):
    """
    Simulates fine-tuning task initiation. In production, this would trigger PyTorch process.
    """
    if twin_id not in DB["twins"]:
        raise HTTPException(status_code=404, detail="Twin profile not found.")
        
    DB["twins"][twin_id]["status"] = "COMPLETED"
    return {"message": "Model training completed successfully.", "status": "COMPLETED"}
@app.post("/api/v1/twin/{twin_id}/chat")
def chat_with_twin(twin_id: str, chat_input: ChatInput):
    """
    Phase 4 & 5: Generates twin response and computes attribution details.
    """
    if twin_id not in DB["twins"]:
        raise HTTPException(status_code=404, detail="Twin profile not found.")
        
    twin = DB["twins"][twin_id]
    profile = twin["personality_profile"]
    
    # Simple simulated generation based on training vocabulary for high fidelity mock responsiveness
    vocab_words = [item["word"] for item in profile.get("frequent_vocabulary", [])]
    top_emojis = profile.get("stylometrics", {}).get("top_emojis", ["🚀", "💡"])
    emojis = "".join(top_emojis)
    
    # Construct stylized responsive text incorporating user signature styles
    sentence_base = "Absolutely! Let's leverage our dynamic strategy to build an innovative solution."
    if len(vocab_words) >= 3:
        sentence_base = f"I absolutely agree. Let's look at the {vocab_words[2]} and think of a {vocab_words[1]} way forward!"
    elif len(vocab_words) >= 1:
        sentence_base = f"I absolutely agree. Let's look at the {vocab_words[0]} and think of a creative way forward!"
    # Clean user input to detect context
    user_msg = chat_input.message.lower().strip()
    
    w1 = vocab_words[0] if len(vocab_words) > 0 else "absolutely"
    w2 = vocab_words[1] if len(vocab_words) > 1 else "innovative"
    w3 = vocab_words[2] if len(vocab_words) > 2 else "strategy"
    w4 = vocab_words[3] if len(vocab_words) > 3 else "dynamic"
    
    import random
    
    if any(greet in user_msg for greet in ["hello", "hi", "hey", "greetings"]):
        greetings = [
            f"Hey there! It's {w1} great to hear from you. Let's think of some {w2} ideas today!",
            f"Hello! Always ready to leverage a {w4} conversation. What's on your mind?",
            f"Hey! Let's get right into it. What kind of {w3} are we building today?"
        ]
        sentence_base = random.choice(greetings)
    elif "?" in user_msg:
        questions = [
            f"That's a {w2} question! We should {w1} leverage our {w3} to find the answer.",
            f"Honestly, it comes down to a {w4} approach. Let's think of how to utilize {w2} methods.",
            f"I think we need to look at {w3} options first. What do you think?"
        ]
        sentence_base = random.choice(questions)
    elif any(agree in user_msg for agree in ["yes", "yeah", "agree", "sure", "ok"]):
        agreements = [
            f"I {w1} agree with that! Let's push forward with this {w4} path.",
            f"Exactly. Implementing this {w3} is the most {w2} way forward.",
            f"Totally! Let's leverage our resources and make it happen."
        ]
        sentence_base = random.choice(agreements)
    else:
        defaults = [
            f"I think we should {w1} focus on our {w3}. That's the most {w2} way to grow.",
            f"It's all about being {w4} and adaptable. Let's leverage what we have.",
            f"Interesting! Let's keep exploring this {w2} angle and build a solid {w3} around it."
        ]
        sentence_base = random.choice(defaults)
        
    response_text = f"{sentence_base} {emojis}"
    
    # 5. Explainable AI analysis
    xai = ExplainableAIEngine()
    explanation = xai.explain_generation(chat_input.message, response_text, profile)
    
    # Store session conversation logs
    session_id = chat_input.session_id
    if session_id not in DB["conversations"]:
        DB["conversations"][session_id] = []
        
    DB["conversations"][session_id].append({"sender": "user", "text": chat_input.message})
    DB["conversations"][session_id].append({"sender": "twin", "text": response_text, "explanation": explanation})
    
    return {
        "response": response_text,
        "explanation": explanation
    }
from fastapi.staticfiles import StaticFiles
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
