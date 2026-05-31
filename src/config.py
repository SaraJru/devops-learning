"""
Configuration module for the DevOps Learning API
"""
import os

class Config:
    """Base configuration"""
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENV: str = os.getenv("ENV", "development")
    API_VERSION: str = "v1"
    API_TITLE: str = "DevOps Learning API"
    API_DESCRIPTION: str = "A scalable API built with FastAPI for learning DevOps principles"

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = "development"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = "production"

def get_config() -> Config:
    """Get the appropriate configuration based on environment"""
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionConfig()
    return DevelopmentConfig()