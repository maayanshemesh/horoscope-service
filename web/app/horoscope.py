"""
Horoscope Service Module

This module handles horoscope data retrieval with caching capabilities using Redis.
It implements resilient external API communication with retry mechanisms and
comprehensive error handling.

Key Functions:
- get_horoscope_from_api(): Fetches horoscope data from external API with retry logic
- get_horoscope_for_sign(): Implements a caching strategy using Redis to minimize API calls

Features:
- Structured error handling with detailed logging
- Multiple retry attempts for API resilience
- 24-hour Redis caching to improve performance and reliability
- Proper response formatting for consistent data structure

The module follows best practices for external API integration including timeouts,
error handling, and structured logging for monitoring and debugging.
"""

import requests
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_horoscope_from_api(sign):
    """Fetch horoscope from external API for the given sign."""
    url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign.lower()}"

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=5)
            logger.info(f"[Attempt {attempt+1}] API URL: {url}")
            logger.info(f"[Attempt {attempt+1}] Status Code: {response.status_code}")

            if response.status_code == 200:
                api_response_data = response.json()

                if api_response_data.get("success") and "data" in api_response_data:
                    horoscope_content = api_response_data["data"]
                    return {
                        "sign": sign.capitalize(),
                        "date": horoscope_content.get("date", ""),
                        "description": horoscope_content.get("horoscope_data", "")
                    }
                else:
                    logger.warning(f"[Attempt {attempt+1}] API returned unexpected format: {api_response_data}")
            else:
                logger.warning(f"[Attempt {attempt+1}] Bad status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            logger.warning(f"[Attempt {attempt+1}] Network error: {e}")
        except json.JSONDecodeError as e:
            logger.warning(f"[Attempt {attempt+1}] Failed to parse JSON: {e}")
        except Exception as e:
            logger.warning(f"[Attempt {attempt+1}] Unexpected error: {e}")

    return {"error": "Failed to fetch horoscope data after multiple attempts"}

def get_horoscope_for_sign(sign, redis_client):
    """Get horoscope for sign, using Redis cache if available."""
    today = datetime.now().strftime('%Y-%m-%d')
    cache_key = f"horoscope:{sign}:{today}"

    cached_horoscope = redis_client.get(cache_key)

    if cached_horoscope:
        logger.info(f"[Cache HIT] Returning cached horoscope for {sign}")
        return json.loads(cached_horoscope)

    logger.info(f"[Cache MISS] Fetching new horoscope for {sign}")
    horoscope_data = get_horoscope_from_api(sign)

    if "error" not in horoscope_data:
        redis_client.setex(
            cache_key,
            86400,
            json.dumps(horoscope_data)
        )

    return horoscope_data
