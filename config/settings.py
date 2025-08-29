"""
Configuration settings for the automation framework.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration."""
    
    def __init__(self):
        """Initialize settings from environment variables."""
        # Base URLs
        self.base_url: str = os.getenv("BASE_URL", "https://playwright.dev")
        self.api_base_url: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
        
        # Browser settings
        self.browser: str = os.getenv("BROWSER", "chromium")
        self.headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
        self.slow_mo: int = int(os.getenv("SLOW_MO", "100"))
        
        # Test environment
        self.environment: str = os.getenv("ENVIRONMENT", "test")
        
        # Timeouts (in milliseconds)
        self.default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
        self.navigation_timeout: int = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
        
        # Screenshot and video settings
        self.take_screenshots: bool = os.getenv("TAKE_SCREENSHOTS", "true").lower() == "true"
        self.record_videos: bool = os.getenv("RECORD_VIDEOS", "false").lower() == "true"
        
        # Authentication (example)
        self.username: Optional[str] = os.getenv("TEST_USERNAME")
        self.password: Optional[str] = os.getenv("TEST_PASSWORD")
        
        # API settings
        self.api_timeout: int = int(os.getenv("API_TIMEOUT", "10"))
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        
    def get_browser_args(self) -> dict:
        """Get browser launch arguments."""
        return {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
            "args": [
                "--disable-dev-shm-usage",
                "--disable-extensions",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ] if os.getenv("CI") else []
        }
    
    def get_context_args(self) -> dict:
        """Get browser context arguments."""
        return {
            "viewport": {"width": 1920, "height": 1080},
            "ignore_https_errors": True,
            "record_video_dir": "reports/videos/" if self.record_videos else None,
        }
    
    def __str__(self) -> str:
        """String representation of settings."""
        return f"Settings(base_url={self.base_url}, browser={self.browser}, env={self.environment})" 