from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI()

# === Data models ===
class MoodInput(BaseModel):
    mood: str
    intensity: Optional[int] = 5

class Recipe(BaseModel):
    id: int
    name: str
    ingredients: List[str]
    instructions: str

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    preferences: Optional[dict] = {}

class Feedback(BaseModel):
    user_id: int
    recipe_id: int
    rating: int
    comment: Optional[str] = None

# In-memory placeholders (to be replaced with DB)
users_db = {}
recipes_db = {
    1: Recipe(id=1, name="Happy Pancakes", ingredients=["flour", "milk", "eggs"], instructions="Mix and cook.")
}
feedback_db = []

# === User Authentication & Registration ===
@app.post("/api/users")
async def register_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = user
    return {"message": "User registered"}

@app.post("/api/users/login")
async def login_user(user: User):
    stored_user = users_db.get(user.username)
    if not stored_user or stored_user.hashed_password != user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": "fake-jwt-token"}

@app.put("/api/users/{user_id}/preferences")
async def update_preferences(user_id: int, preferences: dict):
    # Dummy update
    for username, user in users_db.items():
        if user.id == user_id:
            user.preferences = preferences
            return {"message": "Preferences updated"}
    raise HTTPException(status_code=404, detail="User not found")

# === Recommendation API based on mood ===
@app.post("/api/recommendations")
async def get_recommendations(mood_input: MoodInput):
    # Simplified logic: return all recipes tagged with that mood
    # For demo, we ignore mood and return all recipes
    return list(recipes_db.values())

# === Recipe display ===
@app.get("/api/recipes/{recipe_id}")
async def get_recipe(recipe_id: int):
    recipe = recipes_db.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# === Feedback collection ===
@app.post("/api/feedback")
async def submit_feedback(feedback: Feedback):
    feedback_db.append(feedback)
    return {"message": "Feedback submitted"}

# === Search service ===
@app.get("/api/search")
async def search_recipes(query: Optional[str] = None):
    # Simplified search
    if not query:
        return list(recipes_db.values())
    return [r for r in recipes_db.values() if query.lower() in r.name.lower()]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
