from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional
import uvicorn
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Simple FastAPI App", version="1.0.0")

# In-memory data store
data = [
    {"name": "Sam Larry", "age": 20, "track": "AI Developer"},
    {"name": "Bahubali", "age": 21, "track": "Backend Developer"},
    {"name": "John Doe", "age": 22, "track": "Frontend Developer"}
]

# Models
class Item(BaseModel):
    name: str = Field(..., example="Perpetual")
    age: int = Field(..., example=25)
    track: str = Field(..., example="Frontend Developer")

class PatchItem(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    track: Optional[str] = None

# Routes
@app.get("/", description="Returns a welcome message")
def root():
    return {"Message": "Welcome to my FastAPI Application"}

@app.get("/get-data")
def get_data():
    return data

@app.post("/create")
def create_data(req: Item):
    data.append(req.dict())
    return {"Message": "Data Received", "Data": data}

@app.put("/update-data/{id}")
def update_data(id: int, req: Item):
    if id >= len(data):
        raise HTTPException(status_code=404, detail="Record not found")
    data[id] = req.dict()
    return {"Message": "Data Updated", "Data": data}

@app.patch("/edit-data/{id}")
def edit_data(id: int, req: PatchItem):
    if id >= len(data):
        raise HTTPException(status_code=404, detail="Record not found")
    updates = req.model_dump(exclude_unset=True)
    if updates:
        data[id].update(updates)
        return {"Message": "Data Edited", "Data": data}
    return {"Message": "No fields to update", "Data": data}

@app.delete("/delete-data/{id}")
def delete_data(id: int):
    if id >= len(data):
        raise HTTPException(status_code=404, detail="Record not found")
    deleted = data.pop(id)
    return {"Message": "Data Deleted", "Deleted": deleted}

# Run the app
if __name__ == "__main__":
    host = os.getenv("host", "127.0.0.1")
    port = int(os.getenv("port", 8000))
    uvicorn.run(app, host=host, port=port)
