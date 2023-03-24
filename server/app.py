import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse, JSONResponse

from model import TextGenerationModel
from schema import GenerationInput, GenerationResponse, GenerationResult, ErrorResponse
from exception_handler import validation_exception_handler, exception_handler


app = FastAPI(
    title="Text Generation Model",
    description="Generates text in the style of Jack London",
    version="0.0.1",
    terms_of_service=None,
    contact=None,
    license_info=None,
)


app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, exception_handler)


@app.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and variables
    """
    model = TextGenerationModel()

    app.package = {"model": model}


@app.post(
    "/api/predict",
    response_model=GenerationResponse,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def predict(request: Request, body: GenerationInput):
    generated_prompt = app.package["model"].generate(
        input_prompt=body.input_prompt, generate_len=body.generate_len
    )

    return {"generated_prompt": generated_prompt}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
