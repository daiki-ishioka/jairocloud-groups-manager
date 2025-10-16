import hashlib


def compute_signature(client_secret: str, access_token: str, time_stamp: str) -> str:
    """Compute a SHA-256 signature."""
    return hashlib.sha256(
        f"{client_secret}{access_token}{time_stamp}".encode()
    ).hexdigest()
