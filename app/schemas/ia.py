from pydantic import BaseModel


class AI_request(BaseModel):
  prompt: str