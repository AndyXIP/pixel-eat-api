from fastapi import FastAPI
from app.views import posts, users, ingredients, badges

app = FastAPI(title="Pixel Eat API", version="0.1.0")

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(ingredients.router)
app.include_router(badges.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
