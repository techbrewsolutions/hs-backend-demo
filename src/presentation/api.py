from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.middleware.hubspot_verification import (
    HubSpotVerificationMiddleware,
)
from src.presentation.routers import auth_router, contacts_router

app = FastAPI(
    title="HS Backend Demo",
    description="Backend for HS Auth & Backend Api's",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add HubSpot verification middleware
app.add_middleware(HubSpotVerificationMiddleware)

# Include routers
app.include_router(auth_router)
app.include_router(contacts_router)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
