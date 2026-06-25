from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class HFAdapter():
    def __init__(self, path):

        self.tokenizer = AutoTokenizer.from_pretrained(
            path,
            local_files_only=True,
            use_fast=False
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            path,
            local_files_only=True,
            device_map="auto",
            dtype=torch.float16,
            trust_remote_code=False
        )

    def generate(self,
                 prompt: list[dict],
                 max_new_tokens: int = 128,
                 temperature: float = 0.7,
                 top_p: float = 0.9) -> str:


        inputs = self.tokenizer(prompt[-1]["content"], return_tensors="pt")

        inputs = {
            k: v.to(self.model.device)
            for k, v in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

        return self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )
