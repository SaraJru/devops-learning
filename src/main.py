"""
DevOps Learning API - A simple but scalable FastAPI application
to learn DevOps principles and best practices.
"""
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import logging
from datetime import datetime, timezone


from .config import get_config

# Configuration
config = get_config()

# Logging setup
logging.basicConfig(
    level=logging.INFO if not config.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# In-memory storage (for demo purposes)
contacts: Dict[int, Dict[str, Any]] = {}
contact_id_counter = 1


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Check if API is running"""
    logger.info("Health check endpoint called")
    return {
        "status": "OK",
        "message": "DevOps Learning API is running",
        "environment": config.ENV,
        "version": config.API_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    logger.info("Health check endpoint called")
    return {
        "status": "healthy",
        "environment": config.ENV,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post("/contacts", tags=["Contacts"])
async def create_contact(name: str, email: str, phone: str):
    """Create a new contact"""
    global contact_id_counter
    
    logger.info(f"Creating contact: {name} - {email}")
    
    if not name or not email or not phone:
        logger.warning("Invalid contact data provided")
        raise HTTPException(status_code=400, detail="All fields are required")
    
    contact_id = contact_id_counter
    contact_id_counter += 1
    
    contact = {
        "id": contact_id,
        "name": name,
        "email": email,
        "phone": phone,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    contacts[contact_id] = contact
    logger.info(f"Contact created successfully with ID: {contact_id}")
    
    return contact


@app.get("/contacts", tags=["Contacts"])
async def list_contacts():
    """List all contacts"""
    logger.info("Listing all contacts")
    return {
        "total": len(contacts),
        "contacts": list(contacts.values())
    }


@app.get("/contacts/{contact_id}", tags=["Contacts"])
async def get_contact(contact_id: int):
    """Get a specific contact by ID"""
    logger.info(f"Fetching contact with ID: {contact_id}")
    
    if contact_id not in contacts:
        logger.warning(f"Contact not found: {contact_id}")
        raise HTTPException(status_code=404, detail="Contact not found")
    
    return contacts[contact_id]


@app.get("/info", tags=["Info"])
async def get_api_info():
    """Get API information"""
    logger.info("Info endpoint called")
    return {
        "api_name": config.API_TITLE,
        "api_version": config.API_VERSION,
        "environment": config.ENV,
        "debug_mode": config.DEBUG,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info(f"Starting up API in {config.ENV} environment")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("Shutting down API")


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Running API on {config.HOST}:{config.PORT}")
    uvicorn.run(
        "src.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="debug" if config.DEBUG else "info"
    )