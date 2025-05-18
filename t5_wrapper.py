from transformers import T5Tokenizer, T5ForConditionalGeneration
from langchain_core.language_models.llms import LLM

class HuggingFaceT5(LLM):
    model_name: str = "gaussalgo/T5-LM-Large-text2sql-spider"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, "tokenizer", T5Tokenizer.from_pretrained(self.model_name))
        object.__setattr__(self, "model", T5ForConditionalGeneration.from_pretrained(self.model_name))

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: list = None) -> str:
        print(f"[Prompt to T5]: {prompt}")  # Expect: "Question: ...\nSchema: ..."

        input_ids = self.tokenizer.encode(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        output_ids = self.model.generate(input_ids, max_length=128)
        decoded_output = self.tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

        if "SELECT" in decoded_output.upper():
            sql_start = decoded_output.upper().index("SELECT")
            cleaned = decoded_output[sql_start:]
        else:
            cleaned = decoded_output

        print(f"[Cleaned SQL output]: {cleaned}")
        return cleaned
