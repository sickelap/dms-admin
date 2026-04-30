from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    environment: str


class SessionResponse(BaseModel):
    authenticated: bool
    username: str | None = None


class SystemStateResponse(BaseModel):
    dms_container_name: str
    dms_reachable: bool
