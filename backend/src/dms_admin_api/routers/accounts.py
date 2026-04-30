from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

from dms_admin_api.auth import require_authenticated_user
from dms_admin_api.dms.models import Account, MutationResult
from dms_admin_api.dms.service import DmsService, get_dms_service

router = APIRouter(prefix="/accounts", tags=["accounts"])


class CreateAccountRequest(BaseModel):
    email: EmailStr
    password: str


class UpdatePasswordRequest(BaseModel):
    password: str


@router.get("", response_model=list[Account])
def list_accounts(
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> list[Account]:
    return dms.list_accounts()


@router.post("", response_model=MutationResult)
def create_account(
    payload: CreateAccountRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.create_account(email=str(payload.email), password=payload.password)


@router.post("/{email}/password", response_model=MutationResult)
def update_password(
    email: EmailStr,
    payload: UpdatePasswordRequest,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.update_account_password(email=str(email), password=payload.password)


@router.delete("/{email}", response_model=MutationResult)
def delete_account(
    email: EmailStr,
    _: str = Depends(require_authenticated_user),
    dms: DmsService = Depends(get_dms_service),
) -> MutationResult:
    return dms.delete_account(email=str(email))
