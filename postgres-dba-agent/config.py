"""
Configuration module for Multi-Agent PostgreSQL DBA Assistant.
This module handles environment variables and configuration settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from .logging_config import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    """
    Centralized application configuration via Pydantic.
    Automatically loads variables from .env file and system environment.
    Validates and converts data types.
    """

    # Indicates to Pydantic to load variables from .env file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,  # Ignore empty variables
    )

    # ==========================================
    # VERTEX AI CONFIGURATION (Google Cloud)
    # ==========================================
    GOOGLE_CLOUD_PROJECT: str = "test-gcp-databases"
    GOOGLE_CLOUD_LOCATION: str = "global"
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
    GOOGLE_GENAI_USE_VERTEXAI: bool = True

    # ==========================================
    # MCP TOOLBOX CONFIGURATION (Cloud Run)
    # ==========================================
    TOOLBOX_URL: str = "https://xxxxx.run.app"
    TOOLSET_NAME: str = "postgres-dba-complete"

    # ==========================================
    # APPLICATION CONFIGURATION
    # ==========================================
    APP_NAME: str = "PostgreSQL DBA Multi-Agent"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Intelligent assistant for PostgreSQL database administration"
    )
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    DEFAULT_USER_ID: str = "dba_user"

    # ==========================================
    # MODEL CONFIGURATION
    # ==========================================
    MODEL_NAME: str = "gemini-2.5-flash"
    COORDINATOR_MODEL: str = "gemini-2.5-flash"
    SPECIALIZED_AGENTS_MODEL: str = "gemini-2.5-flash"

    def log_config(self):
        """Log current configuration (without sensitive data)"""
        logger.info("Current configuration:")
        logger.info(f"   - Application: {self.APP_NAME} v{self.APP_VERSION}")
        logger.info(f"   - Toolbox URL: {self.TOOLBOX_URL}")
        logger.info(f"   - Toolset: {self.TOOLSET_NAME}")
        logger.info(f"   - Model: {self.MODEL_NAME}")
        logger.info(f"   - Default user: {self.DEFAULT_USER_ID}")
        logger.info(f"   - Coordinator model: {self.COORDINATOR_MODEL}")
        logger.info(f"   - Specialized agents model: {self.SPECIALIZED_AGENTS_MODEL}")


def load_config():
    """
    Configuration loading function.
    This function is called by agents to ensure configuration is loaded.
    """
    try:
        # Create settings instance
        config = Settings()
        logger.info(
            f"✅ Configuration loaded for {config.APP_NAME} v{config.APP_VERSION}"
        )
        config.log_config()
        return config
    except Exception as e:
        logger.error(f"⚠️  Error loading configuration: {e}")
        logger.info("📝 Using default values...")
        # Return configuration with default values
        return Settings()


# Single settings instance, loaded at startup
settings = load_config()

# Create alias for backward compatibility
config = settings

# Export main elements for easy import
__all__ = ["settings", "config", "load_config", "Settings"]
