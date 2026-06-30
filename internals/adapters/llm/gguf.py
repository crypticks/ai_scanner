from llama_cpp import Llama

class GGUFAdapter():
    def __init__(self, path):

        self.model = Llama(model_path = path + "/model.gguf",
                           n_ctx = 1024,
                           n_gpu_layers = 0,
                           n_threads = 2)

    def generate(self,
                 prompt: list[dict],
                 max_new_tokens: int = 1024,
                 temperature: float = 0.7,
                 top_p: float = 0.9) -> str:

        response = self.model.create_chat_completion(
            messages= prompt,
            temperature=temperature,
            max_tokens=max_new_tokens,
            top_p = top_p
        )

        return response["choices"][0]["message"]["content"]

