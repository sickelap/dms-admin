from typing import Literal

from pydantic import BaseModel

VerificationStatus = Literal["applied", "failed", "verification_failed"]


class Account(BaseModel):
    email: str


class Alias(BaseModel):
    address: str
    target: str


class Quota(BaseModel):
    email: str
    quota: str


class RelayDomain(BaseModel):
    domain: str
    host: str | None = None
    port: int | None = None
    excluded: bool = False


class RelayAuth(BaseModel):
    domain: str
    username: str


class RelayState(BaseModel):
    domains: list[RelayDomain]
    auth: list[RelayAuth]


class CommandResult(BaseModel):
    stdout: str
    stderr: str
    exit_code: int


class MutationResult(BaseModel):
    status: VerificationStatus
    detail: str
