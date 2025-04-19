from typing import Optional

from src.models.schemas.base import BaseSchemaModel
from typing import Optional


class RegisterRequestPayload(BaseSchemaModel):
    full_name: str
    email: str
    password: str
    mobile_number: Optional[str] = None
    role_id: int

class AccountInLogin(BaseSchemaModel):
    email: str
    password: str
