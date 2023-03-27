# language-modeling-app

![workflow badge](https://github.com/littlephony/language-modeling-app/actions/workflows/build_server.yml/badge.svg)

FastAPI application serving a PyTorch model for text generation.

## Table of contents

* [General info](#general-info)
* [Technology](#technology)
* [Setup](#setup)
* [How to use](#how-to-use)
* [Planned changes](#planned-changes)
* [Sources and inspiration](#sources-and-inspiration)

## General info

I trained a recurrent neural network with PyTorch to generate text in style of Jack London. I used 3 novels — _Martin Eden_, _The Sea-Wolf_, and _The Call of the Wild_ — as training data. To serve it, I used FastAPI web-framework.

## Technology

- `PyTorch` to train the model
- `FastAPI` to serve the model
- `uvicorn` to run ASGI
- `Pydantic` to validate requests and responses
- `Black` to format Python code

## Setup

1. Clone the repository

  ```
  $ git clone https://github.com/littlephony/language-modeling-app.git
  ```

2. Install dependencies specified in `requirements.txt` in `server` directory:

  ```
  $ cd server
  $ pip install -r requirements.txt
  ```

3. To run the application you can either simply run `app.py` file located in the `server` directory:

  ```
  $ python app.py
  ```

  or launch the app using `uvicorn`:


  ```
  $ uvicorn app:app --host 0.0.0.0 --port 8000
  ```

## How to use

To use the application you should make a `POST` request containing `input_prompt` and `generate_len` to the `/api/generate` endpoint:

```
$ curl -X 'POST' \
  'http://127.0.0.1:8000/api/generate' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_prompt": "This ship is taking me far away",
  "generate_len": 500
}'
```

To see the full documentation you should visit the `/docs` endpoint.

## Planned changes

I have the following changes planned for this project:

1. Use a more complex model — perhaphs a transformer — that would be able to generate a more meaningful text.
2. Add UI to make the application easier to use.

## Sources and inspiration

As I was developing this project I have drawn insight and inspiration from the following sources:

- [Machine Learning with PyTorch and Scikit-Learn by Sebastian Raschka](https://www.packtpub.com/product/machine-learning-with-pytorch-and-scikit-learn/9781801819312#_ga=2.34450529.1118007180.1679687705-725254805.1672444559)
- [Deploying PyTorch Model to Production with FastAPI in CUDA-supported Docker](https://medium.com/@mingc.me/deploying-pytorch-model-to-production-with-fastapi-in-cuda-supported-docker-c161cca68bb8)
