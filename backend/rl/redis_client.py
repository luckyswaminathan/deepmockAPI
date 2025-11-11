"""Redis client with LFU eviction policy support."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import redis
from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def get_redis_client() -> redis.Redis:
    """Get Redis client instance."""
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.from_url(url, decode_responses=True)


def ensure_lfu_policy(maxmemory_bytes: Optional[int] = None) -> None:
    """
    Ensure Redis is configured with LFU eviction policy.
    
    Args:
        maxmemory_bytes: Maximum memory in bytes. If None, uses REDIS_MAXMEMORY env var.
    """
    client = get_redis_client()
    
    try:
        # Check current policy
        current_policy = client.config_get("maxmemory-policy").get("maxmemory-policy", "")
        
        if current_policy != "allkeys-lfu":
            print(
                f"[RL] Warning: Redis eviction policy is '{current_policy}', "
                "not 'allkeys-lfu'. Setting to LFU..."
            )
            client.config_set("maxmemory-policy", "allkeys-lfu")
            print("[RL] Redis eviction policy set to 'allkeys-lfu'")
        else:
            print("[RL] Redis eviction policy already set to 'allkeys-lfu'")
        
        # Set maxmemory if provided
        if maxmemory_bytes is None:
            maxmemory_bytes = int(os.getenv("REDIS_MAXMEMORY", "2147483648"))  # 2GB default
        
        current_maxmemory = client.config_get("maxmemory").get("maxmemory", "0")
        if current_maxmemory == "0" or int(current_maxmemory) != maxmemory_bytes:
            client.config_set("maxmemory", str(maxmemory_bytes))
            print(f"[RL] Redis maxmemory set to {maxmemory_bytes / (1024**3):.2f} GB")
        
    except redis.exceptions.ConnectionError as e:
        raise RuntimeError(
            f"Failed to connect to Redis at {os.getenv('REDIS_URL', 'redis://localhost:6379/0')}. "
            "Ensure Redis is running and REDIS_URL is correct."
        ) from e
    except Exception as e:
        print(f"[RL] Warning: Could not configure Redis LFU policy: {e}")
        # Don't fail if we can't configure, just warn

