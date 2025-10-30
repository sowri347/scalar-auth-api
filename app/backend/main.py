from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import auth_router
from ..db.database import connect_to_mongo, create_indexes

# Create FastAPI app with metadata
app = FastAPI(
    title="Auth API",
    description="Authentication API with JWT tokens",
    version="1.0.0"
)

# ✅ Enable CORS (Allow All Origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    return {
        "message": "Welcome to Auth API",
        "docs_url": "/docs",
        "auth_prefix": "/api/v1/auth"
    }

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()
    await create_indexes()

app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
