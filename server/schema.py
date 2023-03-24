from pydantic import BaseModel, Field


class GenarationInput(BaseModel):
    '''
    Input values for the text geneartion model
    '''

    input_prompt: str = Field(
        ...,
        example='This ship is taking me far away',
        title='Input prompt'
    )
    generate_len: int = Field(
        ...,
        example=500,
        title='Length of generated text'
    )


class GenerationResult(BaseModel):
    '''
    Generation result from the model
    '''

    generated_prompt = Field(
        ..., 
        example=f'This ship is taking me far away'
                f'Far away from the memories',
        title='Generated prompt'
    )


class GenerationResponse(BaseModel):
    '''
    Output response for model generation
    '''

    error: bool = Field(
        ...,
        example=False,
        title='Is there error or not'
    )
    results: GenerationResult = ...


class ErrorResponse(BaseModel):
    '''
    API error response
    '''

    error: bool = Field(
        ...,
        example=False,
        title='Is there error or not'
    )
    message: str = Field(..., example='', title='Error message')
    traceback: str = Field(None, example='', title='Error traceback')
