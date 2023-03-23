import uvicorn
from fastapi import FastAPI, Request
from model import TextGenerationModel
from pydantic import BaseModel


app = FastAPI()
model = TextGenerationModel()


class InputData(BaseModel):
    input_prompt: str
    generate_len: int


@app.get('/')
async def hello():
    return {"message": "Hello, World!"}

@app.post('/predict')
async def predict(
    input_data: InputData,
    request: Request
):
    generated_prompt = model.generate(
        input_prompt=input_data.input_prompt,
        generate_len=input_data.generate_len
    )

    return {"generated_prompt": generated_prompt}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
