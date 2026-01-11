from pydantic import BaseModel

class user_schema(BaseModel):
    username: str
    password: str