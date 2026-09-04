from pydantic import BaseModel

class Response_Access_And_Refresh_Token(BaseModel):
    access_token: str
    refresh_token: str