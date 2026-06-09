import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Any

class PersonalityResponseGenerator:
    """
    Phase 4: Digital Twin Generation & Style-Injected Generation
    Uses fine-tuned language weights and prompt engineering parameters (temperature, top_p)
    to emulate the target person's unique speech patterns.
    """
    def __init__(self, checkpoint_dir: str):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_dir)
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint_dir).to(self.device)

    def generate_response(self, user_prompt: str, personality_profile: Dict[str, Any], max_new_tokens: int = 80) -> str:
        """
        Generates a custom stylized reply. Integrates user-specific metrics 
        (e.g. favorite emojis, exclamation rate) directly into target formatting tags.
        """
        # Formulate dynamic prefix based on the personality profile
        stats = personality_profile.get("stylometrics", {})
        top_emojis = "".join(stats.get("top_emojis", []))
        
        # Guide system behavior using detailed system style tokens
        system_prefix = (
            f"[Style: Mean Sentence Length: {stats.get('mean_sentence_length', 12.0)} words. "
            f"Emojis: {top_emojis}] "
        )
        
        prompt_text = f"{system_prefix}Prompt: {user_prompt}\nResponse:"
        
        inputs = self.tokenizer(prompt_text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.85, # Adds stylistic variability
                top_p=0.92,       # Excludes low probability vocab tails
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id
            )
            
        full_decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Parse output to extract only the generated Response segment
        if "Response:" in full_decoded:
            response = full_decoded.split("Response:")[-1].strip()
        else:
            response = full_decoded[len(prompt_text):].strip()
            
        # Post-processing helper to append typical user signature emojis if missing
        if top_emojis and not any(e in response for e in top_emojis):
            response = f"{response} {top_emojis[:2]}"
            
        return response
