# api.py
""" FastAPI or Flask code for serving the model. """

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello from the Music Recommender API!'}
