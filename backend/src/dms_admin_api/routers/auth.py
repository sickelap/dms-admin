from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from dms_admin_api.auth import clear_session_cookie, require_authenticated_user, set_session_cookie
from dms_admin_api.config import Settings, get_settings
from dms_admin_api.schemas import SessionResponse

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login", response_model=SessionResponse)
def login(
    payload: LoginRequest,
    response: Response,
    settings: Settings = Depends(get_settings),
) -> SessionResponse:
    if payload.username != settings.admin_username or payload.password != settings.admin_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    set_session_cookie(response, payload.username, settings)
    return SessionResponse(authenticated=True, username=payload.username)


@router.post("/logout", response_model=SessionResponse)
def logout(response: Response) -> SessionResponse:
    clear_session_cookie(response)
    return SessionResponse(authenticated=False)


@router.get("/session", response_model=SessionResponse)
def session(username: str = Depends(require_authenticated_user)) -> SessionResponse:
    return SessionResponse(authenticated=True, username=username)
