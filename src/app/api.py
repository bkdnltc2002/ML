from .db.seed_data import seed_data
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .constants.config import settings
from .db.database import Base, engine
from .routers.audio_router import router as audio_router
from .routers.auth_router import router as auth_router
from .routers.car_router import router as car_router
from .routers.performance_router import router as performance_router
from .routers.playlist_audio_router import router as playlist_audio_router
from .routers.playlist_router import router as playlist_router
from .routers.user_router import router as user_router
from .db.database import get_db
from .routers.inquiry_router import router as inquiry_router
from .routers.brand_router import router as brand_router
from fastapi.staticfiles import StaticFiles
import os

db = Depends(get_db)
Base.metadata.create_all(bind=engine)

PREFIX = f"/api/{settings.API_VERSION}"

app = FastAPI(
    openapi_url=f"{PREFIX}/openapi.json",
    docs_url=f"{PREFIX}/docs",
    redoc_url=f"{PREFIX}/redoc",
)
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        + "/static",
        html=False,
    ),
    name="static",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(
    auth_router, tags=["Authenication"], prefix=f"{PREFIX}/auth"
)
app.include_router(user_router, tags=["User"], prefix=f"{PREFIX}/user")
app.include_router(audio_router, tags=["Audio"], prefix=f"{PREFIX}/audio")
app.include_router(
    playlist_router, tags=["Playlist"], prefix=f"{PREFIX}/playlist"
)
app.include_router(
    playlist_audio_router,
    tags=["Playlist Audio"],
    prefix=f"{PREFIX}/playlist-audio",
)
app.include_router(car_router, tags=["Car"], prefix=f"{PREFIX}/car")
app.include_router(
    performance_router, tags=["Performance"], prefix=f"{PREFIX}/performance"
)
app.include_router(
    inquiry_router, tags=["Inquiry"], prefix=f"{PREFIX}/inquiry"
)
app.include_router(
    brand_router, tags=["Brand"], prefix=f"{PREFIX}/brand"
)
@app.on_event("startup")
async def startup_event():
    seed_data()