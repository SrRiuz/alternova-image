# FastApi
from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

# Libs
from core.db.setup import setUp
from core.settings import ALLOWER_CORS_ORIGINS, DEBUG

# Modules
from modules.healthcheck.routes import router as healthcheck_router
from modules.images.routes import router as image_router


# Set up FastApi config
app = FastAPI()
handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWER_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the db config.
engine = setUp()

# Map the API routes
app.include_router(healthcheck_router)
app.include_router(image_router)
