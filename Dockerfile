FROM python:3.12-slim

WORKDIR /test

RUN pip install garak transformers torch accelerate safetensors

CMD ["sleep", "infinity"]
