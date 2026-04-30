import base64
import hashlib
import hmac
import json
import time
from typing import Any

from fastapi import Depends, HTTPException, Request, Response, status

from dms_admin_api.config import Settings, get_settings

SESSION_COOKIE = "dms_admin_session"
SESSION_TTL_SECONDS = 60 * 60 * 8


def _encode_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _decode_payload(value: str) -> dict[str, Any]:
    padding = "=" * (-len(value) % 4)
    raw = base64.urlsafe_b64decode(f"{value}{padding}".encode())
    return json.loads(raw.decode())


def _sign(value: str, secret: str) -> str:
    return hmac.new(secret.encode(), value.encode(), hashlib.sha256).hexdigest()


def create_session_token(username: str, settings: Settings) -> str:
    payload = {"sub": username, "exp": int(time.time()) + SESSION_TTL_SECONDS}
    encoded = _encode_payload(payload)
    signature = _sign(encoded, settings.session_secret)
    return f"{encoded}.{signature}"


def read_session_token(token: str, settings: Settings) -> dict[str, Any] | None:
    try:
        encoded, signature = token.split(".", maxsplit=1)
    except ValueError:
        return None

    expected = _sign(encoded, settings.session_secret)
    if not hmac.compare_digest(signature, expected):
        return None

    try:
        payload = _decode_payload(encoded)
    except (ValueError, json.JSONDecodeError):
        return None

    expires_at = payload.get("exp")
    if not isinstance(expires_at, int) or expires_at < int(time.time()):
        return None

    return payload


def set_session_cookie(response: Response, username: str, settings: Settings) -> None:
    token = create_session_token(username, settings)
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
    )


def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(key=SESSION_COOKIE)


def require_authenticated_user(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> str:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    payload = read_session_token(token, settings)
    if not payload or not isinstance(payload.get("sub"), str):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    return payload["sub"]
