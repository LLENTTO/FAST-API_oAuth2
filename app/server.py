from fastapi import FastAPI, HTTPException                            # type: ignore

app = FastAPI()

bands = [
    {"id": 1, 'name': 'john'},
    {"id": 2, 'name' : 'mike'}
]

@app.get("/")
async def index():
    return {"Hello" : "worldh"}

@app.get("/bands")
async def getBands() -> list[dict]:
    return bands

@app.get("/bands/{band_id}", status_code=200) 
async def getBand(band_id: int) -> dict:
    band = next((b for b in bands if b['id'] == band_id), None)
    if band is None:
        # return 404
        raise HTTPException(status_code=404, detail="Band not found")
    return band
    