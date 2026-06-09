from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class VocabularyItem(BaseModel):
    word: str
    count: int

class Stylometrics(BaseModel):
    mean_sentence_length: float
    exclamation_rate: float
    top_emojis: List[str]
    ellipse_rate: float

class BigFive(BaseModel):
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

class PersonalityProfile(BaseModel):
    big_five: BigFive
    stylometrics: Stylometrics
    frequent_vocabulary: List[VocabularyItem]

class TwinDocument(BaseModel):
    id: Optional[str] = None
    username: str
    status: str = "READY_TO_TRAIN"
    personality_profile: Optional[PersonalityProfile] = None

class ChatInput(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"

class ExplanationToken(BaseModel):
    token: str
    frequency_in_dataset: int
    attribution_weight: float

class ExplanationOutput(BaseModel):
    confidence_score: float
    influential_tokens: List[ExplanationToken]
    reasoning: str

class ChatResponse(BaseModel):
    response: str
    explanation: ExplanationOutput
