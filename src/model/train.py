import os
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from src.model.dataset import PersonalityTwinDataset
from typing import List, Dict

class ModelTrainer:
    """
    Phase 3: Deep Learning Model Training Pipeline
    Fine-tunes transformer models on a clean corpus of user messages.
    """
    def __init__(self, model_name: str = "distilgpt2", output_dir: str = "./results"):
        self.model_name = model_name
        self.output_dir = output_dir
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize Tokenizer and Causal LM
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(self.device)

    def train(self, training_data: List[Dict[str, str]], validation_data: List[Dict[str, str]], epochs: int = 3, batch_size: int = 4):
        """
        Runs the fine-tuning loop using Hugging Face's Trainer API.
        """
        train_dataset = PersonalityTwinDataset(training_data, self.tokenizer)
        val_dataset = PersonalityTwinDataset(validation_data, self.tokenizer)
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            overwrite_output_dir=True,
            num_train_epochs=epochs,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            eval_strategy="epoch",
            save_strategy="epoch",
            logging_steps=10,
            learning_rate=5e-5,
            weight_decay=0.01,
            warmup_steps=50,
            fp16=torch.cuda.is_available(), # Accelerate training if GPU is available
            logging_dir="./logs"
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            data_collator=data_collator
        )
        
        print("Starting Model Training...")
        trainer.train()
        
        # Save model and tokenizer checkpoint
        self.model.save_pretrained(os.path.join(self.output_dir, "best_model"))
        self.tokenizer.save_pretrained(os.path.join(self.output_dir, "best_model"))
        print(f"Model successfully saved to {self.output_dir}/best_model")
        
        return trainer.state.log_history
