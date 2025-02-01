from fastapi import FastAPI                            # type: ignore

app = FastAPI()

myList = [
    {id: 1, 'name': 'john'}
]

@app.get("/")
async def index():
    return {"Hello" : "worldh"}

@app.get("/bands")
async def bands() -> list:
    return {}