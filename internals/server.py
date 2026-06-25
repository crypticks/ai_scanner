import uvicorn
import os
from fastapi import FastAPI

from pydantic import BaseModel

class GenerateRequest(BaseModel):
    data: list[dict]

#-----------------SETUP SERVER, READ ENV-----------------#
app = FastAPI()

model_path = "/model"

adapter_name = os.environ["ADAPTER"]

print(adapter_name)
if adapter_name == "huggingface":
    from adapters.llm.huggingface import HFAdapter
    model = HFAdapter(model_path)
else:
    raise Exception("Unsupported adapter")




#--------------------ENDPOINT SETUP----------------------#
@app.post("/generate")
def generate(req: GenerateRequest):
    return {
        "text": model.generate(req.data)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
