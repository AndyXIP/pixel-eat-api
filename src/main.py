from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from views import posts, users, ingredients, badges
from views import feed, diary, events, recipes_mock, profile_mock
import os

app = FastAPI(title="Pixel Eat API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static image files
assets_path = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
app.mount("/images", StaticFiles(directory=assets_path), name="images")

# Mock data routers (no auth required)
app.include_router(feed.router)
app.include_router(diary.router)
app.include_router(events.router)
app.include_router(recipes_mock.router)
app.include_router(profile_mock.router)

# Real routers (auth required — keep as is)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(ingredients.router)
app.include_router(badges.router)


@app.get("/utils/health")
async def health():
    return {"status": "ok"}
