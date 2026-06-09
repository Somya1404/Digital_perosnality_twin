import torch
from torch.utils.data import Dataset
from typing import List, Dict, Any

class PersonalityTwinDataset(Dataset):
    """
    Phase 3: Dataset Preparation
    Wraps text tokens and prompts for PyTorch modeling.
    """
    def __init__(self, conversations: List[Dict[str, str]], tokenizer: Any, max_length: int = 512):
        self.conversations = conversations
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.conversations)

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        item = self.conversations[idx]
        prompt = item.get("prompt", "")
        response = item.get("response", "")
        
        # Format conversation standard format: "Prompt: <text>\nResponse: <text>"
        full_text = f"Prompt: {prompt}\nResponse: {response}"
        
        encodings = self.tokenizer(
            full_text,
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        
        input_ids = encodings["input_ids"].squeeze(0)
        attention_mask = encodings["attention_mask"].squeeze(0)
        
        # For Causal Language Modeling, labels are the same as input_ids
        labels = input_ids.clone()
        # Ignore padding indices when calculating loss
        labels[labels == self.tokenizer.pad_token_id] = -100
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels
        }
