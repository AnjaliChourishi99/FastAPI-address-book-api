"""Address Book API - Main Application."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import init_db
from app.routers import addresses

# Configure logging
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown."""
    logger.info("Starting Address Book API...")
    init_db()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Address Book API",
    description="API for managing addresses with geographic coordinates.",
    lifespan=lifespan
)

app.include_router(addresses.router)


@app.get("/", tags=["Root"])
def root():
    """Health check endpoint."""
    return {"status": "healthy", "docs": "/docs"}
