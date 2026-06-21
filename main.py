import docker
import torch
from transformers import pipeline
from adapters import BaseAdapter

def main():

    path_on_system = "/home/kiwi/code/ai_scanner/models/tinyllama"
    path_in_env = "/model"

    #client = docker.from_env()

    #container = client.containers.run(
    #    image="test-image",

    #    detach=True,

    #    network_disabled=True,

    #    mem_limit="2g",

    #    volumes={
    #        "/home/kiwi/code/ai_scanner/models/tinyllama": {
    #            "bind": "/model",
    #            "mode": "ro"
    #        }
    #    }
    #)
    tokenizer = AutoTokenizer.from_pretrained("/home/kiwi/code/ai_scanner/models/tinyllama")
    model = AutoModelForCausalLM.from_pretrained(
        "/home/kiwi/code/ai_scanner/models/tinyllama",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    #generate function
    inputs = tokenizer("Hi", return_tensors="pt")

    # Move tensors to the same device as the model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    ##return response
    ##result = container.exec_run(
    ##    "garak "
    ##    "--verbose "
    ##    "--target_type huggingface.Model "
    ##    "--target_name /model "
    ##    "--probes lmrc.Profanity"
    ##)

    ##print(result.output.decode())
    print(response)

    #container.stop()
    #container.remove()

main()
