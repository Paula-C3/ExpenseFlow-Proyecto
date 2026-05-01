from pydantic import BaseModel


class TokenResponseDTO(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int
