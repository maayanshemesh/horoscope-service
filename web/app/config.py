"""
Application Configuration Module

This module defines configuration settings for the application using environment variables
for flexibility across different deployment environments.

Configuration Parameters:
- REDIS_HOST: Redis server hostname (defaults to localhost)
- REDIS_PORT: Redis server port (defaults to 6379)

The Config class centralizes all configuration parameters and follows the principle of
configuration through environment variables, allowing for easy adjustment in
different deployment scenarios without code changes.
"""

import os

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
