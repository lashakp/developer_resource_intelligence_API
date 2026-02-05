import os

API_KEY = os.getenv("API_KEY", "demo-key")


def verify_api_key_optional(api_key: str | None) -> str:
    """
    Returns access mode instead of raising errors.
    """
    if api_key and api_key == API_KEY:
        return "full"
    return "demo"
