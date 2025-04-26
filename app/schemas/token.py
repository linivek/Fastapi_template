from pydantic import BaseModel


class Token(BaseModel):
    """
    OAuth2兼容的令牌
    """

    access_token: str
    token_type: str
