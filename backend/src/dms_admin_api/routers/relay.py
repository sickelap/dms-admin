from fastapi import APIRouter, Depends
from pydantic import BaseModel

from dms_admin_api.auth import require_authenticated_user
from dms_admin_api.dms.models import MutationResult, RelayState
from dms_admin_api.dms.service import DmsService, get_dms_service

router = APIRouter(prefix="/relay", tags=["relay"])


class AddRelayDomainRequest(BaseModel):
    domain: str
    host: str
    port: int | None = None


class AddRelayAuthRequest(BaseModel):
    domain: str
    username: str
    password: str


class ExcludeRelayDomainRequest(BaseModel):
    domain: str


@router.get("", response_model=RelayState)
def relay_state(
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> RelayState:
    return dms.relay_state()


@router.post("/domains", response_model=MutationResult)
def add_relay_domain(
    payload: AddRelayDomainRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.add_relay_domain(domain=payload.domain, host=payload.host, port=payload.port)


@router.post("/domains/exclude", response_model=MutationResult)
def exclude_relay_domain(
    payload: ExcludeRelayDomainRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.exclude_relay_domain(domain=payload.domain)


@router.post("/auth", response_model=MutationResult)
def add_relay_auth(
    payload: AddRelayAuthRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.add_relay_auth(domain=payload.domain, username=payload.username, password=payload.password)
